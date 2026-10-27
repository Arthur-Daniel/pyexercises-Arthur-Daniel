"""Exercise 4.1 — Reordering without losing the original (homework)

WHAT THE PROGRAM MUST DO
    Starting from the list you built in exercise 4.0, display it in four different
    orders, and prove at the end that the original list has not been damaged.

ANSWER THESE FIRST, in comments at the top of your file
    1. What goes in?
    2. What happens to it?
    3. What comes out?
    4. Which four orders did you choose, and in which of them is your original list
       modified rather than copied?

WHAT THE AI CANNOT KNOW
    That your original must survive. Some ways of reordering a list change it in place,
    others return a new one. Find out which is which, and say so in your comments.
    That distinction is the entire exercise.

CHECK IT YOURSELF
    The last line of your program must display the original list. Compare it, item by
    item, with what you wrote in 4.0. If it has moved, your program is wrong even
    though it ran.

DELIVERABLE
    This file, with your comments and your code.
"""

# 1. In:
# 2. Process:
# 3. Out:
# 4. My four orders, and which ones modify the original:


# Your code below
 
# The list from exercise 4.0 (monthly budgets in euros)
budgets = [1000, 900, 100, 700, 800, 600, 200, 300, 400, 500]
print("Original list:", budgets)
 
# Order 1: smallest to biggest (new list)
print("1. Smallest to biggest:", sorted(budgets))
 
# Order 2: biggest to smallest (new list)
print("2. Biggest to smallest:", sorted(budgets, reverse=True))
 
# Order 3: original order turned around (we reverse a copy)
reversed_budgets = budgets.copy()
reversed_budgets.reverse()
print("3. Original order turned around:", reversed_budgets)
 
# Order 4: alphabetical order, numbers compared as text (new list)
print("4. Alphabetical order:", sorted(budgets, key=str))
 
# Last line: proof that the original list has not changed
print("Original list at the end:", budgets)