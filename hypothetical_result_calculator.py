import decimal
from decimal import Decimal
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
user_ID = "hyp" #will eventually be updated to be unique to user w/ randomized value (from current date/time?)
#generate new table names based on unique identifier
temp_match_list_name = user_ID + "_temp_match_list"
school_name = user_ID + "_school"
match_list_name = user_ID + "_match_list"
#create new temporary tables
temp_match_list_query = "CREATE TABLE %s like temp_match_list" % (temp_match_list_name)
school_query = "CREATE TABLE %s AS SELECT * FROM school" % (school_name)
match_list_query = "CREATE TABLE %s AS SELECT * FROM match_list" % (match_list_name)
mycursor.execute(temp_match_list_query)
mycursor.execute(school_query)
mycursor.execute(match_list_query)

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

def print_match_list():
    #define function to print user_ID_match_list table to console
    mycursor.execute("SELECT MAX(ID) FROM %s" % (match_list_name))
    max_ID = mycursor.fetchone()[0]
    mycursor.execute("SELECT * FROM %s" % (match_list_name))
    match_list_table = mycursor.fetchall()
    match_ID = 1
    while match_ID <= max_ID:
        print(match_list_table[match_ID - 1])
        match_ID += 1
def print_school():
    #define function to print user_ID_school table to console
    mycursor.execute("SELECT MAX(ID) from %s" % (school_name))
    max_ID = mycursor.fetchone()[0]
    mycursor.execute("SELECT * FROM %s" % (school_name))
    school_table = mycursor.fetchall()
    school_ID = 1
    while school_ID <= max_ID:
        print(school_table[school_ID - 1])
        school_ID += 1
def PI_summation():
  max_number = "SELECT MAX(ID) FROM %s" % (school_name)
  mycursor.execute(max_number)
  max_match = mycursor.fetchone()[0]
  max_match = int(max_match)
  i = 1
  while i <= max_match:
    #tup_i = i,
    PI_sum = 0
    #find sum of all prelminary index values for each school
    AA_get = "SELECT AA_Wins FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(AA_get)
    AA_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (AA_count * 42) #replace counts with class_points = [AA_points, A_points, B_points, C_points, D_points]
    A_get = "SELECT A_Wins FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(A_get)
    A_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (A_count * 40)
    B_get = "SELECT B_Wins FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(B_get)
    B_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (B_count * 38)
    C_get = "SELECT C_Wins FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(C_get)
    C_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (C_count * 36)
    D_get = "SELECT D_Wins FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(D_get)
    D_count = mycursor.fetchone()[0]
    PI_sum = PI_sum + (D_count * 34)
    #divde total PI summed values by number of games to get current PI for a given school
    game_query = "SELECT games FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(game_query)
    game_count = mycursor.fetchone()[0]
    if game_count != 0:
      PI_sum = PI_sum / game_count
      if PI_sum < 1:
        PI_sum = 1
    else:
      PI_sum = 1
    PI_update = "UPDATE %s SET PI = %s WHERE ID = %s" % (school_name, PI_sum, i)
    mycursor.execute(PI_update)
    i += 1
def TI_summation():
  i = 1
  while i <= len(school_names):
    delete_from_temp_match_list = "DELETE FROM %s" % (temp_match_list_name)
    mycursor.execute(delete_from_temp_match_list)
    #find winning team name and number of wins
    #primary_team = i,
    select_school_name = "SELECT school_name FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(select_school_name)
    pri_name = mycursor.fetchone()[0]
    #pri_name_2 = pri_name,
    select_lose_ID = "SELECT Lose_ID FROM %s WHERE WIN_ID = '%s'" % (match_list_name, pri_name)
    mycursor.execute(select_lose_ID)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain wins for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      mycursor.execute(select_lose_ID)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      str_c = str(c)
      match_entry = "INSERT INTO %s (ID, Win_ID, Lose_ID) VALUES (%s, '%s', '%s')" % (temp_match_list_name, str_c, pri_name, sec_name)
      mycursor.execute(match_entry)
      c += 1
    #add wins to TI
    d = 1
    TI_sum = 0
    while d <= temp_length:
      #tup_d = d,
      select_lose_ID_temp = "SELECT Lose_ID FROM %s WHERE ID = %s" % (temp_match_list_name, d)
      mycursor.execute(select_lose_ID_temp)
      sec_name = mycursor.fetchone()[0]
      select_PI = "SELECT PI FROM %s WHERE school_name = '%s'" % (school_name, sec_name)
      #tup_sec_name = sec_name,
      mycursor.execute(select_PI)
      sec_PI = mycursor.fetchone()[0]
      TI_sum = TI_sum + sec_PI
      d += 1
    #clears data from temp_match table
    mycursor.execute(delete_from_temp_match_list)
    #find tie team name (when team 1) and number of ties as team 1
    primary_team = i
    #tup_primary_team = i,
    select_school_name_query = "SELECT school_name FROM %s WHERE ID = %s" % (school_name, i)
    mycursor.execute(select_school_name_query)
    pri_name = mycursor.fetchone()[0]
    #tup_pri_name = pri_name,
    select_tie_ID_2 = "SELECT Tie_ID_2 FROM %s WHERE Tie_ID_1 = '%s'" % (match_list_name, pri_name)
    mycursor.execute(select_tie_ID_2)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain ties for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      mycursor.execute(select_tie_ID_2)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      str_c = str(c)
      match_entry = "INSERT INTO %s (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, '%s', '%s')" % (temp_match_list_name, str_c, pri_name, sec_name)
      #val = (str_c, pri_name, sec_name)
      mycursor.execute(match_entry)
      c += 1
    #add ties to TI
    d = 1
    while d <= temp_length:
      #tuple_d = d,
      s_t_2 = "SELECT Tie_ID_2 FROM %s WHERE ID = %s" % (temp_match_list_name, d)
      mycursor.execute(s_t_2)
      sec_name = mycursor.fetchone()[0]
      #tuple_sec_name = sec_name,
      select_PI = "SELECT PI FROM %s WHERE school_name = '%s'" % (school_name, sec_name)
      mycursor.execute(select_PI)
      sec_PI = mycursor.fetchone()[0]
      #only half the PI is used because it's a tie, not a win
      sec_PI = sec_PI / 2
      TI_sum = TI_sum + sec_PI
      d += 1
    mycursor.execute(delete_from_temp_match_list)
    #find tie team name (when team 2) and number of ties as team 2
    primary_team = i
    #t_p_t = primary_team,
    s_s_n = "SELECT school_name FROM %s WHERE ID = %s" % (school_name, primary_team)
    mycursor.execute(s_s_n)
    pri_name = mycursor.fetchone()[0]
    #tuple_pri_name = pri_name,
    s_t_1 = "SELECT Tie_ID_1 FROM %s WHERE Tie_ID_2 = '%s'" % (match_list_name, pri_name)
    mycursor.execute(s_t_1)
    temp_length = len(mycursor.fetchall())
    #update temp_match_list to contain ties for a given team and provide iterating list
    c = 1
    while c <= temp_length:
      #t_p_n = pri_name,
      s_t_i_1 = "SELECT TIE_ID_1 FROM %s WHERE Tie_ID_2 = '%s'" % (match_list_name, pri_name)
      mycursor.execute(s_t_i_1)
      sec_name_tuple = mycursor.fetchall()[c-1]
      sec_name = "".join(sec_name_tuple)
      str_c = str(c)
      match_entry = "INSERT INTO %s (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, '%s', '%s')" % (temp_match_list_name, str_c, pri_name, sec_name)
      #val = (str_c, pri_name, sec_name)
      mycursor.execute(match_entry)
      c += 1
    #add ties to TI
    d = 1
    while d <= temp_length:
      #t_d = d,
      s_t_i_2 = "SELECT Tie_ID_2 FROM %s WHERE ID = %s" % (temp_match_list_name, d)
      mycursor.execute(s_t_i_2)
      sec_name = mycursor.fetchone()[0]
      #s_n = sec_name,
      s_PI = "SELECT PI FROM %s WHERE school_name = '%s'" % (school_name, sec_name)
      mycursor.execute(s_PI)
      sec_PI = mycursor.fetchone()[0]
      #only half the PI is used because it's a tie, not a win
      sec_PI = sec_PI / 2
      #print (sec_PI)
      TI_sum = TI_sum + sec_PI
      d += 1
    #TI = sum of defeated PI / games played * 10
    #t_primary_team = primary_team,
    s_g = "SELECT games FROM %s WHERE ID = %s" % (school_name, primary_team)
    mycursor.execute(s_g)
    game_count = mycursor.fetchone()[0]
    if game_count != 0:
      TI_sum = 10 * TI_sum / game_count
    else:
      TI_sum = 0
    #tup_TI_pri = (TI_sum, primary_team)
    u_s_s = "UPDATE %s SET TI = %s WHERE ID = %s" % (school_name, TI_sum, primary_team)
    mycursor.execute(u_s_s)
    #print (TI_sum)
    i += 1
def index_reset():
  #reset PI/TI in user_ID_temp_school table
  reset_PI = "UPDATE %s SET PI = 0" % (school_name)
  reset_TI = "UPDATE %s SET TI = 0" % (school_name)
  mycursor.execute(reset_PI)
  mycursor.execute(reset_TI)

  print ("resetting PI and TI values. . .")
def add_matches():
  max_ID_query = "SELECT MAX(ID) FROM %s" % (match_list_name)
  mycursor.execute(max_ID_query)
  max_ID = mycursor.fetchone()[0]
  match_number = max_ID + 1
  choice = input("Do you have games/matches to add? y/n ")
  while choice == "y" or choice == "Y":
    win_or_tie = input ("Is this a win or a tie? w/t ")
    if win_or_tie == "T" or win_or_tie == "t":
      tie_school_1 = input ("First team that tied: ") #input sanitization needed here -> check against school[] array to confirm it's in it and to avoid SQL injection
      tie_school_2 = input ("Second team that tied: ")
      #enter match result into match_list if tie
      str_match_number = str(match_number)
      #if in school[]
      match_entry = "INSERT INTO %s (ID, Tie_ID_1, Tie_ID_2) VALUES (%s, '%s', '%s')" % (match_list_name, str_match_number, tie_school_1, tie_school_2)
      mycursor.execute(match_entry)
      print(mycursor.rowcount, "game/match result recorded")
      #update ties in class_ID_school table
      tie_class_query_1 = "SELECT class FROM %s WHERE school_name = '%s'" % (school_name, tie_school_1)
      tie_class_query_2 = "SELECT class FROM %s WHERE school_name = '%s'" % (school_name, tie_school_2)
      mycursor.execute(tie_class_query_1)
      tie_class_1 = mycursor.fetchone()[0]
      tie_class_1 = str(tie_class_1)
      mycursor.execute(tie_class_query_2)
      tie_class_2 = mycursor.fetchone()[0]
      tie_class_2 = str(tie_class_2)
      class_win_column_1 = tie_class_2 + "_wins" #swap necessary because opponent's class is what matters
      class_win_column_2 = tie_class_1 + "_wins"
      number_class_wins_query_1 = "SELECT %s FROM %s WHERE school_name = '%s'" % (class_win_column_1, school_name, tie_school_1)
      number_class_wins_query_2 = "SELECT %s FROM %s WHERE school_name = '%s'" % (class_win_column_2, school_name, tie_school_2)
      mycursor.execute(number_class_wins_query_1)
      number_class_wins_1 = mycursor.fetchone()[0]
      number_class_wins_1 = Decimal(number_class_wins_1)
      number_class_wins_1 = number_class_wins_1 + Decimal(0.5)
      mycursor.execute(number_class_wins_query_2)
      number_class_wins_2 = mycursor.fetchone()[0]
      number_class_wins_2 = Decimal(number_class_wins_2)
      number_class_wins_2 = number_class_wins_2 + Decimal(0.5)
      update_class_wins_query_1 = "UPDATE %s SET %s = %s WHERE school_name = '%s'" % (school_name, class_win_column_1, number_class_wins_1, tie_school_1)
      update_class_wins_query_2 = "UPDATE %s SET %s = %s WHERE school_name = '%s'" % (school_name, class_win_column_2, number_class_wins_2, tie_school_2)
      mycursor.execute(update_class_wins_query_1)
      mycursor.execute(update_class_wins_query_2)
      
      number_ties_query_1 = "SELECT ties FROM %s WHERE school_name = '%s'" % (school_name, tie_school_1)
      number_ties_query_2 = "SELECT ties FROM %s WHERE school_name = '%s'" % (school_name, tie_school_2)
      mycursor.execute(number_ties_query_1)
      number_ties_1 = mycursor.fetchone()[0]
      number_ties_1 += 1 #increase ties by 1
      mycursor.execute(number_ties_query_2)
      number_ties_2 = mycursor.fetchone()[0]
      number_ties_2 += 1 #increase ties by 1
      update_ties_query_1 = "UPDATE %s SET ties = %s WHERE school_name = '%s'" % (school_name, number_ties_1, tie_school_1)
      update_ties_query_2 = "UPDATE %s SET ties = %s WHERE school_name = '%s'" % (school_name, number_ties_2, tie_school_2)
      mycursor.execute(update_ties_query_1)
      mycursor.execute(update_ties_query_2)

      number_games_query_1 = "SELECT games from %s WHERE school_name = '%s'" % (school_name, tie_school_1)
      number_games_query_2 = "SELECT games from %s WHERE school_name = '%s'" % (school_name, tie_school_2)
      mycursor.execute(number_games_query_1)
      number_games_1 = mycursor.fetchone()[0]
      number_games_1 += 1 #increases games by 1
      mycursor.execute(number_games_query_2)
      number_games_2 = mycursor.fetchone()[0]
      number_games_2 += 1 #increase games by 1
      update_games_query_1 = "UPDATE %s SET games = %s WHERE school_name = '%s'" % (school_name, number_games_1, tie_school_1)
      update_games_query_2 = "UPDATE %s SET games = %s WHERE school_name = '%s'" % (school_name, number_games_2, tie_school_2)
      mycursor.execute(update_games_query_1)
      mycursor.execute(update_games_query_2)

    elif win_or_tie == "W" or win_or_tie == "w":
      win_school = input ("Winning team name: ")
      lose_school = input ("Losing team name: ")
      #enter result into match_list table if win
      str_match_number = str(match_number)
      #if in school[]
      match_entry = "INSERT INTO %s (ID, Win_ID, Lose_ID) VALUES (%s, '%s', '%s')" % (match_list_name, str_match_number, win_school, lose_school)
      mycursor.execute(match_entry)
      print(mycursor.rowcount, "game/match result recorded")

      #update wins/losses in class_ID_school table
      loss_class_query = "SELECT class FROM %s WHERE school_name = '%s'" % (school_name, lose_school)
      mycursor.execute(loss_class_query)
      loss_class = mycursor.fetchone()[0]
      loss_class = str(loss_class)
      class_win_column = loss_class + "_wins"
      number_class_wins_query = "SELECT %s FROM %s WHERE school_name = '%s'" % (class_win_column, school_name, win_school)
      mycursor.execute(number_class_wins_query)
      number_class_wins = mycursor.fetchone()[0]
      number_class_wins = int(number_class_wins)
      number_class_wins = number_class_wins + 1
      update_class_wins_query = "UPDATE %s SET %s = %s WHERE school_name = '%s'" % (school_name, class_win_column, number_class_wins, win_school)
      mycursor.execute(update_class_wins_query)
      
      number_wins_query = "SELECT wins FROM %s WHERE school_name = '%s'" % (school_name, win_school)
      number_losses_query = "SELECT losses FROM %s WHERE school_name = '%s'" % (school_name, lose_school)
      mycursor.execute(number_wins_query)
      number_wins = mycursor.fetchone()[0]
      number_wins += 1 #increase ties by 1
      mycursor.execute(number_losses_query)
      number_losses = mycursor.fetchone()[0]
      number_losses += 1 #increase ties by 1
      update_wins_query = "UPDATE %s SET wins = %s WHERE school_name = '%s'" % (school_name, number_wins, win_school)
      update_losses_query = "UPDATE %s SET losses = %s WHERE school_name = '%s'" % (school_name, number_losses, lose_school)
      mycursor.execute(update_wins_query)
      mycursor.execute(update_losses_query)

      number_games_query_1 = "SELECT games from %s WHERE school_name = '%s'" % (school_name, win_school)
      number_games_query_2 = "SELECT games from %s WHERE school_name = '%s'" % (school_name, lose_school)
      mycursor.execute(number_games_query_1)
      number_games_1 = mycursor.fetchone()[0]
      number_games_1 += 1 #increases games by 1
      mycursor.execute(number_games_query_2)
      number_games_2 = mycursor.fetchone()[0]
      number_games_2 += 1 #increase games by 1
      update_games_query_1 = "UPDATE %s SET games = %s WHERE school_name = '%s'" % (school_name, number_games_1, win_school)
      update_games_query_2 = "UPDATE %s SET games = %s WHERE school_name = '%s'" % (school_name, number_games_2, lose_school)
      mycursor.execute(update_games_query_1)
      mycursor.execute(update_games_query_2)

    else:
      print ("This is not a valid command.")
    choice = input("Would you like to add another game/match result? Y/N ")
    if choice == "Y" or choice == "y":
      match_number += 1
index_reset()
add_matches()
PI_summation()
TI_summation()

#print_match_list()
#print_school()

#drop_temp_match_list_query = "DROP TABLE %s" % (temp_match_list_name)
#drop_school_query = "DROP TABLE %s" % (school_name)
#drop_match_list_query = "DROP TABLE %s" % (match_list_name)
#mycursor.execute(drop_temp_match_list_query)
#mycursor.execute(drop_school_query)
#mycursor.execute(drop_match_list_query)
mydb.close

#update user_ID_school with wins, losses, ties, and class wins