import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testing.settings')
django.setup()


from django.db import connection



# Now you can continue with your script


# Define the raw SQL query to create the table
create_table_sql = """
CREATE TABLE IF NOT EXISTS Employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    department VARCHAR(100),
    salary DECIMAL(10, 2)
);
"""

# Define the raw SQL query to insert rows into the table
insert_rows_sql = """
INSERT INTO Employees (name, age, department, salary) VALUES
('John Doe', 30, 'HR', 50000.00),
('Jane Smith', 35, 'Finance', 60000.00),
"""

# Execute the raw SQL query to create the table
with connection.cursor() as cursor:
    cursor.execute(create_table_sql)

# Execute the raw SQL query to insert rows into the table
with connection.cursor() as cursor:
    cursor.execute(insert_rows_sql)

# Print something to check the results
# For example, fetch and print all rows from the table
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
