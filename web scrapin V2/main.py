from parsel import Selector
import requests
import os
import re

for j in range(1, 5):
    url = "https://mabrouk.tn/categorie-produit/nouvelle-collection/page/"+str(j)+"/"
    html = requests.get(url).text

    sel = Selector(text=html)

    # Extract all links
    #links = sel.css('a::attr(href)').getall()
    #print(links)
    # Extract all image URLs
    image_urls = sel.css('img.wp-post-image::attr(src)').getall()
    product_names = sel.css('h3.font-titles a.color-dark::text').getall()
    print(len(image_urls))
    print(len(product_names))
    for i in range(len(image_urls)):
        # Get the image name from the URL
        # Remove tabs, newlines, and extra spaces, then replace spaces with underscores
        clean_name = re.sub(r'\s+', ' ', product_names[i//2]).strip()
        image_name = clean_name.replace(" ", "_") + ".jpg"
        # Download the image
        response = requests.get(image_urls[i])  # Adjusted to match the product name index
        # Check if the response is successful
        if response.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download {image_name}")