# Question 1: Print Numbers
# Get a number greater than 3 from user, if odd -> print odd numbers 1 to n,
# if even -> print even numbers from 2 to n

try:
    n = int(input("Enter a number greater than 3: "))  # get integer input from user

    if n <= 3:  # check if number is not greater than 3
        print("Error: Please enter a number greater than 3.")  # show error message
    elif n % 2 != 0:  # check if the number is odd
        odd_numbers = list(range(1, n + 1, 2))  # create list of odd numbers from 1 to n
        print("Odd numbers from 1 to", n, ":", odd_numbers)  # print the odd numbers
    else:  # number is even
        even_numbers = list(range(2, n + 1, 2))  # create list of even numbers from 2 to n
        print("Even numbers from 2 to", n, ":", even_numbers)  # print the even numbers

except ValueError:  # handle non-integer input
    print("Error: Invalid input. Please enter a valid integer.")  # show appropriate error message
