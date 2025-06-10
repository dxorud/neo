import lmstudio as lms

def dose_chat_fit_in_context(model: lms.LLM, chat: lms.Chat) -> bool:
    formatted = model.apply_prompt_template(chat)
    token_count = len(model.tokenize(formatted))
    context_length = model.get_context_legth()
    print(f'Token Count : {token_count}, Context Length : {context_length}')
    return token_count < context_length

model = lms.llm()

chat = lms.Chat.from_history({
    "messages" : [
        {"role": "system", "content": "You are a resident AI philosopher."},
        {"role": "user", "content": "What is the meaning of life?"}
    ]
})

print("Fir in Context : ", dose_chat_fit_in_context(model, chat))