# Question 3: Create Dictionary
# Receive a string, count the frequency of each word, and store in a dictionary

text = input("Enter a string: ")  # get string input from user
words = text.split()  # split the string into a list of words by whitespace
word_freq = {}  # initialize an empty dictionary to store word frequencies

for word in words:  # iterate over each word in the list
    # capitalize first letter to match the expected output format
    key = word[0].upper() + word[1:] if word else word  # capitalize first letter of the word
    if key in word_freq:  # check if the word already exists in dictionary
        word_freq[key] += 1  # increment count if word already found
    else:
        word_freq[key] = 1  # add new word with count 1

print("Word frequency dictionary:", word_freq)  # display the resulting dictionary
