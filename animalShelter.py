from pymongo import MongoClient

class AnimalShelter:
    """CRUD operations for the Animal collection in MongoDB"""

    def __init__(self, username, password, host, port, db_name, col_name):
        """Initialize with dynamic username and password."""
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.col_name = col_name

        try:
            # Connect to MongoDB with user authentication
            self.client = MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}")
            self.database = self.client[self.db_name]
            self.collection = self.database[self.col_name]
            print("MongoDB connection successful.")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise

    def create(self, data):
        """Insert a new document into the animals collection."""
        if not data:
            raise ValueError("Data cannot be empty")

        try:
            result = self.collection.insert_one(data)
            if result.inserted_id:
                print(f"Animal inserted with ID: {result.inserted_id}")
                return True
            return False
        except Exception as e:
            print(f"Error inserting data into MongoDB: {e}")
            return False

    def read(self, query):
        """Query documents from the animals collection."""
        try:
            results = self.collection.find(query)
            animals = list(results)  # Convert cursor to list
            if not animals:
                print("No animals found matching the query.")
            return animals
        except Exception as e:
            print(f"Error reading from database: {e}")
            return []

    def update(self, query, new_values):
        """Update an animal's information based on a query."""
        if not new_values:
            raise ValueError("New values cannot be empty")

        try:
            result = self.collection.update_one(query, {"$set": new_values})
            if result.modified_count > 0:
                print(f"Updated {result.modified_count} animal(s).")
                return True
            print("No animals matched the query for update.")
            return False
        except Exception as e:
            print(f"Error updating database: {e}")
            return False

    def delete(self, query):
        """Delete an animal record based on a query."""
        try:
            result = self.collection.delete_one(query)
            if result.deleted_count > 0:
                print(f"Deleted {result.deleted_count} animal(s).")
                return True
            print("No animals matched the query for deletion.")
            return False
        except Exception as e:
            print(f"Error deleting from database: {e}")
            return False

# Example usage:
if __name__ == "__main__":
    # Update the following with your dynamic credentials and MongoDB details
    username = "aacuser"
    password = "HoustonLux21"
    host = "nv-desktop-services.apporto.com"
    port = 31448
    db_name = "AAC"
    col_name = "animals"
    
    shelter = AnimalShelter(username, password, host, port, db_name, col_name)

    # Example of creating a new animal record
    animal_data = {"name": "Bella", "species": "Dog", "age": 3}
    shelter.create(animal_data)
    
    # Example of reading data
    query = {"species": "Dog"}
    animals = shelter.read(query)
    for animal in animals:
        print(animal)

    # Example of updating a record
    update_query = {"name": "Bella"}
    new_values = {"age": 4}
    shelter.update(update_query, new_values)
    
    # Example of deleting a record
    delete_query = {"name": "Bella"}
    shelter.delete(delete_query)