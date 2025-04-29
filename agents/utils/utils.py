from agents.utils import pc

def get_chatbot_response(client, model, messages : list, temperature=0, max_tokens=1000, top_p=0.8):
    input_message = []
    for message in messages:
        input_message.append({"role": message['role'], "content": message['content']})

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=input_message,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
        )
        
        if completion is None or not hasattr(completion, 'choices') or len(completion.choices) == 0:
            print("API call failed or returned invalid response NULL")
            # return "Sorry, I couldn't process your request at this time."
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        # return "Sorry, I encountered an error while processing your request."



def get_embedding(text_input:list[str]):
        
    embed = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=text_input,
        parameters={'input_type':'passage', 'truncate':'END'}
    )   
    return embed


def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chatbot_response(client,model_name,messages)

    return response