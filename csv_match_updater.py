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
#clear match_list
mycursor.execute("delete from match_list")
file_name = input("What is the file name being used? Include .csv in the name: ")
#2022_boystennis_match_list.csv
#open csv file with match data
with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row[0], row[1], row[2], row[3], row[4])
            m_ID = row[0]
            m_Win_ID = row[1]
            m_Lose_ID = row[2]
            m_Tie_ID_1 = row[3]
            m_Tie_ID_2 = row[4]
            match_send = "insert into match_list (ID, Win_ID, Lose_ID, Tie_ID_1, Tie_ID_2) values (%s, %s, %s, %s, %s)"
            match_val = (m_ID, m_Win_ID, m_Lose_ID, m_Tie_ID_1, m_Tie_ID_2)
            mycursor.execute(match_send, match_val)
            line_count += 1
    print(f'Processed {line_count} lines.')
mydb.close