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
