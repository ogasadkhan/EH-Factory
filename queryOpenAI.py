from APIcallingfunc import *
import openai
import json

# Load API configurations
with open("new.json", "r") as f:
    data = json.load(f)

intents = data["API_INTENTS"]

                                # Define function to query OpenAI #
def call_openai(system_message, prompt):
    # Prepare the messages payload
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    try:
        # Query OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        # Extract the response content
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        # Handle API errors
        return f"An error occurred while processing your query: {e}"


#                                     #  # # Agent 1 - Refine User Query # # #
# def refine_query():
#     print("Agent 1 - Refine Query called")
#     query = input("Enter your question: ")
#     # Define system message for the refinement agent
#     sys_msg = """You are a query refinement agent of a chatbot that calls APIs dynamically. Your job is to take user queries, remove ambiguities, and make them concise and clear according to the APIs. 
#         If the query is irrelevant or ambiguous, politely ask the user to clarify or provide more relevant details. 
#         If the query is a general greeting like 'hi', 'hello', or 'how are you', return "general_prompt". 
#         If the query is not general then refine the query and return the refined query according to APIs.
#         Some APIs are 
#     Here are APIs:
#     {intents}
#     1. send_notification
#     return "send_notification" when the user prompt is like these: "Send notification", "Send message to this token", "Send alert", "Notify device", "Alert the user", "Push notification"
#     2. get_all_new_requests
#     return "get_all_new_requests" when the user prompt is like these: "Get all new requests", "Show me all new orders", "Retrieve new requests", "Fetch new orders", "Get the latest requests"
#     3. get_token
#     return "get_token" when the user prompt is like these: "Get new token", "Fetch API token", "Retrieve token", "Generate new token" 
#     4. login
#     return "login" when the user prompt is similar to these: "login with customer email abc.xyz@example.com" or login with merchant email abc.xyz@example.com"
#     """

#     res = call_openai(sys_msg, query)
#     print("Agent 1 - Refine Query response:", res)
#     if res == "general_prompt":
#         ask_proper_question(query)
#     else:
#         if res == "send_notification":
#             response = call_send_notification(query)
#         elif res == "get_all_new_requests":
#             response = call_get_all_new_requests(query)
#         elif res == "get_token":
#             response = call_get_token()
#         elif res == "login":
#             response = call_login(query)
#         else:
#             process_query(query, res)
#             # return res




#                                     #  # # Agent 2 - Ask Proper Question # # #
# def ask_proper_question(query):
#     print("Agnet 2 - Ask Proper Query called")
#         # Define system message for the refinement agent
#     sys_msg = """You are a helpful assistant, and the user has provided a general prompt. Ask him to send a proper question. Make sure your tone is polite and helpful."""
#     print(call_openai(sys_msg, query))
#     print("Agent 2 - Ask Proper Query response:", call_openai(sys_msg, query))
#     refine_query()


#                                     #  # # Agent 3 - Process the Query # # #
# def process_query(query, res):
#     print("Agent 3 - Process Query called")
#     # Define system message for the refinement agent
#     sys_msg = """You have knowledge of APIs and their intents. Check the user prompt and select the relevant API. 
#     Here are APIs:
#     {intents}
#     1. send_notification
#     return "send_notification" when the user prompt is like these: "Send notification", "Send message to this token", "Send alert", "Notify device", "Alert the user", "Push notification"
#     2. get_all_new_requests
#     return "get_all_new_requests" when the user prompt is like these: "Get all new requests", "Show me all new orders", "Retrieve new requests", "Fetch new orders", "Get the latest requests"
#     3. get_token
#     return "get_token" when the user prompt is like these: "Get new token", "Fetch API token", "Retrieve token", "Generate new token"
#     4. login
#     return "login" when the user prompt is similar to these: "login with customer email abc.xyz@example.com" or login with merchant email abc.xyz@example.com" 
#     """

#     res = call_openai(sys_msg, res)
#     print("Agent 3 - Process Query response:", query, res)
#     predicted_tag = res

#     if predicted_tag == "send_notification":
#         response = call_send_notification(query)
#     elif predicted_tag == "get_all_new_requests":
#         response = call_get_all_new_requests(query)
#     elif predicted_tag == "get_token":
#         response = call_get_token()
#     elif predicted_tag == "login":
#         response = call_login(query)
#     else:
#         response = {"error": "Intent not recognized"}
#     print ("API called", response)




# # # Agent 1 - Refine User Query # # #
def refine_query():
    print("Agent 1 - Refine Query called")
    query = input("Enter your question: ").strip()
    
    # Define system message for the refinement agent
    sys_msg = """You are a query refinement agent for a chatbot that dynamically calls APIs. 
    Your task is to take user queries, remove ambiguities, and make them concise and clear according to the APIs. 
    If the query is irrelevant, ambiguous, or a general greeting, respond appropriately:
    - General greetings like 'hi', 'hello', or 'how are you': return 'general_prompt'.
    - Refine the query and return the relevant intent based on the following APIs:
    {intents}
    1. send_notification
    Return 'send_notification' for queries like: 'Send notification', 'Send message to this token', 'Send alert', 'Notify device', 'Alert the user', 'Push notification'.
    2. get_all_new_requests
    Return 'get_all_new_requests' for queries like: 'Get all new requests', 'Show me all new orders', 'Retrieve new requests', 'Fetch new orders', 'Get the latest requests'.
    3. get_token
    Return 'get_token' for queries like: 'Get new token', 'Fetch API token', 'Retrieve token', 'Generate new token'.
    4. login
    Return 'login' for queries like: 'Login with customer email abc.xyz@example.com' or 'Login with merchant email abc.xyz@example.com'.
    """

    try:
        res = call_openai(sys_msg, query)
        print("Agent 1 - Refine Query response:", res)

        if res == "general_prompt":
            ask_proper_question(query)
        else:
            process_query(query, res)
    except Exception as e:
        print("Error in refine_query:", str(e))
        ask_proper_question(query)


# # # Agent 2 - Ask Proper Question # # #
def ask_proper_question(query):
    print("Agent 2 - Ask Proper Question called")
    
    # Define system message to prompt user for clarification
    sys_msg = """You are a helpful assistant. The user provided a general or unclear prompt. 
    Politely ask them to send a specific and relevant query. Make sure your tone is polite and encouraging."""
    
    try:
        response = call_openai(sys_msg, query)
        print("Agent 2 - Ask Proper Question response:", response)
        refine_query()
    except Exception as e:
        print("Error in ask_proper_question:", str(e))


# # # Agent 3 - Process the Query # # #
def process_query(query, res):
    print("Agent 3 - Process Query called")
    
    # Define system message for processing the query
    sys_msg = """You understand the available APIs and their intents. Based on the refined user query, select the correct API. 
    Return the intent name or indicate if the query is not relevant to any API.
    APIs:
    {intents}
    1. send_notification
    2. get_all_new_requests
    3. get_token
    4. login
    """

    try:
        predicted_tag = res
        print("Agent 3 - Process Query response:", query, predicted_tag)
        
        if predicted_tag == "send_notification":
            response = call_send_notification(query)
        elif predicted_tag == "get_all_new_requests":
            response = call_get_all_new_requests(query)
        elif predicted_tag == "get_token":
            response = call_get_token()
        elif predicted_tag == "login":
            response = call_login(query)
        else:
            response = {"error": "Intent not recognized"}

        print("API Response:", response)
    except Exception as e:
        print("Error in process_query:", str(e))
