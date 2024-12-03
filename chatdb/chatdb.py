import cmd
import mysql.connector
from pymongo import MongoClient
import random

class ChatDB(cmd.Cmd):
    intro = "Welcome to ChatDB! Type help or ? to list commands.\n"
    prompt = "(ChatDB) "

    def __init__(self):
        super().__init__()
        self.mysql_conn = None
        self.mongo_client = None
        self.current_db = None

    def connect_mysql(self, line):
        args = line.split()
        if len(args) != 4:
            print("Usage: connect_mysql <host> <user> <password> <database>")
            return
        host, user, password, database = args
        try:
            self.mysql_conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            self.current_db = "MySQL"
            print(f"Connected to MySQL database: {database}")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def connect_mongodb(self, line):
        args = line.split()
        if len(args) != 2:
            print("Usage: connect_mongodb <uri> <database>")
            return
        uri, database = args
        try:
            self.mongo_client = MongoClient(uri)
            self.current_db = self.mongo_client[database]
            print(f"Connected to MongoDB database: {database}")
        except Exception as err:
            print(f"Error: {err}")

    def show_tables(self, line):
        if self.current_db == "MySQL" and self.mysql_conn:
            cursor = self.mysql_conn.cursor()
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print("Tables in the MySQL database:")
            for table in tables:
                print(f" - {table[0]}")
        elif isinstance(self.current_db, MongoClient):
            collections = self.current_db.list_collection_names()
            print("Collections in the MongoDB database:")
            for collection in collections:
                print(f" - {collection}")
        else:
            print("No database connection established.")

    def describe_table(self, line):
        if not line:
            print("Usage: describe_table <table/collection_name>")
            return
        if self.current_db == "MySQL" and self.mysql_conn:
            cursor = self.mysql_conn.cursor()
            try:
                cursor.execute(f"DESCRIBE {line}")
                columns = cursor.fetchall()
                print(f"Description of table {line}:")
                for col in columns:
                    print(col)
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        elif isinstance(self.current_db, MongoClient):
            collection = self.current_db[line]
            sample_doc = collection.find_one()
            if sample_doc:
                print(f"Sample document from collection {line}:")
                print(sample_doc)
            else:
                print(f"Collection {line} is empty.")
        else:
            print("No database connection established.")


    def upload_dataset(self, line):
        """Upload a dataset to the current database. Usage: upload_dataset <path_to_file> <table/collection_name>"""
        # This function should be implemented to parse CSV/JSON files and upload to MySQL/MongoDB
        print("Dataset upload feature is under construction.")


if __name__ == "__main__":
    ChatDB().cmdloop()
