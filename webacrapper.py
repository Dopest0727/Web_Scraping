import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    """Get Website Content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching the page: {e}")
        return None

def parse_articles(soup):
    """Parse article with BeautifulSoup."""
    return soup.find_all(class_='relative w-full md:w-auto')

def extract_article_data(article):
    """Extract and return the title and price from a single article."""
    title_element = article.find(class_='hover:underline before:absolute before:inset-0 before:z-2')
    price_element = article.select_one(
        '.inline-block.whitespace-nowrap.text-right, '
        '.pointer-events-none.inline-flex.flex-col.items-start.align-middle.origin-top-left.rotate-4.pt-1\\.5'
    )

    title = title_element.text.strip() if title_element else "No Title Found"
    price = price_element.text.strip() if price_element else "No Price Found"
    return title, price

def display_article_data(articles):
    """Display the title and price of each article."""
    if not articles:
        print("No articles found.")
        return

    for article in articles:
        title, price = extract_article_data(article)
        print(f"Title: {title}, Price: {price}")

def get_page_data(page_url):
    """Fetch, parse, and display articles from a given webpage."""
    html_content = fetch_page_content(page_url)
    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    articles = parse_articles(soup)
    display_article_data(articles)

# Call the function
get_page_data('https://www.jula.se/catalog/tradgard/grillning/grillar/')
