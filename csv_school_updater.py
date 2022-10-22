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
#clear school
mycursor.execute("delete from school")
file_name = input("What is the file name being used? Include .csv in the name: ")
#open csv file with match data
with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter = ',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(row[0], row[1], row[2], row[3])
            s_ID = row[0]
            s_school_name = row[1]
            s_class = row[2]
            s_region = row[3]
            school_send = "insert into school (ID, school_name, class, region) values (%s, %s, %s, %s)"
            school_val = (s_ID, s_school_name, s_class, s_region)
            mycursor.execute(school_send, school_val)
            line_count += 1
    print(f'Processed {line_count} lines.')