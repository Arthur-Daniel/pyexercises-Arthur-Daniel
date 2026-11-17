"""Exercise 7.1 — Loading a file, cleaning it, saving the result (homework)

This is the direct rehearsal for the final exam. Session 8 starts with it.

WHAT THE PROGRAM MUST DO
    Load names.txt, clean what is inside, sort it by last name, and write the result to
    a new file. The original file must not be modified.

DO THIS BEFORE ANYTHING ELSE
    Open names.txt and read it with your eyes. Then write, in comments at the top of
    your file, everything that is wrong with it. There are at least four different
    problems. Find them yourself.

    This step is not optional and it is graded. An assistant cannot see your file.

ANSWER THESE, in comments, after the list of problems
    1. What goes in?
    2. What happens to it?  (one line per problem you found, and how you deal with it)
    3. What comes out?
    4. What does "sort by last name" mean when a line contains two words, and how do you
       know which one is the last name?

WHAT THE AI CANNOT KNOW
    The actual content of names.txt. If you paste this brief into an assistant without
    describing the file, it will write a program for a clean file, and that program will
    crash or produce nonsense on the real one.

    Describe the file to it. That description is the exercise.

CHECK IT YOURSELF
    Count the lines in names.txt, then in your output file. The numbers should differ,
    and you should be able to say exactly why. Then check the first and last name of
    your sorted list by hand.

DELIVERABLE
    This file, plus the output file your program produced.
"""

# What is wrong with names.txt (found by reading it, not by guessing):
# -
# -
# -
# -

# 1. In:
# 2. Process, problem by problem:
# 3. Out:
# 4. How I decide which word is the last name:


# Your code below

import os

INPUT_FILE = "names.txt"
OUTPUT_FILE = "names_clean.txt"


# Return the last name of a clean name: the last word of the line
def get_last_name(name):
    words = name.split()
    return words[-1]


# Read the file and return the list of clean names (no empty lines, no extra spaces,
# a capital on each word). The original file is only read.
def load_clean_names(filename):
    names = []
    with open(filename, encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line == "":
                continue  # empty line: nothing to keep
            names.append(line.title())
    return names


# Write the names in a new file, one per line
def save_names(filename, names):
    with open(filename, "w", encoding="utf-8") as file:
        for name in names:
            file.write(name + "\n")


if not os.path.exists(INPUT_FILE):
    print("I cannot find", INPUT_FILE, "- check that it is in the same folder.")
else:
    # count the lines of the original file, to compare with the output file
    with open(INPUT_FILE, encoding="utf-8") as file:
        lines_before = len(file.readlines())

    names = load_clean_names(INPUT_FILE)
    # sorted() returns a NEW list: my cleaned list is not changed
    sorted_names = sorted(names, key=get_last_name)
    save_names(OUTPUT_FILE, sorted_names)

    print("Lines in", INPUT_FILE + ":", lines_before)
    print("Lines in", OUTPUT_FILE + ":", len(sorted_names))
    print("Sorted names:")
    for name in sorted_names:
        print(" ", name)
        