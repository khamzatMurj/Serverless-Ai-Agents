
from agent_controller import AgentController
import boto3
import os 
import json 

agent_controller = AgentController()

def lambda_handler(event: dict, context) -> dict:
    try:
        # Parse the request body
        body = json.loads(event.get('body', '{}'))

        # Validate that body matches the expected DTO structure
        # Expected: {"input": {"messages": [{"role": "user", "content": "..."}]}}
        if not isinstance(body, dict) or "input" not in body:
            raise ValueError("Request body must contain 'input' field.")
        if not isinstance(body["input"], dict) or "messages" not in body["input"]:
            raise ValueError("'input' must contain 'messages' field.")
        if not isinstance(body["input"]["messages"], list):
            raise ValueError("'messages' must be a list.")
        for message in body["input"]["messages"]:
            if not isinstance(message, dict):
                raise ValueError("Each message must be a dictionary.")
            if "role" not in message or "content" not in message:
                raise ValueError("Each message must contain 'role' and 'content' fields.")
        
        # Get the response from the agent controller
        response = agent_controller.get_response(body)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response)
        }
    except Exception as e:
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }