g = {"S": [("A", 1), ("B", 4)], "A": [("C", 2)], "B": [("G", 5)], "C": [("G", 3)], "G": []}
h = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

def a(s, t, h):
    f = [(h[s], 0, s, [s])]
    b = {s: 0}
    d = []
    while f:
        f.sort()
        _, c, n, p = f.pop(0)
        if c != b[n]:
            continue
        d.append(n)
        if n == t:
            return c, p, d
        for x, w in g[n]:
            nc = c + w
            if nc < b.get(x, 999):
                b[x] = nc
                f.append((nc + h[x], nc, x, p + [x]))

print("A*:", a("S", "G", h))
print("UCS:", a("S", "G", {k: 0 for k in h}))
h["C"] = 10
print("Overestimate:", a("S", "G", h))
