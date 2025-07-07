from flask import request, jsonify
import jwt
from jwt.exceptions import InvalidTokenError
import os

from Models.Brand import Brand
from Models.Campaign import Campaign
from Config.db import db

from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import get_buffer_string

SECRET_KEY = "publiX-jwt-secret"  # Use the same secret key used for signing the JWT

# Set up environment
os.environ["GROQ_API_KEY"] = "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"

# Initialize LLaMA 3 model with GROQ
model = init_chat_model("llama3-8b-8192", model_provider="groq")
last_data = {}

# # Master Agent Prompt for classification
# classification_prompt = ChatPromptTemplate.from_messages([
#     ("system", 
#      "You are a master agent responsible for classifying user queries into two categories: 'product' or 'data'. "
#      "'Product' queries focus on understanding the product, its features, and usage. Examples include: "
#      "'How do I start?', 'What are the key features?', 'What steps should I follow?', 'What does this do?', "
#      "'Is this genuine?'. In short, these questions aim to explore the product's functionality and characteristics. "
#      "'Data' queries focus on retrieving lists, datasets, or counts. Examples include: "
#      "'How many brands are available?', 'How many campaigns are running?', 'Provide me the dataset for this', "
#      "'Give me the list of these items'. In short, these questions aim to gather data or metrics. "
#      "Classify the following query strictly into either 'product' or 'data': {query}"   
#      "please response in one word"
#     )
# ]) 

# # Product Information Agent Prompt
# product_prompt = ChatPromptTemplate.from_messages([
#     ("system", "A Campaign is created by an Advertiser within the platform to achieve specific marketing objectives, such as driving brand awareness, increasing engagement, or generating conversions. The Advertiser can add a campaign and customize its settings, including selecting targeting options such as multiple locations, screens, age groups, proximities, and more. This allows the Advertiser to precisely define where, when, and to whom the campaign will be shown. Once the campaign is set up with the relevant details and creatives, it is sent for approval, and upon approval, it becomes active for execution. "
#      "A Creative is the actual ad content used in a campaign, designed to engage the target audience and achieve the campaign's objectives. Creatives can include various types of media such as images, videos. The Advertiser can upload and customize creatives for the campaign, and these will be displayed across selected advertising channels (e.g. digital billboards). Creatives are typically aligned with the campaign's goals, whether it's increasing brand awareness, driving conversions, or generating user engagement. Each creative can be tailored to specific targeting parameters, such as age group, location, or device type, ensuring it reaches the right audience at the right time."
#      "A Brand is a unique identity created by an Advertiser or business to represent their products, services, or company in the market. In the advertising platform, the Advertiser can add a brand, which becomes a key part of their campaign strategy. Once a brand is created, it allows the Advertiser to manage campaigns, creatives, and other promotional activities under that specific brand identity. A brand also helps to ensure consistency across marketing efforts and enables the Advertiser to track performance and reach specific target audiences."
#      "A Publisher is an entity or platform that owns and manages advertising space or inventory, where Advertisers can display their ads. Publishers provide ad placements on various digital or physical properties such as digital signage, and physical screens (e.g., billboards). In the advertising ecosystem, a Publisher allows Advertisers to access their inventory to reach a specific audience. Once a Publisher is added to the Advertiser's network, the Advertiser can use the Publisher's inventory to run campaigns, targeting selected locations, screens, or other parameters. Publishers often monetize their platforms by selling ad space to Advertisers, either through direct deals or programmatic advertising."),
#      "Please answer it professionally as we are need to explain it very nicely and we need to skip 'In the context of digital advertising'",
#     ("user", "{query}")
# ])

# # Data Request Agent Prompt
# data_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a professional agent classifying user queries as one of the following: 'users', 'campaigns',,'locations','screens' 'brands', 'creatives','campaign-planner','campaign-performance, or 'publishers'. Answer it in one word."),
#     ("user", "{query}")
# ])

# def master_agent(query):
#     """Classify query into 'product' or 'data'"""
#     prompt = classification_prompt.invoke({'query': query})
#     response = model.invoke(prompt)
#     category = response.content.strip().lower()
#     return category.lower() if category.lower() in ['product', 'data'] else 'product'

# def product_agent(query):
#     """Handle product-related queries"""
#     prompt = product_prompt.invoke({'query': query})
#     response = model.invoke(prompt)
#     return response.content.strip()

# def data_agent(query):
#     """Handle data-related queries"""
#     prompt = data_prompt.invoke({'query': query})
#     response = model.invoke(prompt)
#     print("response:", response)

#     table_name = response.content.strip().lower()

#     if table_name == "brands":
#         results = Brand.query.all()
#         return [serialize_brand(b) for b in results]

#     elif table_name == "campaigns":
#         results = Campaign.query.all()
#         return [serialize_campaign(c) for c in results]

#     else:
#         return {"error": f"No handler for table: {table_name}"}


# def serialize_brand(brand):
#     return {
#         "name": brand.brand_name,
#     }

# def serialize_campaign(campaign):
#     return {
#         "name": campaign.campaign_name,
#     }

# def getMasterAgentResponse():
#     # Extract Authorization header
#     auth_header = request.headers.get('Authorization', None)
#     if not auth_header or not auth_header.startswith('Bearer '):
#         return jsonify({"error": "Missing or invalid Authorization header"}), 401

#     # Get the token string
#     token = auth_header.split(" ")[1]

#     # Decode / decrypt the token
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         print(payload)
#         # Now you can access user info inside payload
#         user_id = payload.get("id")
#         # ... do something with user_id if needed
#     except InvalidTokenError:
#         return jsonify({"error": "Invalid or expired token"}), 401

#     data = request.json
#     query = data.get("query", "")
   
#     # Classify query
#     category = master_agent(query)

#     # Route query to appropriate agent
#     if category == 'product':
#         response = product_agent(query)
#     else:
#         response = data_agent(query)

#     return jsonify({"category": category, "response": response, "user_id": user_id})

# ✅ LangChain Memory for whole session
memory = ConversationBufferMemory(return_messages=True)

# ✅ Prompts
classification_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a master agent responsible for classifying user queries into two categories: 'product' or 'data'. "
     "'Product' means the user wants to understand how the platform works. "
     "'Data' means they want lists, counts or raw data. "
     "Classify the following query strictly as 'product' or 'data': {query}. Please respond in one word.")
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
     "You are a data domain agent. "
     "Classify the query as exactly one of: 'users', 'campaigns', 'locations', 'screens', "
     "'brands', 'creatives', 'campaign-planner', 'campaign-performance', or 'publishers'. "
     "Answer with one word only."),
    ("user", "{query}")
])

# ✅ Serializers
def serialize_brand(brand):
    return {"id": brand.id, "name": brand.brand_name}

def serialize_campaign(campaign):
    return {"id": campaign.id, "name": campaign.campaign_name, "is_active": campaign.is_active}

# ✅ Master Agent
def master_agent(query):
    memory.chat_memory.add_user_message(query)
    chain = classification_prompt | model
    result = chain.invoke({"query": query})
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
    chain = data_prompt | model
    result = chain.invoke({"query": query})
    table_name = result.content.strip().lower()

    handlers = {
        "campaigns": (Campaign, serialize_campaign),
        "brands": (Brand, serialize_brand),
    }

    handler = handlers.get(table_name)
    if handler:
        Model, serializer = handler
        records = Model.query.all()
        output = [serializer(r) for r in records]
        last_data["result"] = output
        last_data["type"] = table_name
        memory.chat_memory.add_ai_message(f"Fetched {len(output)} {table_name}.")
        return output
    else:
        # try refinement of last_data
        if last_data and "campaign" in last_data.get("type", ""):
            if "active" in query:
                active_only = [r for r in last_data["result"] if r.get("is_active")]
                memory.chat_memory.add_ai_message(f"{len(active_only)} active campaigns from previous list.")
                return active_only
        msg = f"No handler for {table_name} and no filter matched."
        memory.chat_memory.add_ai_message(msg)
        return {"error": msg}
    
# ✅ Main Flask route
def getMasterAgentResponse():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing or invalid Authorization header"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except InvalidTokenError:
        return jsonify({"error": "Invalid or expired token"}), 401

    data = request.json
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Query cannot be empty"}), 400

    category = master_agent(query)
    if category == "product":
        response = product_agent(query)
    else:
        response = data_agent(query)

    history_str = get_buffer_string(memory.load_memory_variables({})["history"])
    return jsonify({
        "category": category,
        "response": response,
        "chat_history": history_str
    })
