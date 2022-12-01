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

#generate list of all schools/teams in system
i = 1
while i <= max_match:
    new_school_name = get_current_school_name(i)
    school_names.append(new_school_name)
    i += 1

for i in range(len(school_names)):
    games_total_dict = {}
    class_wins_dict = {}
    games_against_dict = {}
    match_duplicate_list = []

    current_school = get_current_school_name(i + 1)

    try:
        win_query = "SELECT Lose_ID FROM match_list WHERE Win_ID = '%s'" % ("Waterville") #current_school not Waterville
        mycursor.execute(win_query)
        win_teams = mycursor.fetchall()
        for ii in range(len(win_teams)):
            games_against_dict[win_teams[ii][0]] = 0
            match_duplicate_list.append(win_teams[ii][0])
    except:
        pass
    try:
        lose_query = "SELECT Win_ID FROM match_list WHERE Lose_ID = '%s'" % ("Waterville") #current_school not Waterville
        mycursor.execute(lose_query)
        lose_teams = mycursor.fetchall()
        for ii in range(len(lose_teams)):
            games_against_dict[lose_teams[ii][0]] = 0
            match_duplicate_list.append(lose_teams[ii][0])
    except:
        pass
    try:
        tie_1_query = "SELECT Tie_ID_1 FROM match_list WHERE Tie_ID_2 = '%s'" % ("Waterville") #current_school not Waterville
        mycursor.execute(tie_1_query)
        tie_1_teams = mycursor.fetchall()
        for ii in range(len(tie_1_teams)):
            games_against_dict[tie_1_teams[ii][0]] = 0
            match_duplicate_list.append(tie_1_teams[ii][0])
    except:
        pass
    try:
        tie_2_query = "SELECT Tie_ID_2 FROM match_list WHERE Tie_ID_1 = '%s'" % ("Waterville") #current_school not Waterville
        mycursor.execute(tie_2_query)
        tie_2_teams = mycursor.fetchall()
        for ii in range(len(tie_2_teams)):
            games_against_dict[tie_2_teams[ii][0]] = 0
            match_duplicate_list.append(tie_2_teams[ii][0])
    except:
        pass
    for ii in range(len(match_duplicate_list)):
        games_against_dict[match_duplicate_list[ii]] = match_duplicate_list.count(match_duplicate_list[ii])
    #above, number of matches played against each school has been obtained and is contained in games_against_dict
    class_wins_dict = games_against_dict.copy()
    match_duplicate_list = [*set(match_duplicate_list)]
    for ii in range(len(class_wins_dict)):
        class_wins_dict[match_duplicate_list[ii]] = #here i'll need to set dict key (like "Medomak" equal to list of class win values [AA, A, B, C, D] pulled from mysql)

print(class_wins_dict)
#print(class_wins_dict)