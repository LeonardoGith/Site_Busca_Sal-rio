from flask import Flask, render_template, request
import sqlite3

from dados import databasehelper

# Function to get the average salary from the SQLite database
def calculate_average_salary(region, profession, db_name=databasehelper.database_name()):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Query to get the average salary for the specified region and profession
    cursor.execute('''SELECT AVG(salary) FROM profession_data
                      WHERE region_id = ? AND profession_id = ?''', (region, profession))
    
    result = cursor.fetchone()
    conn.close()
    
    # If a result is found, return the average salary
    if result[0] is not None:
        return round(result[0], 2)
    else:
        return None
