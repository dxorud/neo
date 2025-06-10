import lmstudio as lms

model = lms.llm()

for fragment in model.respond("What is the meaning of life?"):
    print(fragment.content, end='', flush=True)

print()