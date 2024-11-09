import mysql.connector
from mysql.connector import errorcode
from tabulate import tabulate
import datetime

DB_USERNAME = 'root'   
DB_PASSWORD = 'anshdb'   
DB_NAME = 'hospital_management'
DB_HOST = '127.0.0.1'


def get_connection():
    try:
        conn = mysql.connector.connect(
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            database=DB_NAME
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def show_tables():
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print("Available Tables:")
        for table in tables:
            print(table[0])
        cursor.close()
        conn.close()


def show_table_data(table_name):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        headers = [col[0] for col in columns]  
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        cursor.close()
        conn.close()


def add_data_to_table(table_name):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]
        print(f"Please enter the values for the columns {column_names}:")

        values = []
        for col in column_names:
            if col.lower() == 'updated_at':
                values.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                value = input(f"{col}: ")
                values.append(value)

        placeholders = ", ".join(["%s"] * len(values))
        insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({placeholders})"
        cursor.execute(insert_query, tuple(values))
        conn.commit()
        print(f"Data added successfully to {table_name}.")
        cursor.close()
        conn.close()


def delete_data_from_table(table_name):
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        cursor.execute(f"DESCRIBE {table_name}")
        columns = cursor.fetchall()
        column_names = [col[0] for col in columns]

        print(tabulate(rows, headers=column_names, tablefmt="grid"))

        row_id = input(f"Enter the ID of the row you want to delete from {table_name}: ")
        delete_query = f"DELETE FROM {table_name} WHERE {column_names[0]} = %s"
        cursor.execute(delete_query, (row_id,))
        conn.commit()
        print(f"Record with {column_names[0]} = {row_id} deleted successfully.")
        cursor.close()
        conn.close()


def main():
    while True:
        show_tables()
        table_choice = input("\nEnter the table you want to use (or 'exit' to quit): ").strip()
        if table_choice.lower() == 'exit':
            break

        show_table_data(table_choice)

        action = input("\nWhat do you want to do?\n1. Add new data\n2. Delete data\n3. Go back to tables\nChoose an option (1/2/3): ").strip()

        if action == '1':
            add_data_to_table(table_choice)
        elif action == '2':
            delete_data_from_table(table_choice)
        elif action == '3':
            continue
        else:
            print("Invalid option, please choose again.")


if __name__ == "__main__":
    main()
