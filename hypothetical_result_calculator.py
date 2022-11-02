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
def index_reset():
  #reset PI/TI in user_ID_temp_school table
  reset_PI = "UPDATE %s SET PI = 0" % (school_name)
  reset_TI = "UPDATE %s SET TI = 0" % (school_name)
  mycursor.execute(reset_PI)
  mycursor.execute(reset_TI)

  print ("resetting PI and TI values. . .")

index_reset()

#print_match_list()
#print_school()

#drop_temp_match_list_query = "DROP TABLE %s" % (temp_match_list_name)
#drop_school_query = "DROP TABLE %s" % (school_name)
#drop_match_list_query = "DROP TABLE %s" % (match_list_name)
#mycursor.execute(drop_temp_match_list_query)
#mycursor.execute(drop_school_query)
#mycursor.execute(drop_match_list_query)
mydb.close

#reset JUST PI and TI of school table for new school table
#add any wins/ties (find the max_ID from match list first and iterate from there)
#recalculate PI and TI