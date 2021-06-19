# Q & A Program

This program takes a txt file in which every line is written in "question;answer" format, and then prompts the user to answer all questions until all questions are correctly answered. Every question answered wrongly will reappear, and the program keeps track every time a mistake is made so as to determine which questions will more likely be picked first in the next round. "Points" will be assigned to wrong questions and those points will be deducted whenever the question is answered correctly. It is currently 10 points per wrong answer and 3 points deducted per correct answer, but that can easily be changed according to your needs.

After every round, a stats file will be generated in the "Stats Files" to show how many points each question has.

You can add any number of txt's in the "Word Bank Files" folder, and the program will prompt the user to pick which word bank to use every round. 

Example of how the txt should be formatted:

![image](https://user-images.githubusercontent.com/61149391/122638045-5af58600-d124-11eb-9c21-1c2b1850ae11.png)
