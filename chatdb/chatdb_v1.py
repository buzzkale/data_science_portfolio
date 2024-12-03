import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

from pymongo import MongoClient
client = MongoClient()
final = client['final']
# iris = final['iris']
# property_level = final['property_level']
# us_category_id = final['US_category_id']
# ca_category_id = final['CA_category_id']

import random

# running chatdb
def chatdb(): 
    # selecting a database
    print("What database system would you like to use?")
    print("   1: MySQL")
    print("   2: MongoDB")

    language = input("> ")
    language = error_checking(language, 1, 2)
    
    if language == 1:
        mysql()
    elif language == 2:
        mongodb()

    return yes_no("Continue using ChatDB?")
    

def mysql():
    print("You are now using MySQL.")
    print("Please select a database you would like to explore:")
    print("   1: Books of the Decade")
    print("   2: Spotify: Most Streamed Songs")
    print("   3: Google Merchandise Dataset")

    dataset = input("> ")
    dataset = error_checking(dataset, 1, 3)

    my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/final')

    if dataset == 1:
        # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/books_of_the_decade')
        mysql_query(my_conn, "Books of the Decade", dataset)
    elif dataset == 2:
        # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/spotify_most_streamed_songs')
        mysql_query(my_conn, "Spotify: Most Streamed Songs", dataset)
    elif dataset == 3:
        # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/google_merchandise')
        mysql_query(my_conn, "Google Merchandise", dataset)
        
def mysql_query(my_conn, dataset, dataset_index):
    print("You are now using the", dataset, "dataset.")
    
    exit = False
    while exit == False:
        print("Enter a query, or enter \'?\' for assistance.")
        query = input("> ")

        if query == "?":
            print("Help menu:")
            print("   1: Generate example queries")
            print("   2: Generate example queries by function")
            choice = input("> ")
            sql_query_generation(choice, dataset_index)
        else:
            # data = pd.read_sql(query, my_conn)

            try:
                data = pd.read_sql(query, my_conn)
                if data.empty:
                    print("Query executed successfully, but returned no results.")
                else:
                    print("\nQuery Results:")
                    print(data.to_string(index=False))
                    print(f"\nNumber of rows: {len(data)}")
            except Exception as e:
                print(f"Error executing query: {e}")

        exit = yes_no("Would you like to enter another query?")

def sql_query_generation(menu_option, dataset_index):
    column_titles = []

    functions_end = ["asc", "desc"]
    functions_operators = ["where", "group by", "sort by", "having"]
    functions_number = ["limit", "skip", "offset"]

    functions = ["asc", "desc", "where", "group by", "sort by", "having", "limit", "skip", "offset"]

    if dataset_index == 1: # books of the decade
        column_titles = ["Book_Name", "Author", "Rating", "Number_of_Votes", "Score"]
        book_names = ["The Invisible Life of Addie LaRue", "Project Hail Mary", "The Midnight Library", "Piranesi", "Lessons in Chemistry"]
        authors = ["Victoria Schwab", "T.J. Klune", "Andy Weir", "Matt Haig", "Suzanne Collins"]

        if menu_option == "1": # generate "random" queries
            for _ in range(3):
                attribute = random.choice(column_titles)
                function = random.choice(functions_operators)
                
                query = f"SELECT {attribute} FROM books_of_the_decade"
                
                if function == "where":
                    condition_column = random.choice(column_titles)
                    if condition_column in ["Book_Name", "Author"]:
                        value = random.choice(book_names if condition_column == "Book_Name" else authors)
                        query += f" WHERE {condition_column} = '{value}'"
                    else:
                        operator = random.choice([">", "<", "="])
                        value = random.randint(1, 5) if condition_column == "Rating" else random.randint(1000, 2000000)
                        query += f" WHERE {condition_column} {operator} {value}"
                
                elif function == "group by":
                    group_column = random.choice(["Author", "Rating"])
                    agg_function = random.choice(["AVG", "MAX", "MIN"])
                    agg_column = random.choice([col for col in column_titles if col != group_column])
                    query = f"SELECT {group_column}, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY {group_column}"
                
                elif function == "order by":
                    order_column = random.choice(column_titles)
                    direction = random.choice(["ASC", "DESC"])
                    query += f" ORDER BY {order_column} {direction}"
                
                elif function == "having":
                    group_column = "Author"
                    agg_function = random.choice(["AVG", "MAX", "MIN"])
                    agg_column = random.choice([col for col in column_titles if col != group_column])
                    operator = random.choice([">", "<"])
                    value = random.randint(1, 1000000)
                    query = f"SELECT {group_column}, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY {group_column} HAVING {agg_function}({agg_column}) {operator} {value}"
            
                print(f"{query};")
            # counter = 0
            # while counter < 3:
            #     # pseudo random number generator between 0 and x (amount of attributes)
            #     attribute = random.randint(0, len(column_titles)-1)
            #     att1 = column_titles[attribute] # select Book_Name
            #     # pseudo random number generator between 0 and x (amount of functions in functions list)
            #     function = random.randint(0, len(functions_operators)-1)
            #     func1 = functions_operators[function] # select Book_Name where
            #     if func1 == "where":
            #         attribute = random.randint(0, len(column_titles)-1)
            #         att2 = column_titles[attribute] # select Book_Name where Author
            #         if att2 == "Book_Name":
            #             entry = random.randint(0, 4)
            #             close = "= "
            #             close += book_name[entry] # select Book_Name where Book_Name 
            #         elif att2 == "Author":
            #             entry = random.randint(0, 4)
            #             close = "= "
            #             close += authors[entry]
            #         elif att2 == "Rating":
            #             arg = str(random.randint(0, 4))
            #             close = "> " + arg
            #         elif att2 == "Number_of_Votes":
            #             arg = str(random.randint(2, 2000000))
            #             close = "> " + arg
            #         elif att2 == "Score":
            #             arg = str(random.randint(0, 62442))
            #             close = "> " + arg
            #         example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + " " + close + ";"
            #     elif func1 == "group by":
            #         att2 = "Author" # select Book_Name where Author
            #         example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + ";"
            #     elif func1 == "having":
            #         attribute = random.randint(0, len(column_titles)-1)
            #         att2 = column_titles[attribute] # select Book_Name where Author
            #         if att2 == "Book_Name":
            #             entry = random.randint(0, 4)
            #             close = "= "
            #             close += book_name[entry] # select Book_Name where Book_Name 
            #         elif att2 == "Author":
            #             entry = random.randint(0, 4)
            #             close = "= "
            #             close += authors[entry]
            #         elif att2 == "Rating":
            #             arg = str(random.randint(0, 4))
            #             close = "> " + arg
            #         elif att2 == "Number_of_Votes":
            #             arg = str(random.randint(50, 2000000))
            #             close = "> " + arg
            #         elif att2 == "Score":
            #             arg = str(random.randint(0, 62442))
            #             close = "> " + arg
            #         example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + " " + close + ";"
                
            #     print(example)
            #     counter += 1
        elif menu_option == "2": # user selects what functions they want
            user_functions = []
            incompatible_pairs = [
                {"asc", "desc"},
                {"limit", "offset"},
                {"group by", "order by"}
            ]

            while True:
                print("Select a function you would like an example of:")
                for i, func in enumerate(functions, 1):
                    print(f"{i}: {func}")
                
                selection = int(input("> ")) - 1
                if 0 <= selection < len(functions):
                    new_function = functions[selection]
                    
                    # Check for incompatibility
                    is_incompatible = False
                    for pair in incompatible_pairs:
                        if new_function in pair:
                            if any(func in user_functions for func in pair):
                                print(f"Error: '{new_function}' is incompatible with a previously selected function.")
                                is_incompatible = True
                                break
                    
                    if not is_incompatible:
                        user_functions.append(new_function)
                        print(f"Added '{new_function}' to your query.")
                    
                    if not yes_no("Would you like to add another function?"):
                        break
                else:
                    print("Invalid selection. Please try again.")

            # Generate query based on user_functions
            query = generate_query_from_functions(user_functions, dataset_index)
            print("Generated query:", query)

def generate_query_from_functions(user_functions, dataset_index):
    # Implement query generation based on selected functions
    dataset = ""
    if dataset_index == 1:
        dataset = "books_of_the_decade"
    elif dataset_index == 2:
        dataset = "spotify_most_streamed_songs"
    elif dataset_index == 3:
        dataset = "google_merchandise"
    base_query = "SELECT * FROM " + dataset
    for func in user_functions:
        if func == "where":
            base_query += " WHERE condition"
        elif func == "group by":
            base_query += " GROUP BY column"
        elif func == "order by":
            base_query += " ORDER BY column"
        # Add more conditions for other functions
    
    return base_query

    # hannah's section
    # elif dataset_index == 3: # google merchandise
    #     column_titles = ["id", "brand", "variant", "category", "price_in_usd"]
    #     brand = ["\"Google\"", "\"Android\"", "\"Youtube\"", "\"#IamRemarkable\""]
    #     category = ["\"Apparel\"", "\"New\"", "\"Drinkware\"", "\"Campus Collection\"", "\"Clearance\""]

    #     if menu_option == "1": # generate "random" queries
    #         counter = 0
    #         while counter < 3:
    #             # pseudo random number generator between 0 and x (amount of attributes)
    #             attribute = random.randint(0, len(column_titles)-1)
    #             att1 = column_titles[attribute] # select Book_Name
    #             # pseudo random number generator between 0 and x (amount of functions in functions list)
    #             function = random.randint(0, len(functions_operators)-1)
    #             func1 = functions_operators[function] # select Book_Name where
    #             if func1 == "where":
    #                 attribute = random.randint(0, len(column_titles)-1)
    #                 att2 = column_titles[attribute] # select Book_Name where Author
    #                 if att2 == "column_titles":
    #                     entry = random.randint(0, 4)
    #                     close = "= "
    #                     close += book_name[entry] # select Book_Name where Book_Name 
    #                 elif att2 == "brand":
    #                     entry = random.randint(0, 3)
    #                     close = "= "
    #                     close += authors[entry]
    #                 elif att2 == "category":
    #                     arg = str(random.randint(0, 4))
    #                     close = "> " + arg
    #                 elif att2 == "Number_of_Votes":
    #                     arg = str(random.randint(2, 2000000))
    #                     close = "> " + arg
    #                 elif att2 == "Score":
    #                     arg = str(random.randint(0, 62442))
    #                     close = "> " + arg
    #                 example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + " " + close + ";"
    #             elif func1 == "group by":
    #                 att2 = "Author" # select Book_Name where Author
    #                 example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + ";"
    #             elif func1 == "having":
    #                 attribute = random.randint(0, len(column_titles)-1)
    #                 att2 = column_titles[attribute] # select Book_Name where Author
    #                 if att2 == "Book_Name":
    #                     entry = random.randint(0, 4)
    #                     close = "= "
    #                     close += book_name[entry] # select Book_Name where Book_Name 
    #                 elif att2 == "Author":
    #                     entry = random.randint(0, 4)
    #                     close = "= "
    #                     close += authors[entry]
    #                 elif att2 == "Rating":
    #                     arg = str(random.randint(0, 4))
    #                     close = "> " + arg
    #                 elif att2 == "Number_of_Votes":
    #                     arg = str(random.randint(50, 2000000))
    #                     close = "> " + arg
    #                 elif att2 == "Score":
    #                     arg = str(random.randint(0, 62442))
    #                     close = "> " + arg
    #                 example = "select " + att1 + " from books_of_the_decade " + func1 + " " + att2 + " " + close + ";"
                
    #             print(example)
    #             counter += 1

elif dataset_index == 3:  # Transaction Dataset
    # Dataset Columns
    column_titles = [
        "transaction_id", "transaction_date", "transaction_time", "transaction_qty", 
        "store_id", "store_location", "product_id", "unit_price", 
        "product_category", "product_type", "product_detail"
    ]
    
    # Example values for demonstration
    transaction_ids = ["T001", "T002", "T003", "T004", "T005"]
    store_locations = ["New York", "San Francisco", "Chicago", "Los Angeles", "Seattle"]
    product_categories = ["Electronics", "Groceries", "Apparel", "Toys", "Books"]
    product_types = ["Smartphones", "Fruits", "Shirts", "Dolls", "Novels"]
    unit_prices = [10, 15, 25, 40, 50]  # Example price range
    
    if menu_option == "1":  # Generate "random" queries
        counter = 0
        while counter < 3:
            # Randomly select an attribute
            attribute_index = random.randint(0, len(column_titles) - 1)
            att1 = column_titles[attribute_index]  # Example: "transaction_id", "store_location", etc.

            # Randomly select a function/operator
            function_index = random.randint(0, len(functions_operators) - 1)
            func1 = functions_operators[function_index]  # Example: "where", "group by", etc.

            # Generate query based on selected function/operator
            if func1 == "where":
                attribute_index = random.randint(0, len(column_titles) - 1)
                att2 = column_titles[attribute_index]

                if att2 == "transaction_id":
                    entry = random.choice(transaction_ids)
                    close = f"= \"{entry}\""
                elif att2 == "store_location":
                    entry = random.choice(store_locations)
                    close = f"= \"{entry}\""
                elif att2 == "product_category":
                    entry = random.choice(product_categories)
                    close = f"= \"{entry}\""
                elif att2 == "unit_price":
                    entry = random.randint(5, 100)  # Adjust range based on your dataset
                    close = f"> {entry}"

                example = f"SELECT {att1} FROM transactions WHERE {att2} {close};"

            elif func1 == "group by":
                att2 = "product_category"  # Example: Grouping by "product_category"
                example = f"SELECT {att1} FROM transactions {func1} {att2};"

            elif func1 == "having":
                attribute_index = random.randint(0, len(column_titles) - 1)
                att2 = column_titles[attribute_index]

                if att2 == "product_category":
                    entry = random.choice(product_categories)
                    close = f"= \"{entry}\""
                elif att2 == "unit_price":
                    entry = random.randint(5, 100)  # Adjust range as needed
                    close = f"> {entry}"

                example = f"SELECT {att1} FROM transactions GROUP BY {att1} HAVING {att2} {close};"

            print(example)
            counter += 1

    # # michael's section
    # # elif dataset_index == 2:
    #     user_reviews_col_titles = ["userId", "bookIndex", "score"]
    #     # entry = random.randin(1, 80000) # userID
    #     # entry = random.randin(1, 2327) # bookindex 
    #     # entry = random.randin(1, 5) # score
    #         if menu_option == "1": # generate "random" queries
    #         counter = 0
    #         while counter < 3:
    #             user_reviews_attr = random.randint(0, len(user_reviews_col_titles)-1)
    #             att1 = user_reviews_col_titles[user_reviews_attr]
    #             function = random.randint(0, len(functions_operators)-1)
    #             func1 = functions_operators[function] 
    #             if func1 == "where":
    #                 user_reviews_attr = random.randint(0, len(user_reviews_col_titles)-1)
    #                 att2 = user_reviews_col_titles[user_reviews_attr] 
    #                 if att2 == "userID":
    #                     entry = random.randint(1, 80000)
    #                     close = "= "
    #                     close += entry
    #                 elif att2 == "bookIndex":
    #                     entry = random.randin(1, 2327)
    #                     close = "= "
    #                     close += entry
    #                 elif att2 == "score":
    #                     entry = random.randin(1, 5)
    #                     close = "= "
    #                     close += entry
    #                 example = "select " + att1 + " from user_reviews_dataset " + func1 + " " + att2 + " " + close + ";"
    #             elif func1 == "group by":
    #                 att2 = "Author" # select Book_Name where Author
    #                 example = "select " + att1 + " from user_reviews_dataset " + func1 + " " + att2 + ";"
    #             elif func1 == "having":
    #                 user_reviews_attr = random.randint(0, len(user_reviews_col_titles)-1)
    #                 att2 = user_reviews_col_titles[user_reviews_attr] # select Book_Name where Author
    #                 if att2 == "Book_Name":
    #                     entry = random.randint(0, 4)
    #                     close = "= "
    #                     close += book_name[entry] # select Book_Name where Book_Name 
    #                 elif att2 == "Author":
    #                     entry = random.randint(0, 4)
    #                     close = "= "
    #                     close += authors[entry]
    #                 elif att2 == "Rating":
    #                     arg = str(random.randint(0, 4))
    #                     close = "> " + arg
    #                 elif att2 == "Number_of_Votes":
    #                     arg = str(random.randint(50, 2000000))
    #                     close = "> " + arg
    #                 elif att2 == "Score":
    #                     arg = str(random.randint(0, 62442))
    #                     close = "> " + arg
    #                 example = "select " + att1 + " from user_reviews_dataset " + func1 + " " + att2 + " " + close + ";"
                
    #             print(example)
    #             counter += 1

   

def mongodb():
    print("You are now using MongoDB.")
    print("Please select a database you would like to explore:")
    print("   1: Iris Dataset")
    print("   2: Real Estate Dataset")
    print("   3: YouTube Trending Dataset")

    dataset = input("> ")
    dataset = error_checking(dataset, 1, 3)

    # if dataset == 1:
    #     print("You are now using the Yelp dataset. Enter a query, or enter \'?\' for assistance.")
    #     query = input("> ")

    #     if query == "?":
    #         print("Here are some sample queries.") 

    if dataset == 1:
        collection = final['iris']
    elif dataset == 2:
        collection = final['property_level']
    elif dataset == 3:
        collection = final['US_category_id']
    
    print(f"You are now using the {collection.name} collection. Enter a query, or enter '?' for assistance.")
    
    while True:
        query = input("> ")
        if query.lower() == 'exit':
            break
        elif query == "?":
            show_mongodb_help()
        else:
            execute_mongodb_query(collection, query)

def show_mongodb_help():
    print("MongoDB Query Help:")
    print("1. Find all documents: db.collection.find()")
    print("2. Find with criteria: db.collection.find({field: value})")
    print("3. Find with projection: db.collection.find({}, {field: 1})")
    print("4. Count documents: db.collection.count_documents({})")
    print("5. Aggregate: db.collection.aggregate([{$group: {_id: '$field', count: {$sum: 1}}}])")
    print("Enter 'exit' to quit.")

def execute_mongodb_query(collection, query):
    try:
        # Parse the query
        if query.startswith("db." + collection.name + ".find("):
            # Extract parameters from find()
            params = query[19:-1]
            if params:
                criteria, projection = eval(f"({params})")
            else:
                criteria, projection = {}, {}
            
            results = collection.find(criteria, projection)
            for doc in results:
                print(doc)
        
        elif query.startswith("db." + collection.name + ".count_documents("):
            criteria = eval(query[30:-1])
            count = collection.count_documents(criteria)
            print(f"Count: {count}")
        
        elif query.startswith("db." + collection.name + ".aggregate("):
            pipeline = eval(query[25:-1])
            results = collection.aggregate(pipeline)
            for doc in results:
                print(doc)
        
        else:
            print("Unsupported query. Please try again or type '?' for help.")
    
    except Exception as e:
        print(f"Error executing query: {e}")

def error_checking(variable, lower_bound, upper_bound):
    entry = int(variable)
    while entry < lower_bound or entry > upper_bound:
        print("Input is out of bounds. Please enter a number between", lower_bound, "and", upper_bound)
        entry = int(input("> "))
    
    return entry

def yes_no(prompt):
    print(prompt, "(yes/no)")
    
    response = input("> ")

    if response.lower() == "no":
        response = True
    elif response.lower() == "yes":
        response = False
    
    return response

def main():
    print("Welcome to ChatDB!")

    exit = False

    while exit == False:
        exit = chatdb()
    
    print("Bye!")

if __name__ == "__main__":
    main()
