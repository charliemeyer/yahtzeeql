import random
from strategies.scores import strategies, final_score, get_score_for_category
import sys

import strategies.human_strategy as human_strategy
import strategies.random_ai as random_strategy
import strategies.all_yahtzee as all_yahtzee_strategy
import strategies.random_greedy_ai as random_greedy_strategy

quiet_mode = False

def log(*messages):
    if quiet_mode:
        return
    print(messages)

def roll(old_roll, keep_numbers):
    new_roll = []
    for i in range(5):
        if i < len(keep_numbers):
            # TODO: check if the keep number is actually legit
            new_roll.append(keep_numbers[i])
        else:
            new_roll.append(random.randint(1,6))
    return sorted(new_roll)



def show_scoreboard(scoreboard):
    categories = list(strategies.keys())

    for category in categories:
        if category in scoreboard:
            log(category, scoreboard[category])
        else:
            log(category, 0)
    log("num yahtzees", scoreboard["num_yahtzees"])

def run_game(scoreboard, available_categories, strategy):
    user_roll = []
    keep_numbers = []
    while len(available_categories) > 0:
        for _ in range(3):
            user_roll = roll(user_roll, keep_numbers)
            log(" ".join([str(r) for r in user_roll]))
            keep_numbers = strategy.get_keep_numbers(user_roll)
            if (len(keep_numbers) == 5):
                break
        log("final roll:", " ".join([str(r) for r in user_roll]))
        for category in available_categories:
            (score, is_yahtzee) = get_score_for_category(category, user_roll, scoreboard)
            if is_yahtzee:
                log(category, score, "YAHTZEE!")
            else:
                log(category, score)
        chosen_category = strategy.get_category_choice(available_categories, user_roll, scoreboard)
        (score, is_yahtzee) = get_score_for_category(chosen_category, user_roll, scoreboard)
        scoreboard[chosen_category] = score
        if is_yahtzee:
            scoreboard["num_yahtzees"] += 1
        # remove the category from the list of available categories
        available_categories.remove(chosen_category)
        user_roll = []
        keep_numbers = []
        # clear screen
        log("\033c")
        log("current scoreboard: ")
        show_scoreboard(scoreboard)
        log("\033c")
    return final_score(scoreboard)

def main():
    global quiet_mode

    strategy = None
    strategy_choice = input("What strategy?" )
    if strategy_choice == "human":
        strategy = human_strategy
    if strategy_choice == "random":
        strategy = random_strategy
    if strategy_choice == "all_yahtzee":
        strategy = all_yahtzee_strategy
    if strategy_choice == "random_greedy":
        strategy = random_greedy_strategy
    
    num_runs = int(input("how many runs"))
    if num_runs > 1:
        quiet_mode = True

    sum_scores = 0
    for i in range(num_runs):
        available_categories = list(strategies.keys())
        scoreboard = {"num_yahtzees": 0}
        score = run_game(scoreboard, available_categories, strategy)
        sum_scores += score
        print("score", score)
        if not quiet_mode:
            input("press any key to continue")
        log("THE GAME IS OVER!")
        show_scoreboard(scoreboard)
        log("final score:", score)
    print("average score", sum_scores / num_runs)

main()