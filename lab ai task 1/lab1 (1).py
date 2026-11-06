def symbolic(score, complete):
    return "Review" if complete and score >= 70 else "Hold"

def threshold(probability):
    return "Review" if probability >= 0.70 else "Hold"

def screen(score, complete, fee_paid, letter_done):
    if score >= 70 and complete and fee_paid and letter_done:
        return "Review"
    return "Hold"

print("note: all thresholds are synthetic lab assumptions, not real policy")
print("case | symbolic | threshold | disagreement")
for name, score, complete, probability in [
    ("complete_high", 82, True, 0.81),
    ("complete_low", 68, True, 0.74),
    ("incomplete_high", 91, False, 0.88),
    ("boundary", 70, True, 0.70),
]:
    a, b = symbolic(score, complete), threshold(probability)
    print(name, a, b, a != b, sep=" | ")

print("modified rule tests: input, expected, actual, reason")
for (score, complete, fee_paid, letter_done), expected, reason in [
    ((82, True, True, True), "Review", "all four conditions pass"),
    ((85, True, False, True), "Hold", "fee not paid"),
    ((88, True, True, False), "Hold", "recommendation letter missing"),
    ((70, True, True, True), "Review", "score exactly at the 70 boundary"),
]:
    actual = screen(score, complete, fee_paid, letter_done)
    print("input:", (score, complete, fee_paid, letter_done))
    print("expected:", expected, "| actual:", actual, "| reason:", reason)
    print("match:", actual == expected)
