# Question 4: GPA Calculator
# Ask user for number of courses and grades, compute average,
# then convert to letter grade: A(18-20), B(15-17.99), C(12-14.99), F(0-11.99)

import time  # import time module for the sleep function

try:
    num_courses = int(input("Enter the number of courses: "))  # get total number of courses
except ValueError:  # handle non-integer input
    print("Error: Invalid input for number of courses.")
    exit()  # terminate program on invalid input

grades = []  # initialize empty list to hold grades

for i in range(num_courses):  # loop once per course
    try:
        grade = float(input(f"Enter grade for course {i + 1}: "))  # prompt user for each grade
    except ValueError:  # handle non-numeric grade input
        print("Error: Invalid grade input.")
        exit()

    if grade > 20:  # check if grade exceeds the maximum allowed value of 20
        print("Grade Invalid")  # notify user that the grade is invalid
        time.sleep(1)  # wait 1 second before exiting
        exit()  # terminate the program immediately

    grades.append(grade)  # append valid grade to the list

average = sum(grades) / len(grades)  # calculate the average of all entered grades

# convert numeric average to letter grade based on grading table
if 18 <= average <= 20:  # range for grade A
    letter = "A"
elif 15 <= average < 18:  # range for grade B
    letter = "B"
elif 12 <= average < 15:  # range for grade C
    letter = "C"
else:  # anything below 12 is grade F
    letter = "F"

print(f"Average: {average:.2f} -> Grade: \"{letter}\"")  # print average and corresponding letter grade
