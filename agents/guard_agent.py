

import os
from openai import OpenAI
from typing import List, Dict, Any
from agents.utils.utils import get_chatbot_response, get_embedding
from copy import deepcopy
import json
import dotenv
dotenv.load_dotenv()




class GuardAgent():
    def __init__(self) :
        # print(os.getenv("base_url"))
        self.client = OpenAI(
            base_url= os.getenv("base_url") ,
            api_key= os.getenv("api_key")
        )
        self.model_name = os.getenv("model")
    
    def get_response(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        messages = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menu items and coffee shop related questions.
            2. Ask questions about menu items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. ASk about recommendations of what to buy.

            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menu item.

            If the user's message is empty or Hello or contains no meaningful content, consider it decision not allowed but respond with an engaging prompt like: "Welcome to our coffee shop! I'd be happy to tell you about our menu items, location, hours, or help you place an order. What are you in the mood for today? Perhaps I can recommend something delicious!"

            Your output must be a structured JSON object in the following format. Each key and value must be surrounded by double quotes. Follow this format exactly:
            {

            "decision": "allowed" or "not allowed". Pick one of those, and only write the word.
            "message": Leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
            IMPORTANT: 
                -Do not include anything except this JSON object in your output. 
                -Do not include any explanations, text, markup, or <think> blocks outside the JSON. 
                -Output ONLY the JSON object and nothing else.
                -Output ONLY the JSON object and nothing else.
                -Output ONLY the JSON object and nothing else.
                -Output ONLY the JSON object and nothing else.
                

            """
        
        input_messages = [{"role": "system", "content": system_prompt}] + messages[-3:]
        print(f"inpt_msg____:____{json.dumps(input_messages, indent=4)}")

        chatbot_output = get_chatbot_response(self.client, self.model_name, input_messages)
        output = self.postprocess(chatbot_output)
        
        return output

    def postprocess(self,output):
        print("DEBUG guard chatbot_output:", output)
        output = json.loads(output)

        dict_output = {
            "role": "assistant",
            "content": output['message'],
            "memory": {"agent":"guard_agent",
                       "guard_decision": output['decision']
                      }
        }
        return dict_output

        

        
    
