# Question 2: Vowel Counter
# Receive a string from user and count the vowels (a, e, i, o, u),
# case-insensitive using a function to convert input to lowercase

def to_lowercase(text):
    """Convert all characters in a string to lowercase."""
    return text.lower()  # use built-in lower() method to convert all chars to lowercase

text = input("Enter a string: ")  # get string input from user
text = to_lowercase(text)  # call the function to convert input to lowercase

vowels = "aeiou"  # define vowel characters (only lowercase needed now)
count = 0  # initialize counter to zero

for char in text:  # iterate over each character in the converted string
    if char in vowels:  # check if the character is a vowel
        count += 1  # increment the counter

print("Number of vowels:", count)  # display the total vowel count
