import random
import time

# CONFIG
inf_risk = 0.33  # CHANCE OF INFECTING AN ADJACENT PERSON (Must be between 0.01 and 1.0 to work!)
step_time = 2  # HOW LONG IN SECONDS BETWEEN EACH PROGRESSION STEP (This is how long you wait before seeing updates)
days_per_step = 5  # DAYS EACH STEP REPRESENTS
# TOTAL PEOPLE = ROWS * COLS
rows = 20
cols = 15
disease_duration = 21  # HOW LONG THE DISEASE LASTS
chance_of_death = 0.03  # CHANCE OF DYING BY THE END OF THE DISEASE DURATION (Must be between 0.01 and 1.0 to work!)

base = [[0 for i in range(rows)] for j in range(cols)]
v = {}
s = {}
dead = [0]


def infect(d, x, y):
    if (x, y) in v:
        return
    if x < 0 or x >= len(d) or y < 0 or y >= len(d[0]):
        return
    if d[x][y] >= 1:
        return
    if random.randint(1, 100) <= int(inf_risk * 100):
        d[x][y] = 1
        v[(x, y)] = 1
        s[(x, y)] = 0


def step(d):
    x = len(d)
    y = len(d[0])
    for i in range(x):
        for j in range(y):
            if (i, j) not in v and d[i][j] == 1:
                infect(d, i - 1, j)
                infect(d, i + 1, j)
                infect(d, i, j - 1)
                infect(d, i, j + 1)


def seed(d):
    x = len(d)
    y = len(d[0])
    seeds = random.randint(3, 6)
    for i in range(seeds):
        loc = (random.randint(0, x - 1), random.randint(0, y - 1))
        d[loc[0]][loc[1]] = 1
        s[(loc[0], loc[1])] = 0


def print_pop(d):
    for r in d:
        s = []
        for c in r:
            if c == 0:
                s.append('-')
            elif c == 1:
                s.append('X')
            elif c == 2:
                s.append('D')
            else:
                s.append('R')
        print(''.join(s))


def update_infections(d):
    to_delete = []
    for e in s.keys():
        s[e] += days_per_step
        if s[e] >= disease_duration:
            if random.randint(1, 100) <= int(chance_of_death * 100):
                d[e[0]][e[1]] = 2
                dead[0] += 1
            else:
                d[e[0]][e[1]] = 3
            to_delete.append(e)
    for key in to_delete:
        del s[key]


def check_finish(d):
    x = len(d)
    y = len(d[0])
    for i in range(x):
        for j in range(y):
            if d[i][j] == 1:
                return False
    return True


def count_infected(d):
    x = len(d)
    y = len(d[0])
    inf = 0
    for i in range(x):
        for j in range(y):
            if d[i][j] >= 1:
                inf += 1
    return inf


print("With current configuration each person has a " + str(inf_risk * 100) + '% chance of infecting a nearby person every ' + str(days_per_step) + ' days. Each new graph shown represents the passing of ' + str(days_per_step) + ' days and as you will see this is how COVID-19 will spread.\n- = not infected\nX = infected\nD = dead\nR = recovered\n\n')

time.sleep(10)
print('\a')

seed(base)
print("Day 0 - Initial people infected shown in X")
print_pop(base)

days = days_per_step
while True:
    print('\a')
    time.sleep(step_time)
    step(base)
    v.clear()
    print("Days passed: " + str(days))
    update_infections(base)
    days += days_per_step
    print_pop(base)

    if check_finish(base):
        inf = count_infected(base)
        print("\n\nOUTBREAK OVER\nTOTAL PEOPLE: " + str(rows * cols) + "\nINFECTED: " + str(inf) + "\nDEAD: " + str(dead[0]) + "\nRECOVERED: " + str(inf - dead[0]))
        break
