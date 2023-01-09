import gspread
from oauth2client.service_account import ServiceAccountCredentials
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
#connect to Google Sheets
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(credentials)

def update_matches(str_match_list_sheet):
    school_names = []
    mycursor.execute("delete from match_list")
    mycursor.execute("DELETE FROM school")
    match_list_sheet = client.open('PowerRatings').worksheet(str_match_list_sheet)
    match_results = match_list_sheet.get_all_values()
    new_ID = 0
    if len(match_results) > 1:
        del match_results[0]
        for i in range(len(match_results)):
            m_ID = match_results[i][0]
            m_Win_ID = match_results[i][1]
            m_Lose_ID = match_results[i][2]
            m_Tie_ID_1 = match_results[i][3]
            m_Tie_ID_2 = match_results[i][4]
            m_Score_1 = match_results[i][5]
            m_Score_2 = match_results[i][6]
            m_T1_Class = match_results[i][7]
            m_T1_Region = match_results[i][8]
            m_T2_Class = match_results[i][9]
            m_T2_Region = match_results[i][10]
            match_send = "insert into match_list (ID, Win_ID, Lose_ID, Tie_ID_1, Tie_ID_2, Score_1, Score_2) values (%s, %s, %s, %s, %s, %s, %s)"
            match_val = (m_ID, m_Win_ID, m_Lose_ID, m_Tie_ID_1, m_Tie_ID_2, m_Score_1, m_Score_2)
            mycursor.execute(match_send, match_val)
            ID_class_update = "INSERT INTO school (ID, school_name, class, region) VALUES (%s, %s, %s, %s)"
            if m_Win_ID not in school_names and m_Win_ID != "":
                school_names.append(m_Win_ID)
                new_ID += 1
                values = (new_ID, m_Win_ID, m_T1_Class, m_T1_Region)
                mycursor.execute(ID_class_update, values)
            if m_Lose_ID not in school_names and m_Lose_ID != "":
                school_names.append(m_Lose_ID)
                new_ID += 1
                values = (new_ID, m_Lose_ID, m_T2_Class, m_T2_Region)
                mycursor.execute(ID_class_update, values)
            if m_Tie_ID_1 not in school_names and m_Tie_ID_1 != "":
                school_names.append(m_Tie_ID_1)
                new_ID += 1
                values = (new_ID, m_Tie_ID_1, m_T1_Class, m_T1_Region)
                mycursor.execute(ID_class_update, values)
            if m_Tie_ID_2 not in school_names and m_Tie_ID_2 != "":
                school_names.append(m_Tie_ID_2)
                new_ID += 1
                values = (new_ID, m_Tie_ID_2, m_T2_Class, m_T2_Region)
                mycursor.execute(ID_class_update, values)

    return school_names
def PI_summation(points):
  max_number = "SELECT MAX(ID) FROM school"
  mycursor.execute(max_number)
  max_match = mycursor.fetchone()[0]
  max_match = int(max_match)
  i = 1
  while i <= max_match:
    tup_i = i,
    PI_sum = 0
    #find sum of all prelminary index values for each school
    AA_get = "SELECT AA_Wins FROM school WHERE ID = %s"
    mycursor.execute(AA_get, tup_i)
    AA_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (AA_count * points[0])
    A_get = "SELECT A_Wins FROM school WHERE ID = %s"
    mycursor.execute(A_get, tup_i)
    A_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (A_count * points[1])
    B_get = "SELECT B_Wins FROM school WHERE ID = %s"
    mycursor.execute(B_get, tup_i)
    B_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (B_count * points[2])
    C_get = "SELECT C_Wins FROM school WHERE ID = %s"
    mycursor.execute(C_get, tup_i)
    C_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (C_count * points[3])
    D_get = "SELECT D_Wins FROM school WHERE ID = %s"
    mycursor.execute(D_get, tup_i)
    D_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (D_count * points[4])
    #divde total PI summed values by number of games to get current PI for a given school
    game_query = "SELECT games FROM school WHERE ID = %s"
    mycursor.execute(game_query, tup_i)
    game_count = mycursor.fetchone()[0]
    if game_count != 0:
      PI_sum = PI_sum / game_count
      if PI_sum < 1:
        PI_sum = 1
    else:
      PI_sum = 1
    PI_update = "UPDATE school SET PI = %s WHERE ID = %s"
    tup_PI_update = (PI_sum, i)
    mycursor.execute(PI_update, tup_PI_update)
    i += 1
def TI_summation(school_names):
  #surround this with while loop to loop thru school list, inner loop will generate/loop thru defeated/tied lists
  i = 1
  while i <= len(school_names):
    mycursor.execute("delete from temp_match_list")
    #find winning team name and number of wins
    primary_team = i,
    select_school_name = "SELECT school_name FROM school WHERE ID = %s"
    mycursor.execute(select_school_name, primary_team)
    pri_name = mycursor.fetchone()[0]
    pri_name_2 = pri_name,
    select_lose_ID = "SELECT Lose_ID FROM match_list WHERE WIN_ID = %s"
    mycursor.execute(select_lose_ID, pri_name_2)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain wins for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      mycursor.execute(select_lose_ID, pri_name_2)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      match_entry = "INSERT INTO Temp_Match_List (ID, Win_ID, Lose_ID) VALUES (%s, %s, %s)"
      str_c = str(c)
      val = (str_c, pri_name, sec_name)
      mycursor.execute(match_entry, val)
      c += 1
    #add wins to TI
    d = 1
    TI_sum = 0
    while d <= temp_length:
      tup_d = d,
      select_lose_ID_temp = "SELECT Lose_ID FROM temp_match_list WHERE ID = %s"
      mycursor.execute(select_lose_ID_temp, tup_d)
      sec_name = mycursor.fetchone()[0]
      select_PI = "SELECT PI FROM school WHERE school_name = %s"
      tup_sec_name = sec_name,
      mycursor.execute(select_PI, tup_sec_name)
      sec_PI = mycursor.fetchone()[0]
      TI_sum = TI_sum + sec_PI
      d += 1
    #clears data from temp_match table
    mycursor.execute("delete from temp_match_list")
    #find tie team name (when team 1) and number of ties as team 1
    primary_team = i
    tup_primary_team = i, #CHECK THESE THREE LINES WITH TIE DATA
    select_school_name_query = "SELECT school_name FROM school WHERE ID = %s"
    mycursor.execute(select_school_name_query, tup_primary_team)
    pri_name = mycursor.fetchone()[0]
    tup_pri_name = pri_name,
    select_tie_ID_2 = "SELECT Tie_ID_2 FROM match_list WHERE Tie_ID_1 = %s"
    mycursor.execute(select_tie_ID_2, tup_pri_name)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain ties for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      mycursor.execute(select_tie_ID_2, tup_pri_name)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      match_entry = "INSERT INTO Temp_Match_List (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, %s, %s)"
      str_c = str(c)
      val = (str_c, pri_name, sec_name)
      mycursor.execute(match_entry, val)
      c += 1
    #add ties to TI
    d = 1
    while d <= temp_length:
      tuple_d = d,
      s_t_2 = "SELECT Tie_ID_2 FROM temp_match_list WHERE ID = %s"
      mycursor.execute(s_t_2, tuple_d)
      sec_name = mycursor.fetchone()[0]
      tuple_sec_name = sec_name,
      select_PI = "SELECT PI FROM school WHERE school_name = %s"
      mycursor.execute(select_PI, tuple_sec_name)
      sec_PI = mycursor.fetchone()[0]
      #only half the PI is used because it's a tie, not a win
      sec_PI = sec_PI / 2
      TI_sum = TI_sum + sec_PI
      d += 1
    mycursor.execute("delete from temp_match_list")
    #find tie team name (when team 2) and number of ties as team 2
    primary_team = i
    t_p_t = primary_team,
    s_s_n = "SELECT school_name FROM school WHERE ID = %s"
    mycursor.execute(s_s_n, t_p_t)
    pri_name = mycursor.fetchone()[0]
    tuple_pri_name = pri_name,
    s_t_1 = "SELECT Tie_ID_1 FROM match_list WHERE Tie_ID_2 = %s"
    mycursor.execute(s_t_1, tuple_pri_name)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain ties for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      t_p_n = pri_name,
      s_t_i_1 = "SELECT TIE_ID_1 FROM match_list WHERE Tie_ID_2 = %s"
      mycursor.execute(s_t_i_1, t_p_n)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      match_entry = "INSERT INTO Temp_Match_List (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, %s, %s)"
      str_c = str(c)
      val = (str_c, pri_name, sec_name)
      mycursor.execute(match_entry, val)
      c += 1
    #add ties to TI
    d = 1
    while d <= temp_length:
      t_d = d,
      s_t_i_2 = "SELECT Tie_ID_2 FROM temp_match_list WHERE ID = %s"
      mycursor.execute(s_t_i_2, t_d)
      sec_name = mycursor.fetchone()[0]
      s_n = sec_name,
      s_PI = "SELECT PI FROM school WHERE school_name = %s"
      mycursor.execute(s_PI, s_n)
      sec_PI = mycursor.fetchone()[0]
      #only half the PI is used because it's a tie, not a win
      sec_PI = sec_PI / 2
      #print (sec_PI)
      TI_sum = TI_sum + sec_PI
      d += 1
    #TI = sum of defeated PI / games played * 10
    t_primary_team = primary_team,
    s_g = "SELECT games FROM school WHERE ID = %s"
    mycursor.execute(s_g, t_primary_team)
    game_count = mycursor.fetchone()[0]
    if game_count != 0:
      TI_sum = 10 * TI_sum / game_count
    else:
      TI_sum = 0
    tup_TI_pri = (TI_sum, primary_team)
    u_s_s = "UPDATE school SET TI = %s WHERE ID = %s"
    mycursor.execute(u_s_s, tup_TI_pri)
    #print (TI_sum)
    i += 1
def school_setup(school_name_list):
    points = [42, 40, 38, 36, 34] #update to take values from database
    #set list of schools
    school_names = school_name_list #will make list of school names from match_list

    #reset wins/games in database
    mycursor.execute("UPDATE school SET wins = 0")
    mycursor.execute("UPDATE school SET losses = 0")
    mycursor.execute("UPDATE school SET ties = 0")
    mycursor.execute("UPDATE school SET games = 0")
    mycursor.execute("UPDATE school SET AA_wins = 0")
    mycursor.execute("UPDATE school SET A_wins = 0")
    mycursor.execute("UPDATE school SET B_wins = 0")
    mycursor.execute("UPDATE school SET C_wins = 0")
    mycursor.execute("UPDATE school SET D_wins = 0")
    mycursor.execute("UPDATE school SET PI = 0")
    mycursor.execute("UPDATE school SET TI = 0")
    print ("updating database. . .")
    #determine how many matches are currently set in database
    number_matches = "SELECT COUNT(ID) FROM match_list;"
    mycursor.execute(number_matches)
    int_number_matches = mycursor.fetchone()[0]
    #iterates through all losing teams and updates wins, games, and class wins in school table - current values start at 1
    i = 1
    while i <= int_number_matches:
        str_i = str(i)
        #determine if win/loss or tie/tie scenario
        win_scenario = "~~~"
        tup_i = str_i,
        win_scenario = "SELECT Win_ID FROM match_list WHERE ID = %s"
        mycursor.execute(win_scenario, tup_i)
        win_scenario = mycursor.fetchone()[0]
        win_scenario = str(win_scenario)
        tie_scenario = "~~~"
        tie_scenario = "SELECT Tie_ID_2 FROM match_list WHERE ID = %s"
        mycursor.execute(tie_scenario, tup_i)
        tie_scenario = mycursor.fetchone()[0]
        tie_scenario = str(tie_scenario)
        #wins
        if win_scenario in school_names:
            win = "SELECT Win_ID FROM match_list WHERE ID = %s"
            mycursor.execute(win, tup_i)
            str_win = mycursor.fetchone()[0]
            str_win = str(str_win)
            tup_str_win = str_win,
            update_school_games_w = "UPDATE school SET games = games + 1 WHERE school_name = %s"
            update_school_wins = "UPDATE school SET wins = wins + 1 WHERE school_name = %s"
            mycursor.execute(update_school_games_w, tup_str_win)
            mycursor.execute(update_school_wins, tup_str_win)
            lose = "SELECT Lose_ID FROM match_list WHERE ID = %s"
            mycursor.execute(lose, tup_i)
            str_lose = mycursor.fetchone()[0]
            str_lose = str(str_lose)
            tup_str_lose = str_lose,
            update_school_games_l = "UPDATE school SET games = games + 1 WHERE school_name = %s"
            update_school_losses = "UPDATE school SET losses = losses + 1 WHERE school_name = %s"
            mycursor.execute(update_school_games_l, tup_str_lose)
            mycursor.execute(update_school_losses, tup_str_lose)
            #should execute only if it's a tie
        if tie_scenario in school_names:
            tie_1 = "SELECT Tie_ID_1 FROM match_list WHERE ID = %s"
            mycursor.execute(tie_1, tup_i)
            str_tie_1 = mycursor.fetchone()[0]
            str_tie_1 = str(str_tie_1)
            tup_str_tie_1 = str_tie_1,
            tie_2 = "SELECT Tie_ID_2 FROM match_list WHERE ID = %s"
            mycursor.execute(tie_2, tup_i)
            str_tie_2 = mycursor.fetchone()[0]
            str_tie_2 = str(str_tie_2)
            tup_str_tie_2 = str_tie_2,
            update_ties = "UPDATE school SET ties = ties + 1 WHERE school_name = %s"
            update_games = "UPDATE school SET games = games + 1 WHERE school_name = %s"
            mycursor.execute(update_ties, tup_str_tie_1)
            mycursor.execute(update_ties, tup_str_tie_2)
            mycursor.execute(update_games, tup_str_tie_1)
            mycursor.execute(update_games, tup_str_tie_2)
            #class wins
        if win_scenario in school_names:
            class_check = "SELECT school.class, preliminary_index.points FROM school JOIN preliminary_index ON school.class = preliminary_index.class WHERE school.school_name = %s"
            mycursor.execute(class_check, tup_str_lose)
            str_class_check = mycursor.fetchone()[0]
            str_class_check = str(str_class_check)
            if str_class_check == "AA":
                class_check_column = "AA_Wins"
            elif str_class_check == "A":
                class_check_column = "A_Wins"
            elif str_class_check == "B":
                class_check_column = "B_Wins"
            elif str_class_check == "C":
                class_check_column = "C_Wins"
            elif str_class_check == "D":
                class_check_column = "D_Wins"
            #string replacement used because previous methods couldn't be used to pass variable column names to MySQL database
            mycursor.execute("UPDATE school SET %s = %s + 1 WHERE school_name = '%s'" % (class_check_column, class_check_column, str_win))
        if tie_scenario in school_names:
            class_check = "SELECT school.class, preliminary_index.points FROM school JOIN preliminary_index ON school.class = preliminary_index.class WHERE school.school_name = %s"
            mycursor.execute(class_check, tup_str_tie_1)
            str_class_check = mycursor.fetchone()[0]
            str_class_check = str(str_class_check)
            if str_class_check == "AA":
                class_check_column = "AA_Wins"
            elif str_class_check == "A":
                class_check_column = "A_Wins"
            elif str_class_check == "B":
                class_check_column = "B_Wins"
            elif str_class_check == "C":
                class_check_column = "C_Wins"
            elif str_class_check == "D":
                class_check_column = "D_Wins"
            #string replacement used because previous methods couldn't be used to pass variable column names to MySQL database
            mycursor.execute("UPDATE school SET %s = %s + 0.5 WHERE school_name = '%s'" % (class_check_column, class_check_column, str_tie_2))
            class_check = "SELECT school.class, preliminary_index.points FROM school JOIN preliminary_index ON school.class = preliminary_index.class WHERE school.school_name = %s"
            mycursor.execute(class_check, tup_str_tie_2)
            str_class_check = mycursor.fetchone()[0]
            str_class_check = str(str_class_check)
            if str_class_check == "AA":
                class_check_column = "AA_Wins"
            elif str_class_check == "A":
                class_check_column = "A_Wins"
            elif str_class_check == "B":
                class_check_column = "B_Wins"
            elif str_class_check == "C":
                class_check_column = "C_Wins"
            elif str_class_check == "D":
                class_check_column = "D_Wins"
            #string replacement used because previous methods couldn't be used to pass variable column names to MySQL database
            mycursor.execute("UPDATE school SET %s = %s + 0.5 WHERE school_name = '%s'" % (class_check_column, class_check_column, str_tie_1))
        i += 1
    PI_summation(points)
    TI_summation(school_names)
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
def make_SoS_calculations(str_rating_sheet, column_number):

    rating_sheet = client.open('PowerRatings').worksheet(str_rating_sheet)
    str_match_list_sheet = str_rating_sheet + 'MatchList'
    #update_matches(str_match_list_sheet)
    
    school_names = []

    rating_sheet.clear()
    rating_sheet.insert_row(["Rank (within division)", "School Name", "Class", "Region", "Wins", "Losses", "Ties", "Games", "AA Wins", "A Wins", "B Wins", "C Wins", "D Wins", "PI", "TI", "SoS", "SoS_heal", "SoS2", "SoS2_Heal", "GameWP", "PointWP", "GWP_Over_PWP", "PowerR"])

    mycursor.execute("SELECT MAX(ID) FROM school")
    max_match = mycursor.fetchone()[0]
    max_match = int(max_match)

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

        power_rating = (3 * games_win_ratio + 1 * points_win_ratio) * current_SoS2_heal_combined / 4

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

    ranks = []
    clear_color_range = "A1:W" + str(len(school_names) + 5)
    sort_range = "A2:W" + str(len(school_names))
    all_results_range = "A2:W" + str(len(school_names) + 1)

    rating_sheet.append_rows(school_list_sheet, table_range='B2')
    rating_sheet.format(clear_color_range, {"backgroundColor": {"red": 1, "green": 1, "blue": 1}})
    #below sorts first by class, then region, then by tournament index
    rating_sheet.sort((3, 'asc'), (4, 'asc'), (column_number, 'des'), range=sort_range)

    #no_bold_range = 'A2:W' + '3'
    #rating_sheet.format(no_bold_range, {"textFormat": {"bold": False}})
    #rating_sheet.format('A1:W1', {"textFormat": {"bold": True}})
    rating_sheet.freeze(rows=1, cols=2)

    all_results = rating_sheet.batch_get([all_results_range])
    #[a][b][c]
    #a must be zero as the outer list contains one element
    #b refers to relative school ID number
    #c refers to school trait

    rank = 0
    i = 0
    while True:
        try:
            if all_results[0][i][2] == all_results[0][i+1][2] and all_results[0][i][3] == all_results[0][i+1][3]:
                i += 1
                rank = rank + 1
                ranks.append([rank])
            else:
                i += 1
                rank = rank + 1
                ranks.append([rank])
                rank = 0
        #below assumes that a team will not exist as the sole team in its class/region combo
        except IndexError: 
            if all_results[0][i][2] == all_results[0][i-1][2] and all_results[0][i][3] == all_results[0][i-1][3]:
                rank = ranks[len(ranks) - 1][0] + 1
            else:
                rank = 1
            ranks.append([rank])
            break
    rating_sheet.append_rows(ranks, table_range='A2')


    print("PowerRating Google sheet updated")

#school_setup(update_matches('GTennis2022MatchList'))
#make_SoS_calculations('GTennis2022')

school_setup(update_matches('BBasketball2023MatchList'))
#int param determines sort: 15 for TI, 23 for PowerR
make_SoS_calculations('BBasketball2023', 23)

print("done")
mydb.close()