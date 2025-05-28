from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(k=2, eturn_messages=True)
memory.save_context({"input": "안녕"}, {"output": "무슨 일이야?"})
memory.save_context({"input": "배고파"}, {"output": "나도"})
memory.save_context({"input": "밥 먹자"}, {"output": "응, 그러자"})

print(memory.load_memory_variables({}))