from flask import Blueprint
from Controllers.chat import getMasterAgentResponse

chat_r = Blueprint('chat_r', __name__) # creates a Blueprint object, which is Flask's way of organizing a group of related routes and other code.

chat_r.route('/chat', methods=['POST'])(getMasterAgentResponse)


