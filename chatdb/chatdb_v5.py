import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

#xml imports 
from lxml import etree
import xml.etree.ElementTree as ET
UK_JOBS_XML = "monster_uk-job_sample.xml"
BIBS_XML = "bibs.xml"
MOVIES_XML = "movies.xml"

# old mongo imports
# from pymongo import MongoClient
# client = MongoClient()
# final = client['final']
# iris = final['iris']
# property_level = final['property_level']
# us_category_id = final['US_category_id']
# ca_category_id = final['CA_category_id']
import random

# sql query to display
global my_conn
my_conn = None

# running chatdb
def chatdb(): 
    # selecting a database
    print("What database system would you like to use?")
    print("   1: MySQL")
    print("   2: XML")
    language = input("> ")
    language = error_checking(language, 1, 2)
    
    if language == 1:
        mysql()
    elif language == 2:
        xml()
    return yes_no("Continue using ChatDB?")
    
def mysql():
    global my_conn
    print("You are now using MySQL.")
    print("Please select a database you would like to explore:")
    print("   1: Books of the Decade")
    print("   2: Spotify: Most Streamed Songs")
    print("   3: Google Merchandise Dataset")
    dataset = input("> ")
    dataset = error_checking(dataset, 1, 3)
    # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/final')
    if dataset == 1:
        my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/books')
        mysql_query(my_conn, f"Dataset #{dataset}", dataset)
    elif dataset == 2:
        my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/spotify')
        mysql_query(my_conn, "Spotify: Most Streamed Songs", dataset)
    elif dataset == 3:
        my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/google')
        mysql_query(my_conn, f"Dataset #{dataset}", dataset)
        # sql_query_generation("1", dataset, my_conn)

    # if dataset == 1:
    #     # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/books_of_the_decade')
    #     mysql_query(my_conn, "Books of the Decade", dataset)
    # elif dataset == 2:
    #     # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/spotify_most_streamed_songs')
    #     mysql_query(my_conn, "Spotify: Most Streamed Songs", dataset)
    # elif dataset == 3:
    #     # my_conn = sqlalchemy.create_engine('mysql+mysqldb://root:Dsci-351@localhost/google_merchandise')
    #     mysql_query(my_conn, "Google Merchandise", dataset)
        
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
            sql_query_generation(choice, dataset_index, my_conn)
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

# testing
def get_column_titles(dataset_index):
    if dataset_index == 1:  # Books of the Decade
        return ["`Index`" if col.lower() == "index" else col for col in ["Index", "Book_Name", "Author", "Rating", "Number_of_Votes", "Score"]]
    elif dataset_index == 2:  # Spotify: Most Streamed Songs
        return ["track_name", "artist(s)_name", "artist_count", "released_year", "released_month", "released_day", "in_spotify_playlists", "in_spotify_charts", "streams", "in_apple_playlists", "in_apple_charts", "in_deezer_playlists", "in_deezer_charts", "in_shazam_charts", "bpm", "key", "mode", "danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%", "liveness_%", "speechiness_%", "cover_url"]
    elif dataset_index == 3:  # Google Merchandise
        # Assume three tables: products, orders, customers
        return {
            'items': ["id", "name", "brand", "variant", "category", "price_in_usd"],
            'events1': ["user_id", "ga_session_id", "country", "device", "type", "item_id", "date"],
            'users': ["id", "ltv", "date"]
        }
    return []

def get_shared_columns():
    return {
        ('items', 'events1'): ('id', 'item_id'),
        ('users', 'events1'): ('id', 'user_id')
        # 'products': 'product_id',
        # 'orders': 'product_id',
        # 'customers': 'customer_id'
    }


def sql_query_generation(menu_option, dataset_index, my_conn):
    column_titles = []
    functions_end = ["asc", "desc"]
    functions_operators = ["where", "group by", "sort by", "having"]
    functions_number = ["limit", "skip", "offset"]
    functions = ["asc", "desc", "where", "group by", "sort by", "having", "limit", "skip", "offset"]
    if dataset_index == 1: # books of the decade
        column_titles = ["`Index`" if col.lower() == "index" else col for col in ["Index", "Book_Name", "Author", "Rating", "Number_of_Votes", "Score"]]
        book_names = ["The Invisible Life of Addie LaRue", "Project Hail Mary", "The Midnight Library", "Piranesi", "Lessons in Chemistry"]
        authors = ["Victoria Schwab", "T.J. Klune", "Andy Weir", "Matt Haig", "Suzanne Collins"]
        if menu_option == "1": # generate "random" queries
            for _ in range(10):
                attribute = random.choice(column_titles)
                function = random.choice(functions_operators)
                non_agg_columns = ["Book_Name", "Author", "Index"]
                numeric_columns = ["Rating", "Number_of_Votes", "Score"]

                query = f"SELECT {attribute} FROM books_of_the_decade"
                
                if function == "where":
                    condition_column = random.choice(column_titles)
                    if condition_column in ["Book_Name", "Author"]:
                        value = random.choice(book_names if condition_column == "Book_Name" else authors)
                        query += f" WHERE `{condition_column}` = '{value}'"
                    else:
                        operator = random.choice([">", "<", "="])
                        value = random.randint(1, 5) if condition_column == "Rating" else random.randint(1000, 2000000)
                        query += f" WHERE `{condition_column}` {operator} {value}"
                
                elif function == "group by":
                    group_column = random.choice(non_agg_columns + numeric_columns)
                    agg_function = random.choice(["COUNT", "AVG", "MAX", "MIN"])
                    agg_column = random.choice(numeric_columns)
                    query = f"SELECT `{group_column}`, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY `{group_column}`"
                
                elif function == "order by":
                    order_column = random.choice(column_titles)
                    direction = random.choice(["ASC", "DESC"])
                    query += f" ORDER BY {order_column} {direction}"

                elif function == "having":
                    group_column = random.choice(non_agg_columns)
                    agg_function = random.choice(["COUNT", "AVG", "MAX", "MIN"])
                    agg_column = random.choice(numeric_columns)
                    operator = random.choice([">", "<"])
                    value = random.randint(1, 1000000)
                    # query = f"SELECT {group_column}, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY {group_column} HAVING {agg_function}({agg_column}) {operator} {value}"
                    query = f"SELECT `{group_column}`, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY `{group_column}` HAVING {agg_function}(`{agg_column}`) {operator} {value}"
                    # if agg_function == "COUNT":
                    #     query = f"SELECT {group_column}, COUNT(*) FROM books_of_the_decade GROUP BY {group_column} HAVING COUNT(*) {operator} {value}"
                    # else:
                    #     query = f"SELECT {group_column}, {agg_function}({agg_column}) FROM books_of_the_decade GROUP BY {group_column} HAVING {agg_function}({agg_column}) {operator} {value}"
                elif function == "sort by":
                    sort_column = random.choice(column_titles)
                    direction = random.choice(["ASC", "DESC"])
                    query += f" ORDER BY `{sort_column}` {direction}"

                elif function == "limit":
                    limit_value = random.choice([1, 5, 10, 50, 100])
                    query += f" LIMIT {limit_value}"
            
                # if function == "sort by":
                #     sort_column = random.choice(column_titles)
                #     direction = random.choice(["ASC", "DESC"])
                #     query += f" ORDER BY `{sort_column}` {direction}"
                    
                #     # Add a chance to include LIMIT after ORDER BY
                #     if random.random() < 0.5:  # 50% chance to add LIMIT
                #         limit_value = random.choice([1, 5, 10, 50, 100])
                #         query += f" LIMIT {limit_value}"

                # elif function == "limit":
                #     limit_value = random.choice([1, 5, 10, 50, 100])
                #     query += f" LIMIT {limit_value}"

                # # Add a chance to include LIMIT for queries that don't have sort by or limit
                # if "ORDER BY" not in query and "LIMIT" not in query and random.random() < 0.3:  # 30% chance
                #     limit_value = random.choice([1, 5, 10, 50, 100])
                #     query += f" LIMIT {limit_value}"
                
            
                print(f"Ex #{_+1}: {query};")
                try:
                    # Execute the query
                    result = pd.read_sql(query, my_conn)
                    
                    # Print the results
                    if result.empty:
                        print("Query executed successfully, but returned no results.")
                    else:
                        print("\nQuery Results:")
                        print(result.to_string(index=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
                
                print("\n" + "-"*50 + "\n")  # Separator between queries
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
    elif  dataset_index == 2: # "Spotify: Most Streamed Songs"
        column_titles = ["track_name", "artist(s)_name", "artist_count", "released_year", "released_month", "released_day", "in_spotify_playlists", "in_spotify_charts", "streams", "in_apple_playlists", "in_apple_charts", "in_deezer_playlists", "in_deezer_charts", "in_shazam_charts", "bpm", "key", "mode", "danceability_%", "valence_%", "energy_%", "acousticness_%", "instrumentalness_%", "liveness_%", "speechiness_%", "cover_url"]
        return 
    elif  dataset_index == 3: # "Google Merchandise"
        tables = get_column_titles(dataset_index)
        # brand = ["\"Google\"", "\"Android\"", "\"Youtube\"", "\"#IamRemarkable\""]
        # category = ["\"Apparel\"", "\"New\"", "\"Drinkware\"", "\"Campus Collection\"", "\"Clearance\""]
        # def sql_query_generation(menu_option, dataset_index, my_conn):
        valid_joins = [
            ('events1', 'items', 'item_id', 'id'),
            ('events1', 'users', 'user_id', 'id')
        ]



        if menu_option == "1":  # Generate random queries
            for _ in range(10):
                # Randomly select one of the two valid join pairs
                table1, table2, join_column1, join_column2 = random.choice(valid_joins)

                # Select random columns from each table
                column1 = random.choice(tables[table1])
                column2 = random.choice(tables[table2])

                # Construct the base query
                # query = f"""
                # SELECT {', '.join([f'{table1}.{col}' for col in columns1])},
                #        {', '.join([f'{table2}.{col}' for col in columns2])}
                # FROM {table1}
                # FULL OUTER JOIN {table2} ON {table1}.{join_column1} = {table2}.{join_column2}
                # """

                query = f"""
                SELECT {table1}.{column1}, {table2}.{column2}
                FROM {table1}
                JOIN {table2} ON {table1}.{join_column1} = {table2}.{join_column2}
                """


                # Add WHERE clause (optional)
                if random.choice([True, False]):
                    where_table = random.choice([table1, table2])
                    where_column = random.choice(tables[where_table])
                    where_value = random.randint(1, 1000)  # Adjust range as needed
                    query += f"\nWHERE {where_table}.{where_column} > {where_value}"

                # Add ORDER BY (optional)
                if random.choice([True, False]):
                    order_table = random.choice([table1, table2])
                    order_column = random.choice(tables[order_table])
                    order_direction = random.choice(["ASC", "DESC"])
                    query += f"\nORDER BY {order_table}.{order_column} {order_direction}"

                # Add LIMIT (optional)
                if random.choice([True, False]):
                    limit_value = random.randint(1, 50)
                    query += f"\nLIMIT {limit_value}"

                print(f"Generated query #{_+1}:\n{query}")

                try:
                    result = pd.read_sql(query, my_conn)
                    if result.empty:
                        print("Query executed successfully, but returned no results.")
                    else:
                        print("\nQuery Results:")
                        print(result.to_string(index=False))
                        print(f"\nNumber of rows: {len(result)}")
                except Exception as e:
                    print(f"Error executing query: {e}")

                print("\n" + "-"*50 + "\n")  # Separator between queries
        return 


    
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
            base_query += " WHERE condition" #`column` = value instead of condition?
        elif func == "group by":
            base_query += " GROUP BY `column`"
        elif func == "order by":
            base_query += " ORDER BY `column`"
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
   
# def mongodb():
#     print("You are now using MongoDB.")
#     print("Please select a database you would like to explore:")
#     print("   1: Iris Dataset")
#     print("   2: Real Estate Dataset")
#     print("   3: YouTube Trending Dataset")
#     dataset = input("> ")
#     dataset = error_checking(dataset, 1, 3)
#     # if dataset == 1:
#     #     print("You are now using the Yelp dataset. Enter a query, or enter \'?\' for assistance.")
#     #     query = input("> ")
#     #     if query == "?":
#     #         print("Here are some sample queries.") 
#     if dataset == 1:
#         collection = final['iris']
#     elif dataset == 2:
#         collection = final['property_level']
#     elif dataset == 3:
#         collection = final['US_category_id']
    
#     print(f"You are now using the {collection.name} collection. Enter a query, or enter '?' for assistance.")
    
#     while True:
#         query = input("> ")
#         if query.lower() == 'exit':
#             break
#         elif query == "?":
#             show_mongodb_help()
#         else:
#             execute_mongodb_query(collection, query)
# def show_mongodb_help():
#     print("MongoDB Query Help:")
#     print("1. Find all documents: db.collection.find()")
#     print("2. Find with criteria: db.collection.find({field: value})")
#     print("3. Find with projection: db.collection.find({}, {field: 1})")
#     print("4. Count documents: db.collection.count_documents({})")
#     print("5. Aggregate: db.collection.aggregate([{$group: {_id: '$field', count: {$sum: 1}}}])")
#     print("Enter 'exit' to quit.")
# def execute_mongodb_query(collection, query):
#     try:
#         # Parse the query
#         if query.startswith("db." + collection.name + ".find("):
#             # Extract parameters from find()
#             params = query[19:-1]
#             if params:
#                 criteria, projection = eval(f"({params})")
#             else:
#                 criteria, projection = {}, {}
            
#             results = collection.find(criteria, projection)
#             for doc in results:
#                 print(doc)
        
#         elif query.startswith("db." + collection.name + ".count_documents("):
#             criteria = eval(query[30:-1])
#             count = collection.count_documents(criteria)
#             print(f"Count: {count}")
        
#         elif query.startswith("db." + collection.name + ".aggregate("):
#             pipeline = eval(query[25:-1])
#             results = collection.aggregate(pipeline)
#             for doc in results:
#                 print(doc)
        
#         else:
#             print("Unsupported query. Please try again or type '?' for help.")
    
#     except Exception as e:
#         print(f"Error executing query: {e}")

def load_xml_file(file_path):
    # try:
    #     tree = ET.parse(file_path)
    #     root = tree.getroot()
    #     return root
    # except ET.ParseError as e:
    #     print(f"Error parsing XML file: {e}")
    #     return None

    try:
        tree = etree.parse(file_path)
        return tree
    except etree.XMLSyntaxError as e:
        print(f"Error parsing XML file: {e}")
        return None

def xml():
    print("You are now using XML.")
    print("Please select a database you would like to explore:")
    print("   1: Monster UK Jobs")
    print("   2: Bibliography")
    print("   3: Movies")

    dataset = input("> ")
    dataset = error_checking(dataset, 1, 3)

    if dataset == 1:
        tree = xml_1
        print("You are now using the Monster UK Jobs dataset.")
        xml_root = load_xml_file('monster_uk-job_sample.xml')
        xml_query(xml_root)
    elif dataset == 2:
        tree = xml_2
        print("You are now using the bibs dataset.")
        xml_root = load_xml_file('bibs.xml')
        xml_query(xml_root)
    elif dataset == 3:
        tree = xml_3
        print("You are now using the movies dataset.")
        xml_root = load_xml_file('movies.xml')
        xml_query(xml_root)

def xml_query(tree):
    exit = False
    while exit == False:
        print("Enter a query, or enter \'?\' for assistance.")
        query = input("> ")
        if query == "?":
            print("Help menu:")
            print("   1: Generate example queries")
            print("   2: Generate example queries by function")
            choice = input("> ")
            if choice == "1":
                generate_random_xml_queries(tree)
            else:
                generate_xml_queries_by_function(tree)
        else:
            execute_xml_query(tree, query)
            
        exit = yes_no("Would you like to enter another query?")

def xml_1():
    with open(UK_JOBS_XML, 'r') as file:
        return etree.parse(file)
    
def xml_2():
    with open(BIBS_XML, 'r') as file:
        return etree.parse(file)
    
def xml_3():
    with open(MOVIES_XML, 'r') as file:
        return etree.parse(file)

def generate_random_xml_queries(xml_root):
    # Gather all elements and attributes for query generation
    elements = [elem.tag for elem in xml_root.iter()]
    attributes = {elem.tag: list(elem.attrib.keys()) for elem in xml_root.iter() if elem.attrib}

    query_types = ['find_element', 'find_attribute', 'find_with_predicate']

    for _ in range(3):
        query_type = random.choice(query_types)
        
        if query_type == 'find_element':
            element = random.choice(elements)
            print(f"Find all '{element}' elements: .//{element}")
        
        elif query_type == 'find_attribute' and attributes:
            element = random.choice(list(attributes.keys()))
            attribute = random.choice(attributes[element])
            print(f"Find '{element}' elements with attribute '{attribute}': .//{element}[@{attribute}]")
        
        elif query_type == 'find_with_predicate':
            element = random.choice(elements)
            if attributes.get(element):
                attribute = random.choice(attributes[element])
                value = f"'value{random.randint(1, 100)}'"  # Generate a random value
                print(f"Find '{element}' elements with predicate: .//{element}[@{attribute}={value}]")
            else:
                # If no attributes, use a position predicate
                position = random.randint(1, 5)
                print(f"Find '{element}' elements with position predicate: .//{element}[{position}]")

def generate_xml_queries_by_function(xml_root):
    xpath_forms = [
        "Find elements by tag name",
        "Find elements with specific attribute",
        "Find elements with specific text",
        "Find elements by position",
        "Find elements with attribute and text"
    ]

    # Gather all elements and attributes for query generation
    elements = [elem.tag for elem in xml_root.iter()]
    attributes = {elem.tag: list(elem.attrib.keys()) for elem in xml_root.iter() if elem.attrib}

    print("Select an xpath feature to explore:")
    count = 0
    for f in xpath_forms:
        count += 1
        count_string = str(count)
        print(count_string + ": " + f)

    form = input("> ")

    for _ in range(3):
        
        if form == "find elements by tag name":
            element = random.choice(elements)
            print(f"XPath Query: .//{element}")

        elif form == "find elements with specific attribute" and attributes:
            element = random.choice(list(attributes.keys()))
            attribute = random.choice(attributes[element])
            value = f"value{random.randint(1, 100)}"  # Simulate a possible attribute value
            print(f"XPath Query: .//{element}[@{attribute}='{value}']")

        elif form == "find elements with specific text":
            element = random.choice(elements)
            text_value = f"text{random.randint(1, 100)}"  # Simulate a possible text content
            print(f"XPath Query: .//{element}[text()='{text_value}']")

        elif form == "find elements by position":
            element = random.choice(elements)
            position = random.randint(1, 5)  # Random position
            print(f"XPath Query: .//{element}[position()={position}]")

        elif form == "find elements with attribute and text":
            if attributes:
                element = random.choice(list(attributes.keys()))
                attribute = random.choice(attributes[element])
                attr_value = f"value{random.randint(1, 100)}"
                text_value = f"text{random.randint(1, 100)}"
                print(f"XPath Query: .//{element}[@{attribute}='{attr_value}'][text()='{text_value}']")

def execute_xml_query(xml_root, xpath):
    try:
        # Execute the XPath query
        result = xml_root.xpath(xpath)
        
        # Process and print results based on their type
        for elem in result:
            if isinstance(elem, etree._Element):
                # Print element as a string if it's an XML element
                print(etree.tostring(elem, pretty_print=True, encoding='unicode'))
            else:
                # Print text or attribute values directly
                print(elem)

    except Exception as e:
        print(f"Error executing XPath query: {e}")


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