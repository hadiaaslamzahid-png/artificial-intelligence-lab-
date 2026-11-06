def minimax(scores, depth, index, is_max, count):
    if depth == 0:
        count[0] += 1
        return scores[index]

    left = minimax(scores, depth - 1, index * 2, not is_max, count)
    right = minimax(scores, depth - 1, index * 2 + 1, not is_max, count)

    if is_max:
        return max(left, right)
    return min(left, right)


def alpha_beta(scores, depth, index, is_max, alpha, beta, count, reverse=False):
    if depth == 0:
        count[0] += 1
        return scores[index]

    best = float("-inf") if is_max else float("inf")
    order = [1, 0] if reverse else [0, 1]

    for side in order:
        value = alpha_beta(
            scores, depth - 1, index * 2 + side, not is_max,
            alpha, beta, count, reverse
        )

        if is_max:
            best = max(best, value)
            alpha = max(alpha, best)
        else:
            best = min(best, value)
            beta = min(beta, best)

        if alpha >= beta:
            break

    return best


scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = 3

minimax_count = [0]
minimax_value = minimax(scores, depth, 0, True, minimax_count)

alpha_count = [0]
alpha_value = alpha_beta(
    scores, depth, 0, True, float("-inf"), float("inf"), alpha_count
)

reverse_count = [0]
reverse_value = alpha_beta(
    scores, depth, 0, True, float("-inf"), float("inf"),
    reverse_count, True
)

print("Minimax value:", minimax_value)
print("Minimax leaves:", minimax_count[0])
print("Alpha-Beta value:", alpha_value)
print("Alpha-Beta leaves:", alpha_count[0])
print("Reversed Alpha-Beta value:", reverse_value)
print("Reversed Alpha-Beta leaves:", reverse_count[0])
