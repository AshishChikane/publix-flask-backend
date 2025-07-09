from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from jwt import decode as jwt_decode, InvalidTokenError
from jwt.exceptions import InvalidTokenError
import os
import logging
from Models.Brand import Brand
from Models.Campaign import Campaign
from Models.BrandCategory import BrandCategory
from Config.db import db
import difflib
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import get_buffer_string
import uuid

SECRET_KEY = "publiX-jwt-secret"  # Use the same secret key used for signing the JWT

logging.basicConfig(level=logging.INFO)

# Set up environment
os.environ["GROQ_API_KEY"] = "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"

# Initialize LLaMA 3 model with GROQ
model = init_chat_model("llama3-8b-8192", model_provider="groq")
last_data = {}

# ✅ LangChain Memory for whole session
memory = ConversationBufferMemory(return_messages=True)

# ✅ Prompts
classification_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a master classification agent for a platform. "
     "Your task is to categorize each user query as either **'product'** or **'data'**.\n\n"
     "- Use **'product'** if the user asks how the platform works, requests instructions, or engages in greetings, small talk, or general chit-chat (e.g. 'hi', 'hello', 'how are you').\n"
     "- **'Data'**: Use this only if the user is specifically requesting information like lists, counts, statistics, or raw data.\n\n"
     "Always respond with exactly one word: **'product'** or **'data'**. "
     "Do not include any extra text, punctuation, or explanation.\n\n"
     "Query: {query}")
])

classification_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict master classifier agent. "
     "Classify each user query into exactly one of: "
     "'product', 'data', 'create', or 'chitchat'.\n\n"
     "- Use 'product' for platform-related questions or instructions.\n"
     "- Use 'data' for requests like lists or counts.\n"
     "- Use 'create' for requests to create something.\n"
     "- Use 'chitchat' for greetings, jokes, or casual conversation.\n\n"
     "Return only one lowercase word without any punctuation or extra explanation."),
    ("user", "How do I create a campaign?"),
    ("assistant", "product"),
    ("user", "Give me a list of all campaigns."),
    ("assistant", "data"),
    ("user", "Create a brand for me."),
    ("assistant", "create"),
    ("user", "{query}")
])


product_prompt = ChatPromptTemplate.from_messages([
    ("system", "A Campaign is created by an Advertiser within the platform to achieve specific marketing objectives, such as driving brand awareness, increasing engagement, or generating conversions. The Advertiser can add a campaign and customize its settings, including selecting targeting options such as multiple locations, screens, age groups, proximities, and more. This allows the Advertiser to precisely define where, when, and to whom the campaign will be shown. Once the campaign is set up with the relevant details and creatives, it is sent for approval, and upon approval, it becomes active for execution. "
     "A Creative is the actual ad content used in a campaign, designed to engage the target audience and achieve the campaign's objectives. Creatives can include various types of media such as images, videos. The Advertiser can upload and customize creatives for the campaign, and these will be displayed across selected advertising channels (e.g. digital billboards). Creatives are typically aligned with the campaign's goals, whether it's increasing brand awareness, driving conversions, or generating user engagement. Each creative can be tailored to specific targeting parameters, such as age group, location, or device type, ensuring it reaches the right audience at the right time."
     "A Brand is a unique identity created by an Advertiser or business to represent their products, services, or company in the market. In the advertising platform, the Advertiser can add a brand, which becomes a key part of their campaign strategy. Once a brand is created, it allows the Advertiser to manage campaigns, creatives, and other promotional activities under that specific brand identity. A brand also helps to ensure consistency across marketing efforts and enables the Advertiser to track performance and reach specific target audiences."
     "A Publisher is an entity or platform that owns and manages advertising space or inventory, where Advertisers can display their ads. Publishers provide ad placements on various digital or physical properties such as digital signage, and physical screens (e.g., billboards). In the advertising ecosystem, a Publisher allows Advertisers to access their inventory to reach a specific audience. Once a Publisher is added to the Advertiser's network, the Advertiser can use the Publisher's inventory to run campaigns, targeting selected locations, screens, or other parameters. Publishers often monetize their platforms by selling ad space to Advertisers, either through direct deals or programmatic advertising."),
     "Please answer it professionally as we are need to explain it very nicely and we need to skip 'In the context of digital advertising'",
    ("user", "{query}")
])

data_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a strict table classifier. "
     "Classify the query into one word: users, campaigns, locations, screens, brands, creatives, "
     "campaign-planner, campaign-performance, or publishers. "
     "Return only the word."),
    ("user", "Give me all brands."),
    ("assistant", "brands"),
    ("user", "{query}")
])

chit_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a friendly conversational assistant. You can engage in small talk, answer casual questions, "
     "tell jokes, or just chat politely and warmly. Respond naturally and helpfully."),
    ("user", "{query}")
])


# ✅ Serializers
def serialize_brand(brand):
    return {"id": brand.id, "name": brand.brand_name}

def serialize_campaign(campaign):
    return {"id": campaign.id, "name": campaign.campaign_name, "is_active": campaign.is_active}

def get_brand_categories():
    categories = BrandCategory.query.all()
    return [{"id": c.id, "name": c.brand_type} for c in categories]

def create_uuid():
    return str(uuid.uuid4())

# Helper validation
def verify_classification(category):
    VALID_CATEGORIES = {"product", "data", "create", "chitchat"}
    return category in VALID_CATEGORIES


# =========================
# SAFE INVOKE
# =========================

def safe_invoke(chain, query):
    try:
        result = chain.invoke({"query": query})
        content = result.content.strip().lower()
        logging.info(f"LLM output: {content}")
        return content
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return None

# ✅ Master Agent
def master_agent(query):
    print("query",query)
    memory.chat_memory.add_user_message(query)
    chain = classification_prompt | model
    result = chain.invoke({"query": query})
    print("result",result)
    return result.content.strip().lower()

# ✅ Product Agent
def product_agent(query):
    chain = product_prompt | model
    result = chain.invoke({"query": query})
    answer = result.content.strip()
    memory.chat_memory.add_ai_message(answer)
    return answer


# ✅ Data Agent
def data_agent(query):
    global last_data
    table_name = safe_invoke(data_prompt | model, query)

    handlers = {
        "campaigns": (Campaign, serialize_campaign),
        "brands": (Brand, serialize_brand),
    }

    if table_name in handlers:
        Model, serializer = handlers[table_name]
        records = Model.query.all()
        output = [serializer(r) for r in records]
        last_data["result"] = output
        last_data["type"] = table_name

        # ✅ NEW: Apply BOTH filters if applicable
        if table_name == "campaigns":
            query_lower = query.lower()

            is_active_map = {
                "pending": 0,
                "active": 1,
                "complete": 2,
                "completed": 2,
                "pause": 4,
                "paused": 4
            }

            workflow_status_map = {
                "new": 0,
                "inreview": 1,
                "review": 1,
                "update": 2,
                "approve": 3,
                "approved": 3,
                "reject": 4,
                "rejected": 4,
                "new ad": 5,
                "newad": 5
            }

            # Filter for is_active status
            for keyword, status_value in is_active_map.items():
                if keyword in query_lower:
                    output = [r for r in output if r.get("is_active") == status_value]
                    memory.chat_memory.add_ai_message(
                        f"{len(output)} campaigns with is_active status '{keyword}'."
                    )
                    break  # only first match

            # Filter for workflow status
            for keyword, status_value in workflow_status_map.items():
                if keyword in query_lower:
                    output = [r for r in output if r.get("status") == status_value]
                    memory.chat_memory.add_ai_message(
                        f"{len(output)} campaigns with workflow status '{keyword}'."
                    )
                    break  # only first match

        memory.chat_memory.add_ai_message(f"Fetched {len(output)} {table_name}.")
        return output

    # ✅ Fallback on previous result if LLM failed classification
    elif last_data and "campaign" in last_data.get("type", ""):
        query_lower = query.lower()
        is_active_map = {
            "pending": 0,
            "active": 1,
            "complete": 2,
            "completed": 2,
            "pause": 4,
            "paused": 4
        }
        workflow_status_map = {
            "new": 0,
            "inreview": 1,
            "review": 1,
            "update": 2,
            "approve": 3,
            "approved": 3,
            "reject": 4,
            "rejected": 4,
            "new ad": 5,
            "newad": 5
        }

        # Try is_active fallback first
        for keyword, status_value in is_active_map.items():
            if keyword in query_lower:
                filtered = [
                    r for r in last_data["result"]
                    if r.get("is_active") == status_value
                ]
                memory.chat_memory.add_ai_message(
                    f"{len(filtered)} campaigns with is_active status '{keyword}' from last result."
                )
                return filtered

        # Try workflow fallback
        for keyword, status_value in workflow_status_map.items():
            if keyword in query_lower:
                filtered = [
                    r for r in last_data["result"]
                    if r.get("status") == status_value
                ]
                memory.chat_memory.add_ai_message(
                    f"{len(filtered)} campaigns with workflow status '{keyword}' from last result."
                )
                return filtered

    msg = f"No handler for '{table_name}'. Valid: {list(handlers.keys())}."
    memory.chat_memory.add_ai_message(msg)
    return {"error": msg}


last_creation = {}

# creation agent
def creation_agent(query, user_id):
    global last_creation

    if not last_creation:
        if "brand" in query.lower():
            last_creation["type"] = "brand"
            memory.chat_memory.add_ai_message(
                "Sure! Please provide the name for the new brand."
            )
            return "Sure! Please provide the name for the new brand."
        else:
            msg = "I can only create brands for now. More coming soon!"
            memory.chat_memory.add_ai_message(msg)
            return msg

    if last_creation["type"] == "brand" and "name" not in last_creation:
        last_creation["name"] = query.strip()
        categories = get_brand_categories()
        if not categories:
            msg = "No brand categories found in the database."
            memory.chat_memory.add_ai_message(msg)
            last_creation = {}
            return msg

        categories_str = "\n".join([f"{c['id']}: {c['name']}" for c in categories])
        msg = (
            f"Great! Your brand name is **{last_creation['name']}**.\n"
            f"Now, please type the **category name** you want from this list:\n{categories_str}"
        )
        memory.chat_memory.add_ai_message(msg)
        last_creation["categories"] = categories
        return msg

    if last_creation["type"] == "brand" and "category_id" not in last_creation:
        user_input = query.strip().lower()
        categories = last_creation["categories"]

        exact_matches = [
            c for c in categories if c["name"].lower() == user_input
        ]

        if exact_matches:
            selected = exact_matches[0]
            last_creation["category_id"] = selected["id"]

        else:
            
            possible_names = [c["name"] for c in categories]
            close_matches = difflib.get_close_matches(query, possible_names, n=1, cutoff=0.6)
            if close_matches:
                best_match = close_matches[0]
                last_creation["suggested"] = best_match
                msg = f"Did you mean **'{best_match}'**? Please type 'yes' to confirm or type the correct category name again."
                memory.chat_memory.add_ai_message(msg)
                return msg
            else:
                msg = "No similar category found. Please check the spelling and type again."
                memory.chat_memory.add_ai_message(msg)
                return msg
    
        new_brand = Brand(
            brand_uuid = create_uuid(),
            brand_name=last_creation["name"],
            category_id=last_creation["category_id"],
            advertiser_id=5,   # ⚠️ you must set this properly too!
            user_id=user_id    # ✅ From token
        )
        db.session.add(new_brand)
        db.session.commit()

        msg = f"✅ Brand '{new_brand.brand_name}' created successfully!"
        memory.chat_memory.add_ai_message(msg)
        last_creation = {}
        return msg

    if last_creation["type"] == "brand" and "suggested" in last_creation:
        if query.strip().lower() in ["yes", "y"]:
            confirmed_name = last_creation["suggested"]
            categories = last_creation["categories"]
            selected = next((c for c in categories if c["name"] == confirmed_name), None)

            if selected:
                last_creation["category_id"] = selected["id"]
                print('brand', brand_name=last_creation["name"],
                    category_id=selected["id"],
                    advertiser_id=1,  # ⚠️ fix this
                    user_id=user_id   # ✅
                    )
                new_brand = Brand(
                    brand_name=last_creation["name"],
                    category_id=selected["id"],
                    advertiser_id=1,  # ⚠️ fix this
                    user_id=user_id   # ✅ From token
                )
                db.session.add(new_brand)
                db.session.commit()

                msg = f"✅ Brand '{new_brand.brand_name}' created successfully!"
                memory.chat_memory.add_ai_message(msg)
                last_creation = {}
                return msg

            else:
                msg = "Something went wrong matching the category. Please start again."
                memory.chat_memory.add_ai_message(msg)
                last_creation = {}
                return msg

    msg = "Something went wrong during brand creation. Please start again."
    memory.chat_memory.add_ai_message(msg)
    last_creation = {}
    return msg

# ChitChat Agent
def chit_chat_agent(query):
    chain = chit_chat_prompt | model
    result = chain.invoke({"query": query})
    answer = result.content.strip()
    memory.chat_memory.add_ai_message(answer)
    return answer

# ✅ Main Flask route
# def getMasterAgentResponse():
#     auth_header = request.headers.get("Authorization", None)
#     if not auth_header or not auth_header.startswith("Bearer "):
#         return jsonify({"error": "Missing or invalid Authorization header"}), 401

#     token = auth_header.split(" ")[1]
#     try:
#         payload = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])
#         user_id = payload.get("id")
#         if not user_id:
#             return jsonify({"error": "Token missing user_id claim."}), 401
#     except InvalidTokenError:
#         return jsonify({"error": "Invalid or expired token"}), 401

#     data = request.json
#     query = data.get("query", "").strip()

#     if not query:
#         return jsonify({"error": "Query cannot be empty"}), 400

#     global last_creation

#     if last_creation:
#         response = creation_agent(query, user_id)
#         category = "create"
#     else:
#         MAX_ATTEMPTS = 3
#         attempt = 0
#         category = None

#         while attempt < MAX_ATTEMPTS:
#             category = master_agent(query)
#             if verify_classification(category):
#                 break
#             logging.warning(f"Invalid classification '{category}' from LLM, attempt {attempt + 1}")
#             attempt += 1

#         if not verify_classification(category):
#             return jsonify({"error": f"Invalid classification '{category}' after retries."}), 400

#         if category == "product":
#             response = product_agent(query)
#         elif category == "data":
#             response = data_agent(query)
#         elif category == "create":
#             response = creation_agent(query, user_id)
#         elif category == "chitchat":
#             response = chit_chat_agent(query)
#         else:
#             return jsonify({"error": f"Unhandled classification '{category}'"}), 400

#     if isinstance(response, dict) and response.get("error"):
#         return jsonify(response), 400

#     with open("logs.jsonl", "a") as f:
#         f.write(f'{{"query": "{query}", "category": "{category}", "response": "{response}"}}\n')

#     history_str = get_buffer_string(memory.load_memory_variables({})["history"])
#     return jsonify({
#         "category": category,
#         "response": response,
#         "chat_history": history_str
#     }), 200

async def getMasterAgentResponse(request: Request):
    # --- 1️⃣ Auth header ---
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing user_id claim.")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # --- 2️⃣ Parse JSON body ---
    body = await request.json()
    query = body.get("query", "").strip()

    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    global last_creation

    # --- 3️⃣ Routing logic ---
    if last_creation:
        response = creation_agent(query, user_id)
        category = "create"
    else:
        MAX_ATTEMPTS = 3
        attempt = 0
        category = None

        while attempt < MAX_ATTEMPTS:
            category = master_agent(query)
            if verify_classification(category):
                break
            logging.warning(f"Invalid classification '{category}' from LLM, attempt {attempt + 1}")
            attempt += 1

        if not verify_classification(category):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid classification '{category}' after retries."
            )

        if category == "product":
            response = product_agent(query)
        elif category == "data":
            response = data_agent(query)
        elif category == "create":
            response = creation_agent(query, user_id)
        elif category == "chitchat":
            response = chit_chat_agent(query)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unhandled classification '{category}'"
            )

    # --- 4️⃣ Handle error response ---
    if isinstance(response, dict) and response.get("error"):
        raise HTTPException(status_code=400, detail=response["error"])

    # --- 5️⃣ Write logs ---
    with open("logs.jsonl", "a") as f:
        f.write(f'{{"query": "{query}", "category": "{category}", "response": "{response}"}}\n')

    history_str = get_buffer_string(memory.load_memory_variables({})["history"])

    return JSONResponse(
        status_code=200,
        content={
            "category": category,
            "response": response,
            "chat_history": history_str
        }
    )
