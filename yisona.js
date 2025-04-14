/**
 * YisonaJS - JavaScript client for the Yisona API
 * This client can be used directly in the browser without requiring Node.js
 */
class YisonaJS {
    /**
     * Initialize the YisonaJS client
     * @param {string} baseUrl - The base URL of the API (e.g., 'http://localhost:5000')
     * @param {string} dbName - Name of the database to interact with (must include .json extension)
     * @param {string} token - Authentication token for the API
     */
    constructor(baseUrl, dbName, token) {
        this.baseUrl = baseUrl.endsWith('/') ? baseUrl.slice(0, -1) : baseUrl;
        this.dbName = dbName;
        this.token = token;
        this.apiUrl = `${this.baseUrl}/api/${this.dbName}`;
    }

    /**
     * Get data from the database. If key is provided, returns only that key's value.
     * @param {string} [key] - Optional dot-notated key path to retrieve specific data
     * @returns {Promise<Object>} - The response data
     */
    async getJson(key = null) {
        try {
            let url = new URL(this.apiUrl);
            url.searchParams.append('token', this.token);
            if (key) {
                url.searchParams.append('key', key);
            }

            const response = await fetch(url.toString());
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API Error (${response.status}): ${errorData.error || 'Unknown error'}`);
            }
            
            const data = await response.json();
            return key ? data[key] : data;
        } catch (error) {
            console.error('YisonaJS Error:', error);
            throw error;
        }
    }

    /**
     * Create or update data in the database
     * @param {string} key - Dot-notated key path to create or update
     * @param {any} value - Value to set at the key path
     * @returns {Promise<Object>} - Response indicating success or failure
     */
    async writeJson(key, value) {
        try {
            // For nested keys, we need to create the proper structure
            let data = {};
            if (key.includes('.')) {
                const parts = key.split('.');
                let current = data;
                
                for (let i = 0; i < parts.length - 1; i++) {
                    current[parts[i]] = {};
                    current = current[parts[i]];
                }
                current[parts[parts.length - 1]] = value;
            } else {
                data[key] = value;
            }

            const response = await fetch(this.apiUrl, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Token': this.token
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API Error (${response.status}): ${errorData.error || 'Unknown error'}`);
            }

            return await response.json();
        } catch (error) {
            console.error('YisonaJS Error:', error);
            throw error;
        }
    }

    /**
     * Create new data in the database (alias for writeJson)
     * @param {string} key - Dot-notated key path to create
     * @param {any} value - Value to set at the key path
     * @returns {Promise<Object>} - Response indicating success or failure
     */
    async createJson(key, value) {
        return this.writeJson(key, value);
    }

    /**
     * Delete a specific key from the database
     * @param {string} key - The dot-notated key path to delete
     * @returns {Promise<Object>} - Response indicating success or failure
     */
    async deleteJson(key) {
        try {
            let url = new URL(this.apiUrl);
            url.searchParams.append('token', this.token);
            url.searchParams.append('key', key);

            const response = await fetch(url.toString(), {
                method: 'DELETE',
                headers: {
                    'X-API-Token': this.token
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(`API Error (${response.status}): ${errorData.error || 'Unknown error'}`);
            }

            return await response.json();
        } catch (error) {
            console.error('YisonaJS Error:', error);
            throw error;
        }
    }

    /**
     * Check if a key exists, create it with a default value if it doesn't
     * @param {string} key - Dot-notated key path to check
     * @param {any} defaultValue - Value to set if key doesn't exist
     * @returns {Promise<boolean>} - True if key existed, false if it was created
     */
    async cc(key, defaultValue) {
        try {
            // Try to get the value first
            const data = await this.getJson(key);
            
            // If value is undefined or null, create it
            if (data === undefined || data === null) {
                await this.writeJson(key, defaultValue);
                return false;
            }
            return true;
        } catch (error) {
            // If there was an error, create the key
            await this.writeJson(key, defaultValue);
            return false;
        }
    }

    /**
     * Get a value as a number
     * @param {string} key - Dot-notated key path to retrieve
     * @returns {Promise<number|null>} - The numeric value or null if not convertible
     */
    async getJsonAsNumber(key) {
        const value = await this.getJson(key);
        
        if (typeof value === 'number') {
            return value;
        }
        
        try {
            const num = Number(value);
            return isNaN(num) ? null : num;
        } catch (error) {
            return null;
        }
    }
}
