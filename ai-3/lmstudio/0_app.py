from openai import OpenAI

LM_STUDIO_SERVE_URL = 'http://localhost:1234/v1'

client = OpenAI(base_url=LM_STUDIO_SERVE_URL, api_key='lm-studio')

model_name = "lama3.2"

try:
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'What is the meaning of life?'}
        ],
        temperature = 0.7,
        max_tokens = 300,
    )

    print(completion.choices[0].message.content)

except Exception as e:
    print(f'An error occurred: {e}')
    print('Please check the LM Studio server is running, accessible at the specified url, and a model is loaded.')