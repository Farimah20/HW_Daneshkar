# Question 5: Reverse Sentence
# Receive a sentence and reverse the order of its words

sentence = input("Enter a sentence: ")  # get sentence input from user
words = sentence.split()  # split sentence into a list of individual words
reversed_words = words[::-1]  # reverse the list using Python slice notation
reversed_sentence = " ".join(reversed_words)  # rejoin reversed words into a single string

print("Reversed sentence:", reversed_sentence)  # display the final reversed sentence
