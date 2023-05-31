import csv
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
product_descriptions = []
product_asins = []
product_manufacturers = []

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

        # Extract additional product details from the product URL
        if product_urls[-1] != "Not available":
            product_page = requests.get(product_urls[-1])
            product_soup = BeautifulSoup(product_page.content, "html.parser")

            # Extract the product description
            product_description = product_soup.find("div", id="productDescription")
            if product_description:
                product_descriptions.append(product_description.text.strip())
            else:
                product_descriptions.append("Not available")

            # Extract the ASIN (Amazon Standard Identification Number)
            product_asin = product_soup.find("th", string="ASIN")
            if product_asin:
                product_asins.append(product_asin.find_next_sibling("td").text.strip())
            else:
                product_asins.append("Not available")

            # Extract the product manufacturer
            product_manufacturer = product_soup.find("a", id="bylineInfo")
            if product_manufacturer:
                product_manufacturers.append(product_manufacturer.text.strip())
            else:
                product_manufacturers.append("Not available")

# Prepare the data for CSV writing
data = zip(product_urls, product_names, product_prices, product_ratings, product_reviews, product_descriptions, product_asins, product_manufacturers)

# Write the data to a CSV file
filename = "product_data.csv"
with open(filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Product URL", "Product Name", "Product Price", "Product Rating", "Number of Reviews",
                     "Product Description", "ASIN", "Manufacturer"])  # Write header row
    writer.writerows(data)

print("Data has been written to", filename)
