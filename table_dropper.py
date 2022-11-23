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
drop_temp_match_list_query = "DROP TABLE %s" % (temp_match_list_name)
drop_school_query = "DROP TABLE %s" % (school_name)
drop_match_list_query = "DROP TABLE %s" % (match_list_name)
mycursor.execute(drop_temp_match_list_query)
mycursor.execute(drop_school_query)
mycursor.execute(drop_match_list_query)
print("temporary tables dropped")
mydb.close