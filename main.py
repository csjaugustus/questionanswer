from random import choices, choice
import json

with open("wordbank.txt", encoding="utf-8") as f:
	lines = [l.strip() for l in f]

wordbank = {}
for l in lines:
	question, answer = l.split(";")
	wordbank[question] = answer

#load save file if any
try:
	with open("savedfile.json") as f:
		saved_data = json.load(f)

	if len(saved_data) != len(wordbank):
		new_dict = {}
		for q in wordbank:
			if q in saved_data:
				new_dict[q] = saved_data[q]
			else:
				new_dict[q] = 1
		diff = set(saved_data) ^ set(new_dict)
		print(f"Differences between new word bank and saved data:\n{diff}\n")
		saved_data = new_dict

	if sum(saved_data.values())==len(saved_data):
		weighted = False
	else:
		weighted = True

except FileNotFoundError:
	saved_data = {}
	for k in wordbank:
		saved_data[k] = 1
	with open("savedfile.json", "w") as f:
		json.dump(saved_data, f)
	weighted = False

#game
while True:
	game_wordbank = [q for q in wordbank]
	total_q = len(game_wordbank)
	streak = 0

	if not weighted:
		while game_wordbank:
			print(f"Question {total_q-len(game_wordbank)+1}/{total_q}")
			question = choice(game_wordbank)
			answer = wordbank[question]
			user_input = input(question + "\n")
			if user_input.lower() == answer.lower():
				print("Correct!\n")
				game_wordbank.remove(question)
				if saved_data[question] >= 3:
					saved_data[question] -= 2
				streak += 1
				if streak >= 3:
					print(f"{streak} in a row!\n")
			else:
				print(f"Wrong! The answer was '{answer}'.\n")
				saved_data[question] += 10
				streak = 0

		weighted = True

	else: 
		weights = [saved_data[q] for q in game_wordbank]
		while game_wordbank:
			print(f"Question {total_q-len(game_wordbank)+1}/{total_q}")
			question = choices(game_wordbank, weights, k=1)[0]
			answer = wordbank[question]
			user_input = input(question + "\n")
			if user_input.lower() == answer.lower():
				print("Correct!\n")
				indx = game_wordbank.index(question)
				game_wordbank.remove(question)
				weights.pop(indx)
				if saved_data[question] >= 3:
					saved_data[question] -= 2
				streak += 1
				if streak >= 3:
					print(f"{streak} in a row!\n")
			else:
				print(f"Wrong! The answer was '{answer}'.\n")
				saved_data[question] += 10
				streak = 0


	with open("savedfile.json", "w") as f:
		json.dump(saved_data, f, indent=4)

	stats = [(q, saved_data[q]) for q in saved_data]
	stats.sort(key=lambda x:x[1], reverse=True)
	with open("stats.txt", "w", encoding="utf-8") as f:
		for q,a in stats:
			f.write(f"{q} Points: {a}\n")

	input("Game Over. Enter to start another round.")

