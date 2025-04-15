import json
import sqlite3
import requests
import os


class YisonaLocal:
    """
    A class for local JSON file operations with nested key support and SQLite integration.
    """
    def __init__(self, json_file_path):
        """
        Initialize a YisonaLocal object with a JSON file path.
        
        Args:
            json_file_path (str): Path to the JSON file to be loaded or created
        """
        self.json_file_path = json_file_path
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print(f"Warning: File '{json_file_path}' not found. Creating a new file.")
            self.data = {}
            # Create the directory if it doesn't exist
            directory = os.path.dirname(json_file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            # Create the file
            with open(json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
        except json.JSONDecodeError:
            print(f"Error: File '{json_file_path}' contains invalid JSON. Using empty data.")
            self.data = {}

    def get_json(self, key):
        """
        Get a value from the JSON data using a dot-notated key path.
        
        Args:
            key (str): Dot-notated key path to retrieve (e.g., "users.admin.name")
            
        Returns:
            The value at the key path or None if not found
        """
        keys = str(key).split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(str(k))
            else:
                return None
        return value

    def write_json(self, key, value):
        """
        Write a value to the JSON file at a specific key path.
        
        Args:
            key (str): Dot-notated key path to update (e.g., "users.admin.name")
            value: Value to set at the key path
            
        Returns:
            bool: True if successful, False otherwise
        """
        keys = str(key).split('.')
        current = self.data
        
        # Navigate through nested structure
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            elif not isinstance(current[k], dict):
                # If the path exists but isn't a dict, convert it to one
                current[k] = {}
            current = current[k]
        
        # Set the value at the final key
        current[keys[-1]] = value
        
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            return True
        except IOError as e:
            print(f"Error writing to file: {e}")
            return False

    def get_json_as_number(self, key):
        """
        Get a value from the JSON data and convert it to a number.
        
        Args:
            key (str): Dot-notated key path to retrieve
            
        Returns:
            float: The numeric value or None if not convertible
        """
        value = self.get_json(key)
        if isinstance(value, (int, float)):
            return value
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    def create_json(self, key, value):
        """
        Create a new entry in the JSON data.
        
        Args:
            key (str): Key for the new entry
            value: Value to associate with the key
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.write_json(key, value)

    def get_sqlite(self, db_path, query):
        """
        Execute a SQLite query and return the results.
        
        Args:
            db_path (str): Path to the SQLite database file
            query (str): SQL query to execute
            
        Returns:
            list: List of query result rows
        """
        try:
            connection = sqlite3.connect(db_path)
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            connection.close()
            return results
        except sqlite3.Error as e:
            print(f"SQLite query error: {e}")
            return []

    def cc(self, key, default_value):
        """
        Check if a key exists, create it with a default value if it doesn't.
        
        Args:
            key (str): Dot-notated key path to check
            default_value: Value to set if key doesn't exist
            
        Returns:
            bool: True if key existed, False if it was created
        """
        keys = str(key).split('.')
        current = self.data
        
        # Navigate through nested structure
        for k in keys[:-1]:
            if k not in current or not isinstance(current[k], dict):
                current[k] = {}
            current = current[k]
                
        # Check if final key exists
        if keys[-1] in current:
            return True
            
        # Create with default value
        current[keys[-1]] = default_value
        
        try:
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(self.data, file, ensure_ascii=False, indent=4)
            return False
        except IOError as e:
            print(f"Error writing to file: {e}")
            return False

    def delete_json(self, key):
        """
        Delete a key-value pair from the JSON data.
        
        Args:
            key (str): Dot-notated key path to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        keys = str(key).split('.')
        current = self.data
        
        # Navigate to parent of target key
        for k in keys[:-1]:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                # Path doesn't exist
                return False
        
        # Delete the key if it exists
        if isinstance(current, dict) and keys[-1] in current:
            del current[keys[-1]]
            
            try:
                with open(self.json_file_path, 'w', encoding='utf-8') as file:
                    json.dump(self.data, file, ensure_ascii=False, indent=4)
                return True
            except IOError as e:
                print(f"Error writing to file: {e}")
                return False
        return False

class YisonaConnect:
    """
    A client for interacting with the Yisona API for remote JSON operations.
    Uses only a token to authenticate and identify the database.
    """
    def __init__(self, token):
        """
        Initialize the YisonaConnect client.
        
        Args:
            base_url (str): The base URL of the API (e.g., 'http://localhost:5000')
            token (str): Authentication token for the API that identifies the database
        """
        import requests  # Import here to ensure it's available
        self.requests = requests
        base_url = "https://yisona.xyz"
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.api_url = f"{self.base_url}/api"
        self.cached_data = None
        self.last_update = 0
    
    def get_json(self, key=None):
        """
        Get data from the remote database. If key is provided, returns only that key's value.
        
        Args:
            key (str, optional): The specific dot-notated key path to retrieve
            
        Returns:
            The value at the specified key path or the entire data if no key is provided
        """
        params = {'token': self.token}
        if key:
            params['key'] = key
        
        try:
            response = self.requests.get(self.api_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if key:
                    # API returns {key: value} for specific keys
                    return data.get(key)
                else:
                    self.cached_data = data
                    return data
            else:
                error_data = response.json()
                print(f"API Error ({response.status_code}): {error_data.get('error', 'Unknown error')}")
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None
    
    def create_json(self, key, value):
        """
        Create a new entry in the remote database.
        
        Args:
            key (str): Dot-notated key path for the new entry
            value: Value to associate with the key
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.write_json(key, value)
    
    def write_json(self, key, value):
        """
        Update an existing entry in the remote database.
        
        Args:
            key (str): Dot-notated key path to update
            value: Value to set at the key path
            
        Returns:
            bool: True if successful, False otherwise
        """
        headers = {
            'Content-Type': 'application/json',
            'X-API-Token': self.token
        }
        
        # For nested keys, we need to create the proper structure
        data_dict = {}
        if '.' in key:
            parts = key.split('.')
            current = data_dict
            for part in parts[:-1]:
                current[part] = {}
                current = current[part]
            current[parts[-1]] = value
        else:
            data_dict[key] = value
        
        try:
            response = self.requests.put(
                self.api_url,
                headers=headers,
                json=data_dict
            )
            
            if response.status_code == 200:
                return True
            else:
                error_data = response.json()
                print(f"API Error ({response.status_code}): {error_data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def get_json_as_number(self, key):
        """
        Get a value from the remote database and convert it to a number.
        
        Args:
            key (str): Dot-notated key path to retrieve
            
        Returns:
            float: The numeric value or None if not convertible
        """
        value = self.get_json(key)
        if isinstance(value, (int, float)):
            return value
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def delete_json(self, key):
        """
        Delete a specific key from the remote database.
        
        Args:
            key (str): The dot-notated key path to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        params = {
            'token': self.token,
            'key': key
        }
        
        try:
            response = self.requests.delete(self.api_url, params=params)
            
            if response.status_code == 200:
                return True
            else:
                error_data = response.json()
                print(f"API Error ({response.status_code}): {error_data.get('error', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def cc(self, key, default_value):
        """
        Check if a key exists in the remote database, create it with a default value if it doesn't.
        
        Args:
            key (str): Dot-notated key path to check
            default_value: Value to set if key doesn't exist
            
        Returns:
            bool: True if key existed, False if it was created
        """
        # Try to get the value first
        value = self.get_json(key)
        
        # If value doesn't exist, create it
        if value is None:
            self.write_json(key, default_value)
            return False
        return True
