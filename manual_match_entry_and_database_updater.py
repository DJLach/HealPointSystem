import mysql.connector
#connect to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="heal")
mycursor = mydb.cursor()
mydb.autocommit = True
#defines function for calculating PI values based on wins and updating the school table
points = [42, 40, 38, 36, 34] #update to take values from database
def PI_summation():
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
    PI_sum = PI_sum + (AA_count * points[0]) #replace counts with class_points = [AA_points, A_points, B_points, C_points, D_points]
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
def TI_summation():
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
#get all class point values (will be user-alterable in future version, hence why these are not static set variables)
str_class = ['AA', 'A', 'B', 'C', 'D']
AA_points = A_points = B_points = C_points = D_points = 0
class_points = [AA_points, A_points, B_points, C_points, D_points]
i = 0
while i < len(str_class):
  tup_str_class = str_class[i],
  point_value_get = "SELECT points FROM preliminary_index WHERE class = %s"
  mycursor.execute(point_value_get, tup_str_class)
  class_points[i] = mycursor.fetchone()[0]
  i+=1
#set list of schools
school_names = []
school_count = 1
mycursor.execute("select count(*) from school")
row_total = mycursor.fetchone()[0]
while school_count <= row_total:
    school_select = "SELECT school_name FROM school WHERE ID = %s"
    tup_school_count = school_count,
    mycursor.execute(school_select, tup_school_count)
    current_school_name = mycursor.fetchone()[0]
    school_names.append(current_school_name)
    school_count += 1
#initialize choice variables at arbitrary string
choice = choice_2 = "~~~"
#set user command options
choices = ["Y", "y", "N", "n"]
#set application end condition to false to start
end = False
while choice not in choices: #user prompt
  choice = input("Do you have games/matches to add? y/n ")
  while end == False:
    if choice == "Y" or choice == "y":
      #check number of matches to determine what new match_ID value should be
      match_number = "SELECT COUNT(ID) FROM match_list"
      mycursor.execute(match_number)
      int_match = mycursor.fetchone()[0]
      int_match = int(int_match)
      int_match += 1
      #user input for game/match entry
      win_or_tie = input ("Is this a win or a tie? w/t ")
      if win_or_tie == "T" or win_or_tie == "t":
        tie_school_1 = input ("First team that tied: ")
        tie_school_2 = input ("Second team that tied: ")
        #enter match result into match_list if tie
        match_entry = "INSERT INTO Match_List (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, %s, %s)"
        str_match_number = str(int_match)
        val = (str_match_number, tie_school_1, tie_school_2)
        mycursor.execute(match_entry, val)
        #print(mycursor.rowcount, "game/match result recorded")
      elif win_or_tie == "W" or win_or_tie == "w":
        win_school = input ("Winning team name: ")
        lose_school = input ("Losing team name: ")
        #enter result into match_list table if win
        match_entry = "INSERT INTO Match_List (ID, Win_ID, Lose_ID) VALUES (%s, %s, %s)"
        str_match_number = str(int_match)
        val = (str_match_number, win_school, lose_school)
        mycursor.execute(match_entry, val)
        #print(mycursor.rowcount, "game/match result recorded")
      else:
        print ("This is not a valid command.")
      choice = input("Would you like to add another game/match result? Y/N ")
      if choice == "Y" or choice == "y":
        end = False    
    else:
      choice_2 = input("Would you like to update match results to the school table? y/n ")
      if choice_2 == "Y" or choice_2 == "y":
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
        PI_summation()
        TI_summation()
        print("done")
        end = True
    if choice_2 != "~~~":
      end = True
mydb.close