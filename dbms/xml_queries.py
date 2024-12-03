import sys
from lxml import etree

MOVIES_XML = "movies.xml"

def parse_xml():
    try:
        tree = etree.parse(MOVIES_XML)
        return tree
    except Exception as e:
        print(f"Error parsing XML file: {e}")
        sys.exit(1)

def search_by_id(movie_id):
    tree = parse_xml()
    title = tree.xpath(f"//Movie[@id='{movie_id}']/Title/text()")
    if title:
        return title[0]
    return

def search_by_director(director_name):
    tree = parse_xml()
    titles = tree.xpath(f"//Movie[contains(Director, '{director_name}')]/Title/text()")
    if titles:
        return titles
    return

def search_by_rating(min_rating):
    tree = parse_xml()
    actors = tree.xpath(f"//Movie[Rating/IMDb >= {min_rating}]/Cast/Actor/Name/text()")
    if actors:
        return actors
    return

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("\nUsage: python3 hw3_solutions.py [operation] [arguments]\nOperations: search_by_id <id>, search_by_director <keyword>, search_by_rating <rating>\n")

    operation = sys.argv[1].lower()

    if operation == "search_by_id":
        if len(sys.argv) != 3:
            sys.exit("Usage: search_by_id <id>")
        movie_id = sys.argv[2]
        result = search_by_id(movie_id)
        print(result)

    elif operation == "search_by_director":
        if len(sys.argv) != 3:
            sys.exit("Usage: search_by_director <keyword>")
        director_name = sys.argv[2]
        result = search_by_director(director_name)
        print(result)

    elif operation == "search_by_rating":
        if len(sys.argv) != 3:
            sys.exit("Usage: search_by_rating <rating>")
        try:
            rating = float(sys.argv[2])
        except ValueError:
            sys.exit("Rating should be a numeric value.")
        result = search_by_rating(rating)
        print(result)

    else:
        sys.exit("\nInvalid operation.\nOperations: search_by_id <id>, search_by_director <keyword>, search_by_rating <rating>\n")
