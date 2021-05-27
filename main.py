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

	if len(saved_data) > len(wordbank):
		q_to_delete = []
		for q in saved_data:
			if q not in wordbank:
				q_to_delete.append(q)
		for q in q_to_delete:
			del saved_data[q]
		print(f"Saved data contains questions that were removed from word bank. Cleared the following:\n{'\n'.join(q_to_delete)}.")

	elif len(saved_data) < len(wordbank):
		q_to_add = []
		for q in wordbank:
			if q not in saved_data:
				q_to_add.append(q)
		for q in q_to_add:
			saved_data[q] = 0
		print(f"New questions found in word bank. Added the following to saved data:\n{'\n'.join(q_to_add)}.")

	weighted = True

except FileNotFoundError:
	saved_data = {}
	for k in wordbank:
		saved_data[k] = 0
	with open("savedfile.json", "w") as f:
		json.dump(saved_data, f)
	weighted = False

#game
while True:
	game_wordbank = [q for q in wordbank]

	if not weighted:
		while game_wordbank:
			question = choice(game_wordbank)
			game_wordbank.remove(question)
			answer = wordbank[question]
			user_input = input(question + "\n")
			if user_input.lower() == answer.lower():
				print("Correct!\n")
			else:
				print(f"Wrong! The answer was '{answer}'.\n")
				saved_data[question] += 1
		weighted = True

	else: 
		weights = [saved_data[q] for q in game_wordbank]
		while game_wordbank:
			question = choices(game_wordbank, weights, k=1)[0]
			game_wordbank.remove(question)
			answer = wordbank[question]
			user_input = input(question + "\n")
			if user_input.lower() == answer.lower():
				print("Correct!\n")
			else:
				print(f"Wrong! The answer was '{answer}'.\n")
				saved_data[question] += 1

	with open("savedfile.json", "w") as f:
		json.dump(saved_data, f)

