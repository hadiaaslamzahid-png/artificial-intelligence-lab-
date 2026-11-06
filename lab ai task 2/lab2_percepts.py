class ClassroomAgent:
    def act(self, temp, occupied):
        if not occupied:
            return "ECO"
        if temp > 26:
            return "COOL"
        if temp < 20:
            return "WARM"
        return "IDLE"


agent = ClassroomAgent()
percepts = [(29, True), (24, True), (29, False)]

for percept in percepts:
    print(percept, "->", agent.act(*percept))
