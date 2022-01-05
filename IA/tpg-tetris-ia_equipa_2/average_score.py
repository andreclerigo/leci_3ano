with open('score.txt', 'r') as f:
    l = f.readlines()

score = 0

for x in l:
    score += int(x[:-1])

print(score / len(l))