# Yisona v1.2

Yisona is a simple Python library for managing JSON data with easy access to nested values and basic SQLite database functionality.

## Features

- Read and write data to JSON files with support for nested keys
- Access nested JSON values using dot notation (e.g., "user.settings.theme")
- Convert JSON values to numbers automatically
- Execute SQLite queries and retrieve results
- Create keys with default values if they don't exist

## Installation

Simply copy the `Yisona.py` file into your project folder.

## Usage

### Creating a Yisona Instance

```python
from Yisona import Yisona

# Initialize with a JSON file path
yisona = Yisona("data.json")
```

### Reading JSON Data

```python
# Get a simple value
name = yisona.get_json("name")

# Get a nested value using dot notation
theme = yisona.get_json("user.settings.theme")

# Get a value as a number
count = yisona.get_json_as_number("stats.count")
```

### Writing JSON Data

```python
# Set a simple value
yisona.write_json("name", "John")

# Set a nested value using dot notation
yisona.write_json("user.settings.theme", "dark")

# Create a new top-level key
yisona.create_json("version", "1.0.0")
```

### Check and Create Feature

The `cc` (check and create) method checks if a key exists and creates it with a default value if it doesn't:

```python
# Returns True if the key already exists, False if it was created
exists = yisona.cc("app.initialized", True)
if not exists:
    print("First-time initialization")
```

### SQLite Database Access

```python
# Execute a SQLite query and get results
users = yisona.get_sqlite("database.db", "SELECT * FROM users")
for user in users:
    print(user)
```

## Key Methods

- `get_json(key)`: Retrieves a value from the JSON data, supporting nested keys
- `write_json(key, value)`: Updates a value in the JSON data and saves to file
- `get_json_as_number(key)`: Retrieves a value and converts it to a number
- `create_json(key, value)`: Creates a new top-level key-value pair
- `get_sqlite(db_path, query)`: Executes a SQLite query and returns results
- `cc(key, default_value)`: Checks if a key exists, creates it with default value if not

## Error Handling

Yisona handles common errors gracefully:
- Missing JSON files
- Invalid JSON format
- File I/O errors
- SQLite query errors

## Example

```python
# Initialize with a JSON file
yisona = Yisona("config.json")

# Read nested values
api_key = yisona.get_json("security.api_key")
max_retries = yisona.get_json_as_number("network.max_retries")

# Write nested values
yisona.write_json("security.last_login", "2023-01-01")

# Add default values where missing
yisona.cc("network.timeout", 30)
yisona.cc("ui.theme", "light")

# Get data from SQLite
recent_logs = yisona.get_sqlite("logs.db", "SELECT * FROM logs ORDER BY timestamp DESC LIMIT 10")
```