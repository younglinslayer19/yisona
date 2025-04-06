import json
import sqlite3

class Yisona:
    def __init__(self, json_file_path):
        """
        Initialize the Yisona class with a JSON file
        
        This constructor attempts to load and parse a JSON file. If the file is not found
        or contains invalid JSON, it will initialize with an empty dictionary.
        
        Parameters:
        json_file_path (str): Path to the JSON file to be loaded
        """
        self.json_file_path = json_file_path
        try:
            # Attempt to open and read the JSON file with UTF-8 encoding
            with open(json_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{json_file_path}' not found.")
            self.data = {}
        except json.JSONDecodeError:
            print(f"Error: File '{json_file_path}' contains invalid JSON.")
            self.data = {}
    
    def get_json(self, key):
        """
        Retrieve a value from the JSON data using dot notation for nested keys
        
        Example:
        - Simple key: 'name'
        - Nested key: 'user.address.city'
        
        Parameters:
        key (str): The key to look up (e.g., 'en.messages.hello')
        
        Returns:
        The value associated with the key, or None if the key doesn't exist
        """
        keys = key.split('.')
        value = self.data
        
        # Traverse through nested dictionary using the split keys
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
                
        return value

    def get_json_as_number(self, key):
        """
        Retrieve a value from the JSON data and convert it to a number if possible
        
        Parameters:
        key (str): The key to look up
        
        Returns:
        float or int: The numeric value, or None if the key doesn't exist or value isn't numeric
        """
        value = self.data.get(key)
        if isinstance(value, (int, float)):
            return value
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def write_json(self, key, value):
        """
        Update the JSON data with a new key-value pair and save changes to file
        
        This method will overwrite existing keys if they already exist.
        
        Parameters:
        key (str): The key to update or add
        value: The new value to assign to the key
        """
        self.data[key] = value
        try:
            # Write the updated data back to the JSON file
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            print(f"Successfully updated key '{key}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def create_json(self, key, value):
        """
        Create a new JSON entry with a key-value pair and save to file
        
        This method will warn if the key already exists and will overwrite it.
        
        Parameters:
        key (str): The key to add
        value: The value to assign to the key
        """
        if not isinstance(self.data, dict):
            print("Error: JSON data is not in the expected dictionary format.")
            return
        
        if key in self.data:
            print(f"Warning: Key '{key}' already exists and will be overwritten.")
        
        self.data[key] = value
        try:
            # Save the updated data to the JSON file
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            print(f"Successfully created JSON entry with key '{key}'.")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_sqlite(self, db_path, query):
        """
        Execute a SQL query on a SQLite database and return the results
        
        Parameters:
        db_path (str): Path to the SQLite database file
        query (str): SQL query to execute
        
        Returns:
        list: Query results as a list of tuples, or empty list on error
        """
        try:
            # Establish database connection and execute query
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except sqlite3.Error as e:
            print(f"SQLite query error: {e}")
            return []

# Usage example
if __name__ == "__main__":
    # Create an instance of Yisona and load the JSON file
    yisona = Yisona("test.json")
    
    # Retrieve a value from the JSON file
    value = yisona.get_json("source")
    print(f"Retrieved value is: {value}")
    
    # Retrieve a numeric value
    number = yisona.get_json_as_number("number_key")
    print(f"Retrieved numeric value is: {number}")
    
    # Update values in the JSON file
    yisona.write_json("name", "new value")
    yisona.write_json("number_key", 42)
    
    # Retrieve values from a SQLite database
    db_results = yisona.get_sqlite("test.db", "SELECT * FROM test")
    print(f"SQLite query results: {db_results}")
