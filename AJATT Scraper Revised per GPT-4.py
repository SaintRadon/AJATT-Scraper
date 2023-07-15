import requests
from bs4 import BeautifulSoup as BS
from bs4.element import Comment

BASE_URL = "http://www.alljapaneseallthetime.com/blog/"

def is_element_visible(element):
    """Checks if the HTML element is visible."""
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def extract_visible_text_from_page(url):
    """Fetches the page and extracts visible text."""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BS(resp.text, "html.parser")

    try:
        title = soup.find("h1", class_="entry-title").get_text().strip()
        main = soup.find("div", class_="entry-content")
        text = main.find_all(text=True)
        visible = filter(is_element_visible, text)
        visible_text = u" ".join(t.strip() for t in visible)
        return title, visible_text
    except AttributeError:
        print(f'Failed to extract information from {url}')
        return None, None

def fetch_links_from_homepage():
    """Fetches links from the homepage."""
    res = requests.get(BASE_URL + "all-japanese-all-the-time-ajatt-how-to-learn-japanese-on-your-own-having-fun-and-to-fluency/")
    soup = BS(res.text, "html.parser")
    links = [x.get("href") for x in soup.find_all("a") if x.get("href").startswith(BASE_URL)][5:]
    return links

def write_content_to_file(filename, links):
    """Writes the visible content of each link to the file."""
    with open(filename, mode='w', encoding="utf8") as f:
        for link in links:
            title, visible_text = extract_visible_text_from_page(link)
            if title and visible_text:
                f.write("# " + title + "\n")
                f.write(visible_text + "\n")

def main():
    """Main function to run the script."""
    links = fetch_links_from_homepage()
    write_content_to_file("AJATT TOC.md", links)

if __name__ == "__main__":
    main()
