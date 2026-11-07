from guided_chatbot import build_bot, reply

engine = build_bot()

assert "it_help.txt" in reply(engine, "How do I reset my password?")
assert reply(engine, "") == "Please enter a question."
assert "No matching FAQ" in reply(engine, "volcano geology")
assert "Possible matches" in reply(engine, "password recovery")

print("FAQ behaviour checks passed.")
print("\nExample exact answer:")
print(reply(engine, "How do I reset my password?"))
print("\nExample suggestion:")
print(reply(engine, "password recovery"))
print("\nExample empty input:")
print(reply(engine, ""))
print("\nExample unsupported input:")
print(reply(engine, "volcano geology"))
