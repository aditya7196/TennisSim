
"""
__author__ = "Aditya Gadgil"
Python version = 3.9
This Tennis Sim uses two separate threads as players. Player 1 starts first. The scoring system is a random number
generator that generates numbers either 0 or 1. If 0, player_1 wins the point. If 1, player_2 wins the point. Whoever
wins the last point in the serve, gets to serve next. When one of them reaches score 11 without a tie at 10-10,
the game ends with winner being the player who got the 11th point. When 10-10 tie is reached, player who gets the
two-point lead wins, otherwise game continues until their scores reach 20. At 20-20 tie the player who wins the first
point is declared the winner. (It is also possible to implement without threading - But I wanted the two players -
threads to actually play the game.) """

import collections
import random
import threading
import time

# Minimum winning score
MIN_WINNING_SCORE = 11

# Maximum winning score
MAX_WINNING_SCORE = 21

# Tie score
TIE_SCORE = 10

# Player player_1
PLAYER_1 = "player_1"

# Player player_2
PLAYER_2 = "player_2"

# Decision MATCH_END
MATCH_END = "match_end"

# Decision TEN_TIE
TEN_TIE = "ten_tie"


def serve():
    """
    Function to randomly award the point to a player.
    It fulfills the function that if even is returned player_1 gets the point. and if odd, player_2.
    :return:
    """
    if random.randint(0, 1) == 0:
        return PLAYER_1
    return PLAYER_2


# Utility function to return the player name from the score they have attained
def get_player_from_score(score, score_card):
    """
    from the keys in score_card, finds out which key the given value belongs to.
    :param score:
    :param score_card:
    :return:
    """
    return str(((list(score_card.keys()))[list(score_card.values()).index(
        score)]))


# Simulates one set. Each player (Thread) enters it, plays their serve, and depending upon the score, decisions are
# taken.
def simulate_set(match_decisions, score_card):
    """
    PLayer checks if match is ended first. If the 'tied at ten' conditions isn't in place, player goes on and plays
    their two serves. If minimum winning score is reached, player gets out, and thread exits. If tie occurs,
    then the shared 'ten_tie' variable is set to True to let other player know that we're in ten-tie condition. After
    21 is attained or 2-point lead is attained, set ends. And the winner name is returned. :param match_decisions:
    :param match_decisions:
    :param score_card: :return:
    """
    tied_at_ten = match_decisions[TEN_TIE]
    match_ended = match_decisions[MATCH_END]

    if not match_ended:  # Because the second thread which waits for the event won't know if match ended or not
        print("serving: " + threading.current_thread().name.__str__())
        # Condition 1: Minimum score attainment win
        if not tied_at_ten:
            for i in range(2):
                winner = serve()
                score_card[winner] += 1
                winning_score = max(score_card[PLAYER_1], score_card[PLAYER_2])
                print("Point won by " + winner + " with score " + str(score_card[winner]))
                if score_card[PLAYER_1] == 10 and score_card[PLAYER_2] == 10:
                    match_decisions[TEN_TIE] = True  # Sets the ten_tie to true
                    print("Tie at 10-10.")
                    break  # Break here because we'll need to take different route of game in a ten-tie
                if winning_score >= MIN_WINNING_SCORE:
                    print("Set over. Winner is " + get_player_from_score(score=winning_score,
                                                                         score_card=score_card) + " with " + str(
                        winning_score) + " points")
                    match_decisions[MATCH_END] = True
                    break

        # Condition 2: Win after 10-10 tie. Either get a 2-point lead or attain a score of 21.
        if tied_at_ten:
            # In case of ten-tie players will have to strive for a two point lead to win the game until one of them
            # scores a 21, in which case, it's a game win.
            for i in range(2):
                winner = serve()
                score_card[winner] += 1
                winning_score = max(score_card[PLAYER_1], score_card[PLAYER_2])
                print("Point won by " + winner + " with score " + str(score_card[winner]))
                if abs(score_card[PLAYER_1] - score_card[PLAYER_2]) == 2:
                    print("Set over after tie at 10-10. Winner is {0} with score {1} ".format(
                        get_player_from_score(score=winning_score,
                                              score_card=score_card),
                        winning_score))
                    match_decisions[MATCH_END] = True
                    match_decisions[TEN_TIE] = False
                    break
                if score_card[winner] >= 21:
                    print("Set won after attaining 21 points by {0} ".format(get_player_from_score(
                        score=winning_score, score_card=score_card)))
                    match_decisions[MATCH_END] = True
                    break
        return winner


def player_1(event, match_decisions, score_card):
    """
    Thread player_1
    Doesn't wait for event so player_1 always goes first.
    Checks if match ended, if it is, exits.
    Checks if the serve is won by other player and sets the event letting player_2 serve.
    If won by themselves, goes on to serve.
    Waits.
    :param event:
    :param match_decisions:
    :param score_card:
    """
    while not match_decisions[MATCH_END]:
        winner = simulate_set(match_decisions=match_decisions, score_card=score_card)
        if match_decisions[MATCH_END]:
            break
        if winner is PLAYER_2:
            print("next serving: " + PLAYER_2)
            event.set()
            time.sleep(2)


def player_2(event, match_decisions, score_card):
    """
    Thread player_2.
    At start, waits for a point win.
    Then starts the serve, it they win, event is set for them to start new serve again.
    If player_1 wins, event is cleared for player_1 to take the serve.
    Waits.
    :param event:
    :param match_decisions:
    :param score_card:
    """
    while not match_decisions[MATCH_END]:
        event.wait()
        winner = simulate_set(match_decisions=match_decisions, score_card=score_card)
        if winner is PLAYER_1:
            print("next serving: " + PLAYER_1)
            event.clear()
            time.sleep(2)
        else:
            event.set()


def main():
    """
    main function.
    creates players and starts the game.
    After set end, sends them home.
    """
    # Score card to keep score
    score_card = collections.Counter()
    match_decisions = {MATCH_END: False, TEN_TIE: False}
    event = threading.Event()
    player_1_thread = threading.Thread(name=PLAYER_1, target=player_1, args=(event, match_decisions, score_card,))
    player_2_thread = threading.Thread(name=PLAYER_2, target=player_2, args=(event, match_decisions, score_card,))
    player_1_thread.start()
    player_2_thread.start()
    player_1_thread.join()
    player_2_thread.join()


if __name__ == "__main__":
    main()
