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
school_query = "CREATE TABLE %s like school" % (school_name)
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
        print(school_table[match_ID - 1])
        match_ID += 1
print_match_list()
print_school()
drop_temp_match_list_query = "DROP TABLE %s" % (temp_match_list_name)
drop_school_query = "DROP TABLE %s" % (school_name)
drop_match_list_query = "DROP TABLE %s" % (match_list_name)
mycursor.execute(drop_temp_match_list_query)
mycursor.execute(drop_school_query)
mycursor.execute(drop_match_list_query)
mydb.close