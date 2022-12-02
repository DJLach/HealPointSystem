from decimal import Decimal
import mysql.connector
#connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="heal")
mycursor = mydb.cursor()
mydb.autocommit = True

school_names = []

mycursor.execute("SELECT MAX(ID) FROM school")
max_match = mycursor.fetchone()[0]
max_match = int(max_match)

def get_current_school_name(ID):
    school_query = "SELECT school_name FROM school WHERE ID = '%s'"
    tup_count = ID,
    mycursor.execute(school_query, tup_count)
    current_school_name = mycursor.fetchone()[0]
    return current_school_name

def get_current_school_class(school_name):
    class_query = "SELECT class FROM school WHERE school_name = %s"
    tup_school = school_name,
    mycursor.execute(class_query, tup_school)
    current_school_class = mycursor.fetchone()[0]
    return current_school_class

def get_AA_wins(school_name):
    get_wins = "SELECT AA_wins FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    AA_wins = mycursor.fetchone()[0]
    AA_wins = Decimal(AA_wins)
    return AA_wins

def get_A_wins(school_name):
    get_wins = "SELECT A_wins FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    A_wins = mycursor.fetchone()[0]
    A_wins = Decimal(A_wins)
    return A_wins

def get_B_wins(school_name):
    get_wins = "SELECT B_wins FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    B_wins = mycursor.fetchone()[0]
    B_wins = Decimal(B_wins)
    return B_wins

def get_C_wins(school_name):
    get_wins = "SELECT C_wins FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    C_wins = mycursor.fetchone()[0]
    C_wins = Decimal(C_wins)
    return C_wins

def get_D_wins(school_name):
    get_wins = "SELECT D_wins FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    D_wins = mycursor.fetchone()[0]
    D_wins = Decimal(D_wins)
    return D_wins

#generate list of all schools/teams in system
i = 1
while i <= max_match:
    new_school_name = get_current_school_name(i)
    school_names.append(new_school_name)
    i += 1

SoS_dict = {} #will store SoS values for each school for secondary calculations
SoS_heal_dict = {} #will store SoS_heal values for each school for secondary calculations
matches_played_dict = {} #will store matches {school_name : [matches]}

for i in range(len(school_names)):
    SoS_points = 0 #initialize variable for raw SoS points (will be divided by games to get SoS)
    SoS_heal_points = 0 #same as SoS raw, but will include multiplied class values
    games_to_subtract = 0 #initialize variable for games to subtract from game total for SoS
    games = 0 #total games used in SoS calculation
    class_wins_dict = {}
    games_against_dict = {}
    match_duplicate_list = []
    win_list = []
    lose_list = []
    tie_1_list = []
    tie_2_list = []

    current_school = get_current_school_name(i + 1)

    try:
        win_query = "SELECT Lose_ID FROM match_list WHERE Win_ID = '%s'" % (current_school)
        mycursor.execute(win_query)
        win_teams = mycursor.fetchall()
        for ii in range(len(win_teams)):
            games_against_dict[win_teams[ii][0]] = 0
            match_duplicate_list.append(win_teams[ii][0]) #adds to list of teams played including duplicates
            win_list.append(win_teams[ii][0]) #adds to list of teams defeated
    except:
        pass
    try:
        lose_query = "SELECT Win_ID FROM match_list WHERE Lose_ID = '%s'" % (current_school)
        mycursor.execute(lose_query)
        lose_teams = mycursor.fetchall()
        for ii in range(len(lose_teams)):
            games_against_dict[lose_teams[ii][0]] = 0
            match_duplicate_list.append(lose_teams[ii][0])
            lose_list.append(lose_teams[ii][0]) #adds to list of teams lost to
    except:
        pass
    try:
        tie_1_query = "SELECT Tie_ID_1 FROM match_list WHERE Tie_ID_2 = '%s'" % (current_school)
        mycursor.execute(tie_1_query)
        tie_1_teams = mycursor.fetchall()
        for ii in range(len(tie_1_teams)):
            games_against_dict[tie_1_teams[ii][0]] = 0
            match_duplicate_list.append(tie_1_teams[ii][0])
            tie_1_list.append(tie_1_teams[ii][0])
    except:
        pass
    try:
        tie_2_query = "SELECT Tie_ID_2 FROM match_list WHERE Tie_ID_1 = '%s'" % (current_school)
        mycursor.execute(tie_2_query)
        tie_2_teams = mycursor.fetchall()
        for ii in range(len(tie_2_teams)):
            games_against_dict[tie_2_teams[ii][0]] = 0
            match_duplicate_list.append(tie_2_teams[ii][0])
            tie_2_list.append(tie_2_teams[ii][0])
    except:
        pass
    for ii in range(len(match_duplicate_list)):
        games_against_dict[match_duplicate_list[ii]] = match_duplicate_list.count(match_duplicate_list[ii])
    #above, number of matches played against each school has been obtained and is contained in games_against_dict
    games = 0
    for ii in range(len(match_duplicate_list)):
        get_games = "SELECT games FROM school WHERE school_name = '%s'" % (match_duplicate_list[ii])
        mycursor.execute(get_games)
        new_games = mycursor.fetchone()[0]
        new_games = int(new_games)
        games = games + new_games
    class_wins_dict = games_against_dict.copy()
    match_list = [*set(match_duplicate_list)] #remove duplicate names
    for ii in range(len(games_against_dict)): #loops to determine how many games should be subtracted from game total before calculating SoS
        games_to_subtract = games_to_subtract + (games_against_dict[match_list[ii]] * games_against_dict[match_list[ii]])
    for ii in range(len(class_wins_dict)):
        AA_wins = get_AA_wins(match_list[ii])
        A_wins = get_A_wins(match_list[ii])
        B_wins = get_B_wins(match_list[ii])
        C_wins = get_C_wins(match_list[ii])
        D_wins = get_D_wins(match_list[ii])
        class_win_list = [AA_wins, A_wins, B_wins, C_wins, D_wins]
        class_wins_dict[match_list[ii]] = class_win_list
    current_school_class = get_current_school_class(current_school)
    for ii in range(len(lose_list)):
        if current_school_class == "AA":
            class_wins_dict[lose_list[ii]][0] -= 1 #removes loss from team if class AA
        elif current_school_class == "A":
            class_wins_dict[lose_list[ii]][1] -= 1 #removes loss from team if class A
        elif current_school_class == "B":
            class_wins_dict[lose_list[ii]][2] -= 1 #removes loss from team if class B
        elif current_school_class == "C":
            class_wins_dict[lose_list[ii]][3] -= 1 #removes loss from team if class C
        elif current_school_class == "D":
            class_wins_dict[lose_list[ii]][4] -= 1 #removes loss from team if class D

    games = games - games_to_subtract
    for ii in range(len(match_duplicate_list)):
        SoS_points = SoS_points + class_wins_dict[match_duplicate_list[ii]][0] + class_wins_dict[match_duplicate_list[ii]][1] + class_wins_dict[match_duplicate_list[ii]][2] + class_wins_dict[match_duplicate_list[ii]][3] + class_wins_dict[match_duplicate_list[ii]][4]
        SoS_heal_points = SoS_heal_points + 42 * class_wins_dict[match_duplicate_list[ii]][0] + 40 * class_wins_dict[match_duplicate_list[ii]][1] + 38 * class_wins_dict[match_duplicate_list[ii]][2] + 36 * class_wins_dict[match_duplicate_list[ii]][3] + 34 * class_wins_dict[match_duplicate_list[ii]][4]
    if games > 0:
        SoS = SoS_points / games * 100
        SoS_heal = SoS_heal_points / games /40 * 100
    elif games == 0:
        SoS = 0
        SoS_heal = 0
    add_SoS = "UPDATE school SET SoS = %s WHERE school_name = %s"
    add_SoS_tuple = SoS, current_school
    mycursor.execute(add_SoS, add_SoS_tuple)

    add_SoS_heal = "UPDATE school SET SoS_heal = %s WHERE school_name = %s"
    add_SoS_heal_tuple = SoS_heal, current_school
    mycursor.execute(add_SoS_heal, add_SoS_heal_tuple)

    SoS_dict.update({current_school: SoS}) #adds each school and SoS val to dict
    SoS_heal_dict.update({current_school: SoS_heal}) #adds each school and SoS_heal val to dict
    matches_played_dict.update({current_school : match_duplicate_list})

print("SoS and SoS_heal updated")

SoS2_dict = {}
SoS2_heal_dict = {}

for i in range(len(school_names)):
    SoS2_points = 0
    SoS2_heal_points = 0

    current_school = get_current_school_name(i + 1)
    for ii in range(len(matches_played_dict[current_school])):
        opp_school = matches_played_dict[current_school][ii]
        SoS2_points = SoS2_points + SoS_dict[opp_school]
        SoS2_heal_points = SoS2_heal_points + SoS_heal_dict[opp_school]
    
    if len(matches_played_dict[current_school]) > 0:
        SoS2 = SoS2_points / len(matches_played_dict[current_school])
        SoS2_heal = SoS2_heal_points / len(matches_played_dict[current_school])
    if len(matches_played_dict[current_school]) == 0:
        SoS2 = 0
        SoS2_heal = 0

    SoS2_dict.update({current_school : SoS2})
    SoS2_heal_dict.update({current_school : SoS2_heal})

SoS2_combined_dict = {}
SoS2_heal_combined_dict = {}
for i in range(len(school_names)):
    current_school = get_current_school_name(i + 1)
    
    SoS2_combined = (2 * SoS_dict[current_school] + SoS2_dict[current_school]) / 3
    SoS2_combined_dict[current_school] = SoS2_combined
    
    SoS2_heal_combined = (2 * SoS_heal_dict[current_school] + SoS2_heal_dict[current_school]) / 3
    SoS2_combined_dict[current_school] = SoS2_heal_combined

    add_SoS2 = "UPDATE school SET SoS2 = %s WHERE school_name = %s"
    add_SoS2_tuple = SoS2_combined, current_school
    mycursor.execute(add_SoS2, add_SoS2_tuple)

    add_SoS2_heal = "UPDATE school SET SoS2_heal = %s WHERE school_name = %s"
    add_SoS2_heal_tuple = SoS2_heal_combined, current_school
    mycursor.execute(add_SoS2_heal, add_SoS2_heal_tuple)
print("SoS2 and SoS2_heal updated")