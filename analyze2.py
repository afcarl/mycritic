import json
import operator
from random import shuffle, choice
import collections

movies = json.load(open('movies.json','r'))
critics = json.load(open('critics.json','r'))
critical = {}
for movie in movies:
	b = len(movies[movie]['bad'])
	g = len(movies[movie]['good'])
	if b == 0 or g == 0:
		continue
	num = b / (b+g)
	if num > 0.5:
		num = 1 - num
	critical[movie] = num * (b+g)


criticalMovies = []
sorted_x = sorted(critical.items(), key=operator.itemgetter(1), reverse=True)
for i in range(500):
	print(sorted_x[i])
	criticalMovies.append(sorted_x[i][0])
shuffle(criticalMovies)

agreeableCritics = []
answered = []
i = -1
while True:
	i += 1
	answer = input("Did you like %s? (y/n/s) " % criticalMovies[i])
	answered.append(criticalMovies[i])
	if answer == 'y':
		agreeableCritics += movies[criticalMovies[i]]['good']
	if answer == 'n':
		agreeableCritics += movies[criticalMovies[i]]['bad']
	counter=collections.Counter(agreeableCritics)
	bestCritics= counter.most_common(10)
	if len(bestCritics) == 0:
		continue
	bestCritic = bestCritics[0][0]
	print(bestCritics)

	if i % 10 == 0:
		moviePool = list(set(critics[bestCritic])-set(answered))
		if len(moviePool) > 0:
			criticsChoice = choice(moviePool)
			answer = input("Did you like %s? (y/n/s) " % criticsChoice)
			answered.append(criticsChoice)
			if answer == 'y':
				agreeableCritics += movies[criticalMovies[i]]['good']
			if answer == 'n':
				agreeableCritics += movies[criticalMovies[i]]['bad']
			counter=collections.Counter(agreeableCritics)
			bestCritics= counter.most_common(10)
			print(bestCritics)
