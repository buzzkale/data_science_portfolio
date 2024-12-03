# new
def load_xml_file_root(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return None

# replace
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
        tree = load_xml_file('monster_uk-job_sample.xml')
        root = load_xml_file_root('monster_uk-job_sample.xml')
        xml_query(tree, root)
    elif dataset == 2:
        tree = xml_2
        print("You are now using the bibs dataset.")
        tree = load_xml_file('bibs.xml')
        root = load_xml_file_root('bibs.xml')
        xml_query(tree, root)
    elif dataset == 3:
        tree = xml_3
        print("You are now using the movies dataset.")
        tree = load_xml_file('movies.xml')
        root = load_xml_file_root('movies.xml')
        xml_query(tree, root)

# replace
def xml_query(tree, root):
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
                generate_xml_queries_by_function(root)
        else:
            execute_xml_query(tree, query)
            
        exit = yes_no("Would you like to enter another query?")

# replace
def generate_xml_queries_by_function(xml_root):
    xpath_forms = [
        "Find elements by tag name",
        "Find elements with specific attribute",
        "Find elements with specific text",
        "Find elements by position"
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
