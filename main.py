# ============================================================
# MORINGA SCHOOL - MODULE 5
# LAB: GETTING STARTED WITH DATABASES AND SQL
# ============================================================

# This application demonstrates how to connect to an SQLite
# database and retrieve or transform information using SQL.
#
# Concepts covered:
# 1. Database connections
# 2. SELECT statements
# 3. Column ordering
# 4. Column aliases
# 5. CASE statements
# 6. String functions
# 7. Numeric functions
# 8. Date functions


# ============================================================
# STEP 1A: IMPORT REQUIRED LIBRARIES
# ============================================================

# sqlite3 allows Python to communicate with SQLite databases.
import sqlite3

# pandas allows us to read SQL query results into DataFrames.
import pandas as pd

# pathlib helps us locate the database file reliably.
from pathlib import Path


# ============================================================
# STEP 1B: CONNECT TO THE SQLITE DATABASE
# ============================================================

# Locate the directory containing this Python script.
BASE_DIR = Path(__file__).resolve().parent

# Build the full path to the provided database.
DATABASE_PATH = BASE_DIR / "data.sqlite"

# Establish a connection to the SQLite database.
# Store the connection in the variable expected by the tests.
conn = sqlite3.connect(DATABASE_PATH)


# ============================================================
# STEP 2: SELECT EMPLOYEE NUMBER AND LAST NAME
# ============================================================

# Problem:
# Retrieve the employee number and last name of all employees.
#
# Requirements:
# 1. Return only two columns.
# 2. employeeNumber must appear first.
# 3. lastName must appear second.
#
# SQL Concepts:
# SELECT - specifies columns to retrieve.
# FROM   - identifies the database table.

df_first_five = pd.read_sql(
    """
    SELECT
        employeeNumber,
        lastName
    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 3: REVERSE THE COLUMN ORDER
# ============================================================

# Problem:
# Retrieve the same employee information as Step 2.
#
# This time:
# 1. lastName appears first.
# 2. employeeNumber appears second.
#
# The order in which columns appear in SELECT determines
# their order in the returned DataFrame.

df_five_reverse = pd.read_sql(
    """
    SELECT
        lastName,
        employeeNumber
    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 4: ALIAS THE EMPLOYEE NUMBER COLUMN
# ============================================================

# Problem:
# Retrieve the employee last name and employee number.
#
# Rename employeeNumber to ID.
#
# SQL Concept:
# AS creates an alias for a selected column.
#
# The alias changes the column name in the query results,
# not the original database table.

df_alias = pd.read_sql(
    """
    SELECT
        lastName,
        employeeNumber AS ID
    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 5: CLASSIFY EMPLOYEES USING CASE
# ============================================================

# Problem:
# Classify employees into two categories.
#
# Executive:
# - President
# - VP Sales
# - VP Marketing
#
# Not Executive:
# - All other job titles
#
# SQL Concept:
# CASE allows us to create conditional logic inside SQL.
#
# IN checks whether a value matches any value in a list.
#
# END AS role names the newly generated column.

df_executive = pd.read_sql(
    """
    SELECT
        employeeNumber,
        lastName,
        jobTitle,

        CASE
            WHEN jobTitle IN (
                'President',
                'VP Sales',
                'VP Marketing'
            )
            THEN 'Executive'

            ELSE 'Not Executive'

        END AS role

    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 6: CALCULATE LAST NAME LENGTHS
# ============================================================

# Problem:
# Find the number of characters in each employee's last name.
#
# Requirements:
# 1. Return only one column.
# 2. Name the column name_length.
#
# SQL Concept:
# LENGTH() returns the length of a string.
#
# Example:
# LENGTH('Murphy') returns 6.

df_name_length = pd.read_sql(
    """
    SELECT
        LENGTH(lastName) AS name_length
    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 7: EXTRACT THE FIRST TWO JOB TITLE CHARACTERS
# ============================================================

# Problem:
# Retrieve the first two characters of each job title.
#
# Requirements:
# 1. Return only one column.
# 2. Name the column short_title.
#
# SQL Concept:
# SUBSTR() extracts a portion of a string.
#
# SUBSTR(jobTitle, 1, 2)
#
# 1 = Starting character position.
# 2 = Number of characters to extract.
#
# Example:
# President becomes Pr.

df_short_title = pd.read_sql(
    """
    SELECT
        SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees;
    """,
    conn
)


# ============================================================
# STEP 8: CALCULATE TOTAL ORDER VALUE
# ============================================================

# Problem:
# Calculate the total amount for all orders.
#
# For each order detail:
#
# Total Price = priceEach * quantityOrdered
#
# Requirements:
# 1. Multiply the unit price by the quantity ordered.
# 2. Round each calculated total.
# 3. Add all rounded totals together.
#
# SQL Concept:
# ROUND() rounds numerical values.
#
# Pandas Concept:
# .sum() adds all values in a DataFrame column.
#
# .to_numpy() converts the resulting Pandas Series
# into a NumPy array.
#
# This ensures the test can access the result using [0].

sum_total_price = pd.read_sql(
    """
    SELECT
        ROUND(priceEach * quantityOrdered) AS total_price
    FROM orderDetails;
    """,
    conn
).sum().to_numpy()


# ============================================================
# STEP 9: EXTRACT DAY, MONTH AND YEAR
# ============================================================

# Problem:
# Retrieve the original order date and extract:
#
# 1. Day
# 2. Month
# 3. Year
#
# The columns must be named:
# day, month, year
#
# SQL Concept:
# STRFTIME() formats or extracts date information.
#
# %d = Day of month (01-31)
# %m = Month (01-12)
# %Y = Four-digit year
#
# The original orderDate column must appear first.

df_day_month_year = pd.read_sql(
    """
    SELECT
        orderDate,

        STRFTIME('%d', orderDate) AS day,

        STRFTIME('%m', orderDate) AS month,

        STRFTIME('%Y', orderDate) AS year

    FROM orders;
    """,
    conn
)


# ============================================================
# DISPLAY RESULTS FOR MANUAL VERIFICATION
# ============================================================

# Only print the results when this file is executed directly.
#
# This prevents unnecessary console output when Pytest
# imports the variables from main.py.

if __name__ == "__main__":

    print("\n========== STEP 2: EMPLOYEE NUMBER AND NAME ==========")
    print(df_first_five.head())

    print("\n========== STEP 3: REVERSED COLUMNS ==========")
    print(df_five_reverse.head())

    print("\n========== STEP 4: COLUMN ALIAS ==========")
    print(df_alias.head())

    print("\n========== STEP 5: EXECUTIVE CLASSIFICATION ==========")
    print(df_executive.head())

    print("\n========== STEP 6: LAST NAME LENGTH ==========")
    print(df_name_length.head())

    print("\n========== STEP 7: SHORT JOB TITLES ==========")
    print(df_short_title.head())

    print("\n========== STEP 8: TOTAL ORDER VALUE ==========")
    print(sum_total_price)

    print("\n========== STEP 9: DATE FORMATTING ==========")
    print(df_day_month_year.head())


# ============================================================
# CLOSE DATABASE CONNECTION
# ============================================================

# All queries have already executed and their results
# are stored in Python variables.
#
# Close the connection to release database resources.

conn.close()