import os
import random
import time

"""
Constants:
1. Roles breakdown (depending on number of players).

Global Variables:
1. policy tiles (6 liberal, 11 fascist) (don't need to restore/replenish: just draw according to the odds)
"""

# dictionary constant that associates the number of players with the distribution of Liberals and Fascists
# Key (int) = num_players
# Value (int): num_fascists, not including Hitler
ROLE_DISTRIBUTION = { 5: 1,
                      6: 1,
                      7: 2,
                      8: 2,
                      9: 3,
                      10: 3 }

REPLENISHED_POLICY_DECK = [ "Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist", "Fascist",
                "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist" ]

# global variable containing player roles, where index + 1 represents the Player #.
player_roles = []
# global variable  6 liberal, 11 fascist
policy_deck = [ "Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Liberal", "Fascist", "Fascist", "Fascist",
                "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist", "Fascist" ]
policy_boards = { "Liberal Policies": 0, "Fascist Policies": 0 }
curr_president = 0
curr_chancellor = 0
election_tracker = 0

def clear_console():
    """
    Helper Function: clears the console display. No return value.
    """
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def assign_roles() -> object:
    num_players = input("Type the number of players and press ENTER: ")
    # ensure there are 5 to 10 players
    while True:
        if num_players.isnumeric():
            num_players = int(num_players)
            if num_players in range(5, 10):
                break
            num_players = input("Invalid number of players. Game must be played with 5 to 10 players. Please "
                                "re-type a valid number of players and press ENTER: ")
        else:
            num_players = input("Invalid non-numeric input. Please re-type a valid number of players and press ENTER: ")

    global player_roles
    num_fascists = ROLE_DISTRIBUTION[num_players]

    # initially assign all players as Liberals (some to be overwritten)
    for i in range(num_players):
        player_roles.append("Liberal")

    # randomly assign Hitler
    hitler_index = random.randint(0, num_players - 1)
    player_roles[hitler_index] = "Secret Hitler"

    # randomly assign num_fascists Fascists
    for i in range(num_fascists):
        fascist_index = random.randint(0, num_players - 1)
        # ensure Hitler does not get overwritten
        while fascist_index == hitler_index:
            fascist_index = random.randint(0, num_players - 1)
        player_roles[fascist_index] = "Fascist (not Hitler)"

    # print roles
    input("Ready to receive your secret roles? Hand the computer to Player 1 and press ENTER to initiate the "
          "top-secret role reveal sequence.")
    print("Beginning role reveal sequence...")
    for i in range(len(player_roles)):
        player_number = i + 1
        print("------ FOR PLAYER " + str(player_number) + "'S EYES ONLY! ------" )
        input("Press ENTER to confirm you are Player " + str(player_number) + " and reveal your secret role.")
        print("Player " + str(player_number) + ", your secret role is " + player_roles[i] + ".")
        if player_number + 1 <= num_players:
            input("Press ENTER to obliterate this message, then pass the computer to Player "
                  + str(player_number + 1) + ".")
        else:
            input("Press ENTER to obliterate this message, then return the computer for group viewing.")
        clear_console()

    # start the game
    input("Press ENTER once everyone is ready to begin the game.")


def draw_policy_tile():
    global policy_deck
    # replenish policy deck if needed
    if len(policy_deck) < 3:
        policy_deck = REPLENISHED_POLICY_DECK
    # randomly draw a policy
    drawn_index = random.randint(0, len(policy_deck) - 1)
    return drawn_index


def draw_policy_tiles():
    """
    Randomly draws 3 Policy tiles from the Policy deck.
    Uses global variables: policy_deck.
    :return: Returns a dictionary containing the 3 policies drawn, numbered 1 to 3.
    """
    policies_drawn = {}
    global policy_deck
    for tile_num in range(1, 4):
        drawn_index = draw_policy_tile()
        # add drawn policy to policies_drawn dict
        policies_drawn[tile_num] = policy_deck[drawn_index]
        policy_deck.remove(policy_deck[drawn_index])

    print("President, step forward to draw three Policy tiles from the top of the Policy deck.")
    print("------ FOR THE PRESIDENT'S EYES ONLY! ------")
    input("Press ENTER to confirm you are the President, and that nobody else can see your screen.")
    input("Press ENTER to draw three Policy tiles from the top of the Policy deck.")
    print("Your three policy tiles are:")
    print(policies_drawn)

    # prompt President to discard 1 policy from policies_drawn
    discard_index = input("Type the number of the policy you'd like to discard. The two remaining policies will be "
                          "passed to the Chancellor, who will make the final decision on which policy to enact. ")
    # ensure valid input
    while True:
        if discard_index.isnumeric():
            discard_index = int(discard_index)
            if discard_index in policies_drawn.keys():
                break
            discard_index = input("Invalid policy number. Re-type a valid policy number and press ENTER: ")
        else:
            discard_index = input("Invalid non-numeric input. Please re-type a valid policy number and press "
                                  "ENTER: ")

    discarded_policy = policies_drawn.pop(discard_index)
    print("You have discarded a " + str(discarded_policy) + " policy. The following two policies that will be passed to"
          " the Chancellor:")
    print(policies_drawn)

    input("Press ENTER to obliterate this message, then pass the computer to the Chancellor.")
    clear_console()
    return policies_drawn


def enact_policy(selected_policies):
    print("------ FOR THE CHANCELLOR'S EYES ONLY! ------")
    input("Press ENTER to confirm you are the Chancellor and reveal the two policy tiles the President has given you.")
    print("Your two policy tiles are:")
    print(selected_policies)
    enact_key = input("Type the number of the policy you'd like to enact and press ENTER: ")
    # ensure valid input
    while True:
        if enact_key.isnumeric():
            enact_key = int(enact_key)
            if enact_key in selected_policies.keys():
                break
            enact_key = input("Invalid policy number. Please re-type a valid policy number and press ENTER: ")
        else:
            enact_key = input("Invalid non-numeric input. Re-type the number of the policy you'd like to enact: ")

    enacted_policy = selected_policies[enact_key]
    input("You have enacted a " + enacted_policy + " policy. Press ENTER to obliterate this message, then "
          "return the computer for everyone's viewing.")
    clear_console()
    return enacted_policy


def update_policy_boards(new_policy):
    """
    :param new_policy: a string indicating the nature of a newly enacted policy: "liberal" or "fascist")
    Updates the global variable policy_boards. No return value.
    """
    global policy_boards
    if new_policy == "Liberal":
        policy_boards["Liberal Policies"] += 1
    elif new_policy == "Fascist":
        policy_boards["Fascist Policies"] += 1


def announce_winners(winning_team):
    print()
    print()
    print("Congratulations, " + winning_team + ". You've won the game! Germany is yours.")


def check_for_winners():
    """
    Checks if the game has reached a point where a team has won, and announces the winners if appropriate.
    :return: Boolean value (True if there are winners, False otherwise).
    """
    winning_team = ""
    # if five Liberal Policies enacted OR Hitler is killed, Liberals win
    if policy_boards["Liberal Policies"] >= 5:
        print("Hooray! Five Liberal Policies have been enacted!")
        winning_team = "Liberals"
    elif "Secret Hitler" not in player_roles:
        print("Wunderbar! Secret Hitler has been killed!")
        winning_team = "Liberals"

    # if six Fascist Policies enacted OR (Hitler elected Chancellor & three or more Fascist Policies enacted), Fascists win
    if policy_boards["Fascist Policies"] >= 6:
        print("XXXX Ach nein... Six Fascist Policies have been enacted. XXXX")
        winning_team = "Fascists"
    elif policy_boards["Fascist Policies"] >= 3 and player_roles[curr_chancellor - 1] == "Secret Hitler":
        print("XXXX Ach nein... More than three Fascist Policies are enacted, and Secret Hitler has just been "
              "elected Chancellor. XXXX")
        winning_team = "Fascists"

    if winning_team != "":
        time.sleep(3)
        announce_winners(winning_team)
        return True
    return False


def pass_presidential_candidacy():
    global curr_president
    if curr_president == 0:  # first round, randomly choose Presidential Candidate until successfully elected
        presidential_candidate = random.randint(1, len(player_roles))
    elif curr_president == len(player_roles):  # reached the last player --> re-start cycle
        presidential_candidate = 1
    else:  # else just pass to next player
        presidential_candidate = curr_president + 1 + election_tracker

    # if 3 Fascist policies enacted, allow President to choose the next president
    if policy_boards["Fascist Policies"] == 3 and election_tracker == 0:
        print("------ EXECUTIVE ACTION! ------")
        presidential_candidate = input("The current President gets to choose the next Presidential Candidate. Type"
                                       " the number of the player you'd like to elect as the next President.")
        while True:
            if presidential_candidate.isnumeric():
                presidential_candidate = int(presidential_candidate)
                if presidential_candidate in range(1, len(player_roles) + 1) and presidential_candidate != curr_president:
                    break
                print("Invalid player number. Valid players only exist within the range 1 to " + str(len(player_roles))
                      + ", excluding the current President.")
            presidential_candidate = input("The current President gets to choose the next President. Type the number of"
                                           " the player you'd like to elect as the next President. ")
    return presidential_candidate



def nominate_chancellor(presidential_candidate):
    chancellor_candidate = input("President, type the number of the player you'd like to nominate as Chancellor. "
                                 "(You may discuss your decision with the other players first.) ")
    while True:
        if chancellor_candidate.isnumeric():
            chancellor_candidate = int(chancellor_candidate)
            if chancellor_candidate in range(1, len(player_roles) + 1):
                if chancellor_candidate != curr_president and chancellor_candidate != curr_chancellor and \
                        chancellor_candidate != presidential_candidate:
                    break
                else:
                    print("Invalid player number. The current President, the current Chancellor, and the new "
                          "Presidential Candidate are ineligible to be the new Chancellor Candidate.")
                    chancellor_candidate = input("President, type the number of the player you'd like to nominate as "
                                                 "Chancellor. (You may discuss your decision with the other players "
                                                 "first.) ")
            else:
                print("Invalid player number. Valid players only exist within the range 1 to " + str(len(player_roles))
                      + ".")
                chancellor_candidate = input("President, type the number of the player you'd like to nominate as "
                                             "Chancellor. (You may discuss your decision with the other players first.)"
                                             " ")
        else:
            chancellor_candidate = input("Invalid non-numeric input. Please re-type a valid number of players and "
                                         "press ENTER: ")
    return chancellor_candidate


def election():
    """
    Form a government for the current round:
    1. Pass the Presidential Candidacy to the next player.
    2. Nominate a Chancellor, chosen by the current President. (discussion allowed)
    * Restrictions: the last elected President & Chancellor are ineligible to be nominated as Chancellor in the current
    round.
    :return:
    """
    global curr_president
    global curr_chancellor
    global election_tracker

    input("Press ENTER once the group is ready to commence a new election.")
    print("Commencing a new election...")
    time.sleep(3)
    print("------ NEW ELECTION! ------")
    # pass the Presidential Candidacy to the next player
    presidential_candidate = pass_presidential_candidacy()
    print("Player " + str(presidential_candidate) + " is the new Presidential Candidate.")

    # nominate a Chancellor, chosen by the current President
    chancellor_candidate = nominate_chancellor(presidential_candidate)
    print("Player " + str(chancellor_candidate) + " has been nominated by the President as the new Chancellor "
          "Candidate.")

    # vote on Chancellor
    print("------ VOTING TIME! ------")
    vote_outcome = input('Players, cast in your vote for the proposed government. Type whether the election '
                         'resulted in a "win," "loss," or "tie," then press ENTER. ')
    possible_outcomes = ["win", "loss", "tie"]
    while vote_outcome not in possible_outcomes:
        vote_outcome = input('Invalid outcome. Type whether the election resulted in a "win," "loss," '
                             'or "tie," then press ENTER. ')

    # (RECURSION!!!!) take appropriate action according to election outcome:
    clear_console()
    print("ANNOUNCING THE OUTCOME OF THE ELECTION...")
    # base case
    if vote_outcome == "win":
        curr_president = presidential_candidate
        curr_chancellor = chancellor_candidate
        election_tracker = 0
        print("The proposed government has won the election! Player " + str(curr_president) + " is the new President,"
              " and Player " + str(curr_chancellor) + " is the new Chancellor.")
    # recursive case (tie or loss)
    else:
        election_tracker += 1
        if election_tracker == 3:
            print("The group has rejected three governments in a row. The country has descended into chaos. The"
                  " Policy on top of the Policy deck will now be enacted immediately.")
            drawn_index = draw_policy_tile()
            top_policy = policy_deck[drawn_index]
            update_policy_boards(top_policy)
            print("The policy at the top of the Policy Deck is a " + top_policy + " Policy. Below are the updated "
                  "Policy Boards:")
            print(policy_boards)
            election_tracker = 0
            curr_chancellor = 0
            print("The Election Tracker has been reset to 0. All Players are now eligible to be the next Chancellor.")
        else:   # election_tracker < 3
            print("The vote has failed. Election tracker (# of consecutive rejected governments): "
                  + str(election_tracker))
            print("Warning: If the group rejects three governments in a row, the country will be thrown into chaos,"
                  " and the Policy on top of the Policy deck will be enacted immediately.")
            print("The Presidential Candidate has missed this chance to be elected.")
        # RECURSIONNNNN!!!! :o
        election()


def legislative_session():
    """
    Enact a new Policy.
    1. President draws the top three tiles from the Policy deck, looks at them in secret, and discards one tile face
    down into the Discard pile.
    2. The remaining two tiles go to the Chancellor, who looks in secret, discards one Policy tile face down, and
    enacts the remaining Policy.
    3. call update_policy_boards().
    :return: the type of policy enacted (either "Fascist" or "Liberal")
    """
    print("Commencing the Legislative Session...")
    time.sleep(3)
    print("------ LEGISLATIVE SESSION! ------")
    selected_policies = draw_policy_tiles()
    enacted_policy = enact_policy(selected_policies)
    print("The Chancellor has enacted a " + enacted_policy + " policy. Below are the updated Policy Boards:")
    update_policy_boards(enacted_policy)
    print(policy_boards)


def presidential_execution():
    global player_roles
    print("------ EXECUTIVE ACTION! ------")
    player_to_kill = input("President, you have been granted the one-time power to execute any player you wish. "
                           "Once you've decided who to kill, type the number of the player you'd like to execute "
                           "and press ENTER.")
    # ensure valid input
    while True:
        if player_to_kill.isnumeric():
            player_to_kill = int(player_to_kill)
            if player_to_kill in range(1, len(player_roles) + 1):
                break
            player_to_kill = input("Invalid player number. Please re-type a valid player number and press ENTER: ")
        else:
            player_to_kill = input("Invalid non-numeric input. Re-type the number of the policy you'd like to enact: ")

    player_to_kill_index = player_to_kill - 1
    player_roles[player_to_kill_index] = "dead"
    print("Player " + str(player_to_kill) + " has been executed. He/she can no longer participate in the game.")


def executive_action():
    """
    Exercise governmental power.
    1. Check policy boards to see if an executive action must be taken.
    2. Prompt President to take the appropriate executive action. (investigate loyalty, call special election, policy peek,
    execution
    :return:
    """
    if policy_boards["Fascist Policies"] == 2:
        # investigate loyalty
        print("------ EXECUTIVE ACTION! ------")
        print("------ FOR THE PRESIDENT'S EYES ONLY! ------")
        input("Press ENTER to confirm you are the President, and that nobody else can see your screen.")
        player_to_investigate = input("President, who's loyalty would you like to investigate? Type the Player"
                                      " number and press ENTER to reveal their secret role. ")
        # ensure valid input
        while True:
            if player_to_investigate.isnumeric():
                player_to_investigate = int(player_to_investigate)
                if player_to_investigate in range(1, len(player_roles) + 1):
                    break
                player_to_investigate = input("Invalid player number. Type a valid Player number between 1 and " +
                                              str(len(player_roles)) + " to investigate their loyalty and press ENTER."
                                              " ")
            else:
                player_to_investigate = input("Invalid non-numeric input. Type a valid Player number between 1 and "
                                              + str(len(player_roles)) + " to investigate their loyalty and press "
                                              "ENTER. ")

        print("Player " + str(player_to_investigate) + " is a " + player_roles[player_to_investigate - 1] + ".")
        input("Press ENTER to obliterate this message, and pass the computer back to the public.")
        clear_console()
    elif policy_boards["Fascist Policies"] == 3:
        # president picks the next presidential candidate --> all action happens in pass_presidential_candidacy()
        print("------ EXECUTIVE ACTION! ------")
        print("President, you have been given the one-time power to pick the next Presidential Candidate in the "
              "upcoming Election.")
    elif policy_boards["Fascist Policies"] == 4:
        # president kills a player
        presidential_execution()
    elif policy_boards["Fascist Policies"] == 5:
        # president kills a player
        presidential_execution()
        # veto power unlocked


# PLAY THE GAME!
# setup:
assign_roles()

# play rounds of the game until there is a winner
while True:
    election()
    if check_for_winners():
         break
    legislative_session()
    if check_for_winners():
        break
    executive_action()
    if check_for_winners():
        break

