class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


class StatefulClassroomAgent:
    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):
        if not occupied:
            target = "ECO"
        elif temp > 26:
            target = "COOL"
        elif temp < 20:
            target = "WARM"
        else:
            target = "IDLE"
        send = target != self.previous_mode
        self.previous_mode = target
        return target, send


percepts = [(29, True), (29, True), (20, True), (26, True), (19, True), (29, False)]

print("Reflex agent:")
agent = ClassroomAgent()
for step, percept in enumerate(percepts, 1):
    print(step, percept, "target mode", agent.act(*percept))

print("Stateful agent:")
model = StatefulClassroomAgent()
for step, percept in enumerate(percepts, 1):
    previous = model.previous_mode
    target, send = model.act(*percept)
    print(step, percept, "previous", previous, "target", target, "send", send)

print("Noisy sequence around 26C:")
noisy = [(26, True), (27, True), (26, True), (27, True)]
model2 = StatefulClassroomAgent()
for step, percept in enumerate(noisy, 1):
    previous = model2.previous_mode
    target, send = model2.act(*percept)
    print(step, percept, "previous", previous, "target", target, "send", send)
