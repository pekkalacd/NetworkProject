import re

math_calc = input("Please enter a basic math calculation as a string: ")
if not re.match("^[0-9\+\-\*\/\ \(\)]*$", math_calc):
    print ("Error! Invalid input")
else:
    print("Your basic math calculation is "+ math_calc)
