# Name: Arthur DANIEL
# Group: A
#
# FEATURE I CHOSE: (d) Difficulty
# Why: it is the simplest one for me to explain. The player picks easy (15,000 EUR)
# or hard (6,000 EUR) at the start, and only the starting budget changes.
#
# 1. What goes in?
#    The file scenarios_A.csv. The separator is a comma. It has 14 columns:
#    ID, Scenario, OptionA, OptionB, OptionC, BudgetA, BudgetB, BudgetC,
#    ReputationA, ReputationB, ReputationC, FeedbackA, FeedbackB, FeedbackC.
#    Everything is read as text. The numbers are whole numbers, and a negative number
#    starts with "-" (for example -800), so I turn them into int myself.
#    The texts that contain a comma are inside quotes, the csv module handles that.
#    To find the impact of option B: BudgetB (column 6), ReputationB (column 9),
#    FeedbackB (column 12). The player also types a name, a difficulty and A, B or C.
#
# 2. What happens? (one day)
#    1. Take the next scenario from the shuffled list
#    2. Show the day number, both gauges, the situation and options A, B, C
#    3. Ask for A, B or C, and ask again until the answer is valid
#    4. Apply the budget and reputation change (reputation stops at 100)
#    5. Show the feedback line and the changes
#    6. Save the day in the history
#    7. If budget or reputation is 0 or less: stop the game at once
#
# 3. What comes out?
#    At the end the player sees: fired (and why) or "Quarter survived!", the final
#    gauges, the score, the title, and the best and worst move of the game.
#    One line is added to results.csv, for example:
#    Arthur,6350,100,CMO Material,2026-11-17
#    (columns: name, budget, reputation, title, date)
#
# 4. What could go wrong, and what my program does
#    - The player types something else than A, B or C (d, empty line, space...):
#      I strip it, lower it, and ask again until it is a, b or c.
#    - The player types an empty name or a wrong difficulty: I ask again.
#    - The scenario file is missing: I check with os.path.exists, I print a message
#      and the game stops cleanly instead of crashing.
#    - A row of the file is too short or a number is not a number: the short row is
#      skipped, and a bad number becomes 0 (function to_number).
#    - The reputation goes above 100: I cut it to 100.
#    - The budget or the reputation goes below zero: the game stops at that day.
#    - results.csv does not exist yet: I create it with its header line first.
#    - The file has less than 10 scenarios: I play only the ones I have.

import csv
import random
import os
from datetime import date

SCENARIO_FILE = "scenarios_A.csv"
RESULTS_FILE = "results.csv"
NUMBER_OF_DAYS = 10
START_REPUTATION = 50
MAX_REPUTATION = 100


# Ask the name and keep asking while the player types nothing
def ask_player_name():
    name = input("What is your name? ").strip()
    while name == "":
        name = input("Your name cannot be empty. What is your name? ").strip()
    return name


# Ask easy or hard, and return the starting budget of that difficulty
def choose_difficulty():
    answer = input("Difficulty: easy (15,000 EUR) or hard (6,000 EUR)? Type E or H: ").strip().lower()
    while answer not in ["e", "h", "easy", "hard"]:
        answer = input("Please type E or H: ").strip().lower()
    if answer == "e" or answer == "easy":
        return 15000
    return 6000


# Turn a text from the file into a whole number (negative numbers start with "-")
# If the text is not a number, we return 0 so the game does not crash
def to_number(text):
    text = text.strip()
    if text.lstrip("-+").isdigit():
        return int(text)
    return 0


# Read the scenario file and return a list of scenarios
# One scenario = (situation, option_a, option_b, option_c)
# One option = (text, budget_change, reputation_change, feedback)
def load_scenarios(filename):
    scenarios = []
    if not os.path.exists(filename):
        return scenarios
    with open(filename, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader, None)  # first line = column names, we do not play it
        for row in reader:
            if len(row) < 14:
                continue  # a broken row: we skip it
            option_a = (row[2], to_number(row[5]), to_number(row[8]), row[11])
            option_b = (row[3], to_number(row[6]), to_number(row[9]), row[12])
            option_c = (row[4], to_number(row[7]), to_number(row[10]), row[13])
            scenarios.append((row[1], option_a, option_b, option_c))
    return scenarios


# Write a number with its sign: 20 gives "+20", -20 gives "-20"
def format_change(number):
    if number > 0:
        return "+" + str(number)
    return str(number)


# Show one day: number, gauges, situation and the three options
def show_day(day, budget, reputation, scenario):
    situation, option_a, option_b, option_c = scenario
    print()
    print("--- Day", day, "---")
    print("[Budget:", budget, "EUR | Reputation:", str(reputation) + "/100]")
    print(situation)
    print("  A:", option_a[0])
    print("  B:", option_b[0])
    print("  C:", option_c[0])


# Ask A, B or C until the answer is valid, and return the option (a tuple)
def ask_choice(scenario):
    choice = input("Your choice (A, B or C): ").strip().lower()
    while choice not in ["a", "b", "c"]:
        choice = input("Please type A, B or C: ").strip().lower()
    if choice == "a":
        return scenario[1]
    elif choice == "b":
        return scenario[2]
    return scenario[3]


# Apply the option to the gauges and return the NEW budget and reputation (a tuple)
def apply_choice(budget, reputation, option):
    text, budget_change, reputation_change, feedback = option  # unpack the tuple
    budget = budget + budget_change
    reputation = reputation + reputation_change
    if reputation > MAX_REPUTATION:
        reputation = MAX_REPUTATION
    return budget, reputation


# Return the reason why the player is fired, or "" if the player is still in the game
def get_fired_reason(budget, reputation):
    if budget <= 0 and reputation <= 0:
        return "your budget and your reputation both hit zero"
    elif budget <= 0:
        return "your budget hit zero"
    elif reputation <= 0:
        return "your reputation hit zero"
    return ""


# Final score, only used when the player survives
def compute_score(budget, reputation):
    return reputation + budget // 200


# Return the title that goes with the score
def get_title(score):
    if score < 95:
        return "Eternal Intern"
    elif score < 120:
        return "Growth Hacker"
    elif score < 140:
        return "CMO Material"
    return "Viral Legend"


# History = list of tuples (reputation_change, day, option_text)
# Python compares tuples starting with the first element, so max() gives the biggest
# reputation change (best move) and min() the smallest (worst move)
def find_best_and_worst(history):
    best_move = max(history)
    worst_move = min(history)
    return best_move, worst_move


# Add one line to results.csv (and write the header line if the file is new)
def save_result(name, budget, reputation, title):
    file_is_new = not os.path.exists(RESULTS_FILE) or os.path.getsize(RESULTS_FILE) == 0
    with open(RESULTS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file_is_new:
            writer.writerow(["name", "budget", "reputation", "title", "date"])
        writer.writerow([name, budget, reputation, title, str(date.today())])


# Play the days one by one and return the final gauges and the history
def play_game(scenarios, budget, reputation):
    history = []
    random.shuffle(scenarios)  # a different order every game
    number_of_days = min(NUMBER_OF_DAYS, len(scenarios))
    for day in range(1, number_of_days + 1):
        scenario = scenarios[day - 1]
        show_day(day, budget, reputation, scenario)
        option = ask_choice(scenario)
        budget, reputation = apply_choice(budget, reputation, option)
        print(option[3])  # the feedback line
        print("Budget", format_change(option[1]), "EUR, Reputation", format_change(option[2]))
        history.append((option[2], day, option[0]))
        if get_fired_reason(budget, reputation) != "":
            break  # game over: the game stops at once
    return budget, reputation, history


# Show the end of the game: result, title, best and worst move
# and return the title so we can save it
def show_ending(name, budget, reputation, history):
    print()
    print("==============================")
    reason = get_fired_reason(budget, reputation)
    if reason != "":
        title = "Fired"
        print("You are fired!", "Why:", reason + ".")
        print("Budget left:", budget, "EUR, reputation:", str(reputation) + "/100")
    else:
        score = compute_score(budget, reputation)
        title = get_title(score)
        print("Quarter survived!")
        print("Budget left:", budget, "EUR, reputation:", str(reputation) + "/100")
        print("Final score:", score)
    print(name + ", your title:", title)
    print()
    best_move, worst_move = find_best_and_worst(history)
    print("Best move:  day " + str(best_move[1]) + ', "' + best_move[2] + '" (' + format_change(best_move[0]) + ")")
    print("Worst move: day " + str(worst_move[1]) + ', "' + worst_move[2] + '" (' + format_change(worst_move[0]) + ")")
    return title


# Main part: put everything together
def main():
    print("SURVIVE THE QUARTER - Croissant Rocket")
    name = ask_player_name()
    scenarios = load_scenarios(SCENARIO_FILE)
    if len(scenarios) == 0:
        print("I cannot find any scenario in", SCENARIO_FILE, "- check that the file is in the same folder.")
        return
    budget = choose_difficulty()
    budget, reputation, history = play_game(scenarios, budget, START_REPUTATION)
    title = show_ending(name, budget, reputation, history)
    save_result(name, budget, reputation, title)
    print("Saved in", RESULTS_FILE)


main()