from random import choice

run_result = {
    0.5: [[0, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 0]],
    0.3: [[0, 0, 2, 0, 0, 0], [0, 2, 0, 0, 0, 0]],
    0.4: [[0, 0, 3, 0, 0, 0], [0, 3, 0, 0, 0, 0]],
}

sort = sorted(run_result.items(), reverse=True)

new_population = []
tournament_size = 2
for _ in range(20):
    competitors = []
    for _ in range(tournament_size):
        random_fitness = choice(sort)
        competitors.append((random_fitness[0], choice(random_fitness[1])))
    competitors.sort(reverse=True)
    new_population.append(competitors[0][1])

print(new_population)