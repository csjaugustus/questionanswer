from random import choices, choice
import json
import os

cwd = os.getcwd()
path1 = os.path.join(cwd, "Saved Data Files")
path2 = os.path.join(cwd, "Word Bank Files")
path3 = os.path.join(cwd, "Stats Files")
if not os.path.exists(path1):
	os.mkdir(path1)
if not os.path.exists(path2):
	os.mkdir(path2)
if not os.path.exists(path3):
	os.mkdir(path3)

filename = input("Name of word bank txt file (without file extension):\n")
wordbank_file =  f"Word Bank Files\\{filename}.txt"
saveddata_file = f"Saved Data Files\\{filename}.json"
stats_file = f"Stats Files\\{filename}.txt"

try:
	with open(wordbank_file, encoding="utf-8") as f:
		lines = [l.strip() for l in f]
except FileNotFoundError:
	print(f"No file named '{filename}.txt' in the word bank folder.")
	exit()

wordbank = {}
for l in lines:
	question, answer = l.split(";")
	wordbank[question] = answer

#load save file if any
try:
	with open(saveddata_file) as f:
		saved_data = json.load(f)

	if len(saved_data) != len(wordbank):
		new_dict = {}
		for q in wordbank:
			if q in saved_data:
				new_dict[q] = saved_data[q]
			else:
				new_dict[q] = 1
		diff = list(set(saved_data) ^ set(new_dict))
		additions = []
		removals = []
		for x in diff:
			if x in saved_data:
				removals.append(x)
			else:
				additions.append(x)
		if additions:
			additions_str = "\n".join(x for x in additions)
			print(f"The following additions were made:\n{additions_str}\n")
		if removals:
			removals_str = "\n".join(x for x in removals)
			print(f"The following removals were made:\n{removals_str}\n")

		saved_data = new_dict

	if sum(saved_data.values())==len(saved_data):
		weighted = False
	else:
		weighted = True

except FileNotFoundError:
	saved_data = {}
	for k in wordbank:
		saved_data[k] = 1
	with open(saveddata_file, "w") as f:
		json.dump(saved_data, f, indent=4)
	weighted = False

if weighted:
	message = "Saved data found."
else:
	message = "No saved data found."
#game
input(f"\n{message}\nEnter to start.")
print("========== START ==========\n")
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


	with open(saveddata_file, "w") as f:
		json.dump(saved_data, f, indent=4)

	stats = [(q, saved_data[q]) for q in saved_data]
	stats.sort(key=lambda x:x[1], reverse=True)
	with open(stats_file, "w", encoding="utf-8") as f:
		for q,p in stats:
			f.write(f"Points: {p} {q} {wordbank[q]} \n")

	input("Game Over. Enter to start another round.")

