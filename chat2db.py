import os
import json
import mariadb
import re
from datetime import datetime

# Database configuration
config = {
    'host': 'localhost',
    'port': 3306,
    'user': '<Database_Username>',
    'password': '<Database_Password>',
    'database': '<Database_Name>'
}

# Path to the directory containing JSON files
folder_path = '<Folder_With_JSON_Files>'

# UUID Regex for filename validation
UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.json$')

# Connect to MariaDB
try:
    conn = mariadb.connect(**config)
    cursor = conn.cursor()
    print("Successfully connected to the database.")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")
    exit(1)

def get_existing_chat_ids(cursor):
    cursor.execute("SELECT chat_id FROM chat_data")
    return {row[0] for row in cursor.fetchall()}

def is_valid_json_file(filename):
    return UUID_REGEX.match(filename) is not None

def is_valid_json_content(data):
    required_keys = {'title', 'create_time', 'mapping'}
    if not required_keys.issubset(data.keys()):
        return False
    try:
        # Check if 'create_time' is a valid UNIX timestamp by converting it to a datetime object
        datetime.utcfromtimestamp(data['create_time'])
        return True
    except (ValueError, TypeError):
        return False

def process_json_files(folder_path, cursor):
    existing_chat_ids = get_existing_chat_ids(cursor)

    for filename in os.listdir(folder_path):
        if not is_valid_json_file(filename):
            print(f"Skipping invalid file: {filename}")
            continue

        file_path = os.path.join(folder_path, filename)
        chat_id = filename[:-5]  # Remove the '.json' extension

        if chat_id in existing_chat_ids:
            print(f"Skipping already processed file: {filename}")
            continue

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"Invalid JSON content in file: {filename}")
                continue

            if not is_valid_json_content(data):
                print(f"Invalid data format in file: {filename}")
                continue

            title = data['title']
            create_time = int(data['create_time'])
            messages = json.dumps(data['mapping'])

            # Insert data into the 'chat_data' table
            try:
                cursor.execute(
                    "INSERT INTO chat_data (chat_id, title, create_time, messages) VALUES (?, ?, ?, ?)",
                    (chat_id, title, create_time, messages)
                )
            except mariadb.Error as e:
                print(f"Error inserting into chat_data: {e}")

def main():
    try:
        process_json_files(folder_path, cursor)
        conn.commit()  # Commit changes only if all operations are successful
        print("Finished processing all new files.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
