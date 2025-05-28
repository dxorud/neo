import openai

def response_from_ChatAI(user_content, r_num = 1):
    messages = [
        {"role": "user", "content": user_content},
    ]
    
    reponse = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=100,
        temperature=0.8,
        n = r_num
    )

    assisatant_replies = []

    for choice in response['choices']:
        assisatant_replies.append(choice['message']['content'])

    return assisatant_replies
res = response_from_ChatAI("대한민국 헌번 1조 1항은?")
print(res)     
