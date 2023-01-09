import gspread
from oauth2client.service_account import ServiceAccountCredentials
import mysql.connector
import csv
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

#ABOVE BLOCK DOES NOT NEED TO BE COPIED

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

school_setup(update_matches('GTennis2022MatchList'))
print("done")

mydb.close