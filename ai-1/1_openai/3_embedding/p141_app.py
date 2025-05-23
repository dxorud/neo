import openai

text = '이것은 테스트입니다.'

resopnse = openai.Embedding.create(
    input=text,
    model="text-embedding-ada-002",
)
print('-' * 50)
print(len(resopnse['data'][0]['embedding']))
print('-' * 50)
print(resopnse['data'][0]['embedding'])