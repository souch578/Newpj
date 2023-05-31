import requests
from bs4 import BeautifulSoup

# Set the number of pages to scrape
num_pages = 20

# Base URL for the product listing
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"

# Lists to store the scraped data
product_urls = []
product_names = []
product_prices = []
product_ratings = []
product_reviews = []

# Loop through each page and scrape the data
for page in range(1, num_pages + 1):
    # Construct the URL for the current page
    url = base_url + str(page)

    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all the product listings on the page
    listings = soup.find_all("div", class_="sg-col-inner")

    # Iterate over each listing and extract the required information
    for listing in listings:
        # Extract the product URL
        product_url = listing.find("a", class_="a-link-normal")
        if product_url:
            product_urls.append("https://www.amazon.in" + product_url["href"])
        else:
            product_urls.append("Not available")

        # Extract the product name
        product_name = listing.find("span", class_="a-size-medium")
        if product_name:
            product_names.append(product_name.text.strip())
        else:
            product_names.append("Not available")

        # Extract the product price
        product_price = listing.find("span", class_="a-price-whole")
        if product_price:
            product_prices.append(product_price.text.strip())
        else:
            product_prices.append("Not available")

        # Extract the product rating
        product_rating = listing.find("span", class_="a-icon-alt")
        if product_rating:
            product_ratings.append(product_rating.text.strip())
        else:
            product_ratings.append("Not available")

        # Extract the number of reviews
        product_review = listing.find("span", class_="a-size-base")
        if product_review:
            product_reviews.append(product_review.text.strip())
        else:
            product_reviews.append("Not available")

# Print the scraped data
for i in range(len(product_urls)):
    print("Product URL:", product_urls[i])
    print("Product Name:", product_names[i])
    print("Product Price:", product_prices[i])
    print("Product Rating:", product_ratings[i])
    print("Number of Reviews:", product_reviews[i])
    print()

