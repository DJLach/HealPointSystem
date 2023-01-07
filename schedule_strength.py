import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
GTennis2022 = client.open('PowerRatings').worksheet('GTennis2022')
import time
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

GTennis2022.clear()
GTennis2022.insert_row(["Rank (within division)", "School Name", "Class", "Region", "Wins", "Losses", "Ties", "Games", "AA Wins", "A Wins", "B Wins", "C Wins", "D Wins", "PI", "TI", "SoS", "SoS_heal", "SoS2", "SoS2_Heal", "GameWP", "PointWP", "GWP_Over_PWP", "PowerR"])

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

def get_current_wins(school_name):
    get_wins = "SELECT wins FROM school WHERE school_name = '%s'" % (school_name)
    get_ties = "SELECT ties FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_wins)
    wins = mycursor.fetchone()[0]
    wins = Decimal(wins)
    #counts each tie as a half win for SoS
    mycursor.execute(get_ties)
    ties = mycursor.fetchone()[0]
    ties = Decimal(ties) / 2
    wins = wins + ties
    return wins

def get_current_games(school_name):
    get_games = "SELECT games FROM school WHERE school_name = '%s'" % (school_name)
    mycursor.execute(get_games)
    games = mycursor.fetchone()[0]
    games = Decimal(games)
    return games

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
        SoS_heal = SoS_heal_points / games / 34 * 100 #/34 because class D is lowest class
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
    SoS2_heal_combined_dict[current_school] = SoS2_heal_combined

    add_SoS2 = "UPDATE school SET SoS2 = %s WHERE school_name = %s"
    add_SoS2_tuple = SoS2_combined, current_school
    mycursor.execute(add_SoS2, add_SoS2_tuple)

    add_SoS2_heal = "UPDATE school SET SoS2_heal = %s WHERE school_name = %s"
    add_SoS2_heal_tuple = SoS2_heal_combined, current_school
    mycursor.execute(add_SoS2_heal, add_SoS2_heal_tuple)
print("SoS2_combined and SoS2_heal_combined updated")

points_dict = {} #will store individual game/match scores (ex. 5-0 4-1 3-2)
for i in range(len(school_names)):

    current_school = get_current_school_name(i + 1)
    total_points = points_for = points_against = 0
    
    try:
        get_w_scores = "SELECT Score_1, Score_2 FROM match_list WHERE win_ID = %s"
        current_school_tup = current_school,
        mycursor.execute(get_w_scores, current_school_tup)
        w_scores = mycursor.fetchall()
        for ii in range(len(w_scores)):
            points_for = points_for + w_scores[ii][0]
            points_against = points_against + w_scores[ii][1]
        
    except:
        pass

    try:
        get_l_scores = "SELECT Score_1, Score_2 FROM match_list WHERE lose_ID = %s"
        current_school_tup = current_school,
        mycursor.execute(get_l_scores, current_school_tup)
        l_scores = mycursor.fetchall()
        for ii in range(len(l_scores)):
            points_for = points_for + l_scores[ii][1] #[0] and [1] needed to be swapped for wins/losses
            points_against = points_against + l_scores[ii][0]
    except:
        pass

    try:
        get_t_scores = "SELECT Score_1, Score_2 FROM match_list WHERE Tie_ID_1 = %s"
        current_school_tup = current_school,
        mycursor.execute(get_t_scores, current_school_tup)
        t_scores = mycursor.fetchall()
        for ii in range(len(t_scores)):
            points_for = points_for + t_scores[ii][1]
            points_against = points_against + t_scores[ii][0]
    except:
        pass

    try:
        get_t_scores = "SELECT Score_1, Score_2 FROM match_list WHERE Tie_ID_2 = %s"
        current_school_tup = current_school,
        mycursor.execute(get_t_scores, current_school_tup)
        t_scores = mycursor.fetchall()
        for ii in range(len(t_scores)):
            points_for = points_for + t_scores[ii][1]
            points_against = points_against + t_scores[ii][0]
    except:
        pass
    
    total_points = points_for + points_against

    try:
        points_ratio = points_for / total_points
    except ZeroDivisionError:
        points_ratio = 0

    points_dict[current_school] = [points_for, points_against, total_points, points_ratio] #place values in dict for each school prior to sending to database

    current_wins = get_current_wins(current_school)
    current_games = get_current_games(current_school)
    #power ratings is equal to two times a team's wins times its schedule strength plus its point win ratio * schedule strength
    current_SoS2_heal_combined = Decimal(SoS2_heal_combined_dict[current_school]) #gets finalized 2-layer heal schedule strength value
    points_win_ratio = Decimal(points_dict[current_school][3])
    try: 
        games_win_ratio = current_wins / current_games
    except: #what is this error type?
        games__win_ratio = 0
    try:
        game_win_percentage = Decimal(current_wins) / Decimal(current_games) * Decimal(100)
    except:
        game_win_percentage = 0

    power_rating = (2 * games_win_ratio + 1 * points_win_ratio) * current_SoS2_heal_combined / 3

    add_game_win_percentage = "UPDATE school set GameWP = %s WHERE school_name = %s"
    game_win_tuple = game_win_percentage, current_school
    mycursor.execute(add_game_win_percentage, game_win_tuple)

    point_win_percentage = points_win_ratio * 100
    add_point_win_percentage = "UPDATE school set PointWP = %s WHERE school_name = %s"
    point_win_tuple = point_win_percentage, current_school
    mycursor.execute(add_point_win_percentage, point_win_tuple)

    #calculate game win percentage over point win percent (difference) to demonstrate "clutch" factor, then send to server
    GWP_Over_PWP = game_win_percentage - point_win_percentage
    GWP_Over_PWP_query = "UPDATE school set GWP_Over_PWP = %s WHERE school_name = %s"
    GWP_Over_PWP_tuple = GWP_Over_PWP, current_school
    mycursor.execute(GWP_Over_PWP_query, GWP_Over_PWP_tuple)

    add_power_rating = "UPDATE school SET PowerR = %s WHERE school_name = %s"
    power_rating_tuple = power_rating, current_school
    mycursor.execute(add_power_rating, power_rating_tuple)

school_list_sheet = []
AA_N_school_list_sheet = []
A_N_school_list_sheet = []
B_N_school_list_sheet = []
C_N_school_list_sheet = []
D_N_school_list_sheet = []
AA_S_school_list_sheet = []
A_S_school_list_sheet = []
B_S_school_list_sheet = []
C_S_school_list_sheet = []
D_S_school_list_sheet = []

row = 1
for i in range(len(school_names)):
    row += 1
    
    ID_query = "SELECT ID FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(ID_query)
    ID_sheet = mycursor.fetchone()[0]

    school_name_query = "SELECT school_name FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(school_name_query)
    school_name_sheet = mycursor.fetchone()[0]
    
    class_query = "SELECT class FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(class_query)
    class_sheet = mycursor.fetchone()[0]

    region_query = "SELECT region FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(region_query)
    region_sheet = mycursor.fetchone()[0]

    wins_query = "SELECT wins FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(wins_query)
    wins_sheet = mycursor.fetchone()[0]

    losses_query = "SELECT losses FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(losses_query)
    losses_sheet = mycursor.fetchone()[0]

    ties_query = "SELECT ties FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(ties_query)
    ties_sheet = mycursor.fetchone()[0]

    games_query = "SELECT games FROM school WHERE school_name = '%s'" % (school_names[i])
    mycursor.execute(games_query)
    games_sheet = mycursor.fetchone()[0]

    AA_wins_query = "SELECT AA_wins FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(AA_wins_query)
    AA_wins_sheet = mycursor.fetchone()[0]
    AA_wins_sheet = str(AA_wins_sheet)

    A_wins_query = "SELECT A_wins FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(A_wins_query)
    A_wins_sheet = mycursor.fetchone()[0]
    A_wins_sheet = str(A_wins_sheet)

    B_wins_query = "SELECT B_wins FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(B_wins_query)
    B_wins_sheet = mycursor.fetchone()[0]
    B_wins_sheet = str(B_wins_sheet)

    C_wins_query = "SELECT C_wins FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(C_wins_query)
    C_wins_sheet = mycursor.fetchone()[0]
    C_wins_sheet = str(C_wins_sheet)

    D_wins_query = "SELECT D_wins FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(D_wins_query)
    D_wins_sheet = mycursor.fetchone()[0]
    D_wins_sheet = str(D_wins_sheet)

    PI_query = "SELECT PI FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(PI_query)
    PI_sheet = mycursor.fetchone()[0]

    TI_query = "SELECT TI FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(TI_query)
    TI_sheet = mycursor.fetchone()[0]

    SoS_query = "SELECT SoS FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(SoS_query)
    SoS_sheet = mycursor.fetchone()[0]

    SoS_heal_query = "SELECT SoS_heal FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(SoS_heal_query)
    SoS_heal_sheet = mycursor.fetchone()[0]

    SoS2_query = "SELECT SoS2 FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(SoS2_query)
    SoS2_sheet = mycursor.fetchone()[0]

    SoS2_heal_query = "SELECT SoS2_heal FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(SoS2_heal_query)
    SoS2_heal_sheet = mycursor.fetchone()[0]

    GameWP_query = "SELECT GameWP FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(GameWP_query)
    GameWP_sheet = mycursor.fetchone()[0]

    PointWP_query = "SELECT PointWP FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(PointWP_query)
    PointWP_sheet = mycursor.fetchone()[0]

    GWP_Over_PWP_query = "SELECT GWP_Over_PWP FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(GWP_Over_PWP_query)
    GWP_Over_PWP_sheet = mycursor.fetchone()[0]

    PowerR_query = "SELECT PowerR FROM school WHERE school_name = '%s'" % (school_names[i])    
    mycursor.execute(PowerR_query)
    PowerR_sheet = mycursor.fetchone()[0]
    
    school_row = [school_name_sheet, class_sheet, region_sheet, wins_sheet, losses_sheet, ties_sheet, games_sheet, AA_wins_sheet, A_wins_sheet, B_wins_sheet, C_wins_sheet, D_wins_sheet, PI_sheet, TI_sheet, SoS_sheet, SoS_heal_sheet, SoS2_sheet, SoS2_heal_sheet, GameWP_sheet, PointWP_sheet, GWP_Over_PWP_sheet, PowerR_sheet]
    
    school_list_sheet.append(school_row)

    if region_sheet == "North":
        if class_sheet == "AA":
            AA_N_school_list_sheet.append(school_row)
        if class_sheet == "A":
            A_N_school_list_sheet.append(school_row)
        if class_sheet == "B":
            B_N_school_list_sheet.append(school_row)
        if class_sheet == "C":
            C_N_school_list_sheet.append(school_row)
        if class_sheet == "D":
            D_N_school_list_sheet.append(school_row)
    if region_sheet == "South":
        if class_sheet == "AA":
            AA_S_school_list_sheet.append(school_row)
        if class_sheet == "A":
            A_S_school_list_sheet.append(school_row)
        if class_sheet == "B":
            B_S_school_list_sheet.append(school_row)
        if class_sheet == "C":
            C_S_school_list_sheet.append(school_row)
        if class_sheet == "D":
            D_S_school_list_sheet.append(school_row)

row = 2
range_start = "B"
range_end = ":W"
sheet_range = ""
ranks = []
clear_color_range = "A1:W" + str(len(school_names) + 5)

GTennis2022.append_rows(school_list_sheet, table_range='B2')
GTennis2022.format(clear_color_range, {"backgroundColor": {"red": 1, "green": 1, "blue": 1}})

if len(AA_N_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(AA_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(AA_N_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 20, "green": 100, "blue": 100}})

if len(AA_S_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(AA_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(AA_S_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 100, "green": 20, "blue": 100}})


if len(A_N_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(A_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(A_N_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 20, "green": 20, "blue": 100}})
    
if len(A_S_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(A_S_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(A_S_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 100, "green": 20, "blue": 100}})

if len(B_N_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(B_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(B_N_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 20, "green": 20, "blue": 100}})

if len(B_S_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(B_S_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(B_S_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 100, "green": 20, "blue": 100}})

if len(C_N_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(C_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(C_N_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 20, "green": 20, "blue": 100}})

if len(C_S_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(C_S_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(C_S_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 100, "green": 20, "blue": 100}})

if len(D_N_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(D_N_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(D_N_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 20, "green": 20, "blue": 100}})

if len(D_S_school_list_sheet) > 0:
    range_start = "B" + str(row)
    color_range_start = "A" + str(row)
    row = row + len(D_S_school_list_sheet) - 1
    range_end = ":W" + str(row)
    sheet_range = range_start + range_end
    color_sheet_range = color_range_start + range_end
    GTennis2022.sort((23, 'des'), range=sheet_range)
    row += 1
    for ii in range(len(D_S_school_list_sheet)):
        ranks.append([ii+1])
    GTennis2022.format(color_sheet_range, {"backgroundColor": {"red": 100, "green": 20, "blue": 100}})

row -= 1
no_bold_range = 'A2:W' + str(row)

GTennis2022.append_rows(ranks, table_range='A2')
GTennis2022.format('A1:W1', {"textFormat": {"bold": True}})
GTennis2022.format(no_bold_range, {"textFormat": {"bold": False}})
GTennis2022.freeze(rows=1, cols=2)


print("Power rating sheet updated")

#ADD LINE BELOW EACH DIVISION