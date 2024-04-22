# ChatGPT Parsed Archive To Database Python

This script processes individual ChatGPT chat archive JSON files and uploads them to a database.
The `jsonFiles` directory is just an example of your input folder. I left a random JSON file of one of my chats inside this folder for visualization.

## Requirements

### Download my ChatGPT JSON Archive Splitter Script

You will need to use the following Python script I made for this script to work properly: [ChatGPT JSON Archive Splitter](https://github.com/alanissak/ChatGPT-JSON-Archive-Splitter)
The ChatGPT JSON Archive Splitter takes the JSON file ChatGPT emails to you after you request all your data. All your conversations are stored in a single JSON file called `conversations.json` which needs to be properly converted before using this script to upload each chat into a database.

### SQL Query to prepare your database

```sql
CREATE TABLE chat_data (
    chat_id VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    create_time BIGINT NOT NULL,
    messages TEXT NOT NULL
);
```

## Dependencies

- Python 3
- `os` module
- `json` module
- `mariadb` module
- `re` module
- `datetime` module from the `datetime` package

## Configuration

### Database

Configure the database connection settings:

```chat2db.py
config = {
    'host': 'localhost',
    'port': 3306,
    'user': '<Database_Username>',
    'password': '<Database_Password>',
    'database': '<Database_Name>'
}
```

### JSON Files Directory

```chat2db.py
folder_path = '<Folder_With_JSON_Files>'
```

## Features

### UUID Validation

This part of the script is a check to only process files that match the correct UUID format. Your split conversation files are named after their `conversation_id` variable if you use the required script mentioned at the start of this Read Me file.

```chat2db.py
UUID_REGEX = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.json$')
```

### JSON Content Validation

Checks if JSON files contain the required keys: title, create_time, and mapping. Also verifies that create_time is a valid UNIX timestamp. If everythng is valid, it will insert the data into a MariaDB database
