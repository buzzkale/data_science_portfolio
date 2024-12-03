from lxml import etree
import xml.etree.ElementTree as ET
UK_JOBS_XML = "monster_uk-job_sample.xml"
BIBS_XML = "bibs.xml"
MOVIES_XML = "movies.xml"

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
    functions = ['find', 'findall', 'iter', 'iterfind']
    print("Select functions to include in the queries (comma-separated):")
    print(", ".join(functions))
    selected_functions = input("> ").split(',')
    
    elements = [elem.tag for elem in xml_root.iter()]
    
    for func in selected_functions:
        if func.strip() in functions:
            element = random.choice(elements)
            if func == 'find':
                print(f"Find first '{element}' element: xml_root.find('.//{element}')")
            elif func == 'findall':
                print(f"Find all '{element}' elements: xml_root.findall('.//{element}')")
            elif func == 'iter':
                print(f"Iterate over all elements: for elem in xml_root.iter('{element}'):")
            elif func == 'iterfind':
                print(f"Iterate over '{element}' elements: for elem in xml_root.iterfind('.//{element}'):")

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