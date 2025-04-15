# Yisona 1.4

Yisona is a Python library for simple, structured JSON data management with local file storage and optional cloud connectivity.

## Features

- **Local JSON file operations** with nested key support
- **Cloud-based data storage** via the Yisona API
- **Dot notation for key paths** (e.g., "users.admin.name")
- **Simple SQLite integration**
- **Automatic file handling** (creation of non-existent files/directories)
- **Conversion helpers** for data types (e.g., string to numbers)

## Installation

```bash
pip install git+https://github.com/younglinslayer19/yisona
```

## Quick Start

### Local JSON File Operations

```python
from yisona import Yisona

# Initialize with path to JSON file (will be created if it doesn't exist)
db = Yisona("data/settings.json")

# Write data with nested structure
db.write_json("app.settings.theme", "dark")
db.write_json("app.settings.notifications", True)
db.write_json("user.profile.name", "John Doe")

# Read data
theme = db.get_json("app.settings.theme")  # Returns "dark"
notifications = db.get_json("app.settings.notifications")  # Returns True

# Check and create if not exists
exists = db.cc("app.version", "1.0.0")  # Returns False if created, True if exists

# Delete data
db.delete_json("user.profile.name")

# Convert to number
count_str = db.write_json("stats.count", "42")
count_num = db.get_json_as_number("stats.count")  # Returns 42.0
```

### Cloud Connectivity

```python
from yisona import YisonaConnect

# Initialize with your API token
cloud_db = YisonaConnect("your-api-token")

# Operations work the same as local version
cloud_db.write_json("cloud.data.synced", True)
cloud_data = cloud_db.get_json("cloud.data")  # Returns {"synced": True}

# Delete remote data
cloud_db.delete_json("cloud.data.outdated")
```

## API Reference

### Yisona (Local JSON)

#### `__init__(json_file_path)`
Initialize a Yisona object with a path to a JSON file.

- **Parameters:**
  - `json_file_path` (str): Path to the JSON file to be loaded or created

#### `get_json(key)`
Get a value from the JSON data using a dot-notated key path.

- **Parameters:**
  - `key` (str): Dot-notated key path to retrieve (e.g., "users.admin.name")
- **Returns:** The value at the key path or None if not found

#### `write_json(key, value)`
Write a value to the JSON file at a specific key path.

- **Parameters:**
  - `key` (str): Dot-notated key path to update
  - `value`: Value to set at the key path
- **Returns:** bool: True if successful, False otherwise

#### `get_json_as_number(key)`
Get a value from the JSON data and convert it to a number.

- **Parameters:**
  - `key` (str): Dot-notated key path to retrieve
- **Returns:** float: The numeric value or None if not convertible

#### `create_json(key, value)`
Create a new entry in the JSON data (alias for write_json).

- **Parameters:**
  - `key` (str): Key for the new entry
  - `value`: Value to associate with the key
- **Returns:** bool: True if successful, False otherwise

#### `cc(key, default_value)`
Check if a key exists, create it with a default value if it doesn't.

- **Parameters:**
  - `key` (str): Dot-notated key path to check
  - `default_value`: Value to set if key doesn't exist
- **Returns:** bool: True if key existed, False if it was created

#### `delete_json(key)`
Delete a key-value pair from the JSON data.

- **Parameters:**
  - `key` (str): Dot-notated key path to delete
- **Returns:** bool: True if deletion was successful, False otherwise

#### `get_sqlite(db_path, query)`
Execute a SQLite query and return the results.

- **Parameters:**
  - `db_path` (str): Path to the SQLite database file
  - `query` (str): SQL query to execute
- **Returns:** list: List of query result rows

### YisonaConnect (Cloud API)

#### `__init__(token)`
Initialize the YisonaConnect client.

- **Parameters:**
  - `token` (str): Authentication token for the API that identifies the database

#### `get_json(key=None)`
Get data from the remote database.

- **Parameters:**
  - `key` (str, optional): The specific dot-notated key path to retrieve
- **Returns:** The value at the specified key path or the entire data if no key is provided

All other methods mirror the local Yisona class with similar parameters and behavior.

## Error Handling

Yisona provides informative error messages when operations fail. For example:
- File not found warnings when initializing with non-existent files
- JSON decode errors for invalid files
- API connection errors for remote operations

## License

[MIT License](LICENSE)
