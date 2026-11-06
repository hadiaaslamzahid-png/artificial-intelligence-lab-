from lab2_model import ClassroomAgent

agent = ClassroomAgent()
percepts = [(29, True), (29, True), (20, True),
            (26, True), (19, True), (29, False)]

print("Step | Previous | Percept     | Target | Command")
print("-" * 57)

for step, percept in enumerate(percepts, 1):
    previous = agent.previous_mode
    target, send_command = agent.act(*percept)
    result = "SEND" if send_command else "NO"
    print(f"{step:>4} | {str(previous):<8} | {str(percept):<11} | "
          f"{target:<6} | {result}")
