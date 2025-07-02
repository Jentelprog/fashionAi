from parsel import Selector
import requests
import os
import re
import json

for j in range(1, 4):
    url = (
        "https://mabrouk.tn/categorie-produit/nouvelle-collection/page/" + str(j) + "/"
    )
    html = requests.get(url).text
    sel = Selector(text=html)

    # Extract all links
    # links = sel.css('a::attr(href)').getall()
    # print(links)
    # Extract all image URLs
    image_urls = sel.css("img.wp-post-image::attr(src)").getall()
    product_names = sel.css("h3.font-titles a.color-dark::text").getall()
    products_links = sel.css("h3.font-titles a.color-dark::attr(href)").getall()
    print(len(image_urls))
    print(len(product_names))
    print(len(products_links))
    for i in range(len(product_names)):
        # Get the image name from the URL
        # Remove tabs, newlines, and extra spaces, then replace spaces with underscores
        clean_name = re.sub(r"\s+", " ", product_names[i]).strip()
        image_name = clean_name.replace(" ", "_") + ".jpg"
        # Download the image
        response = requests.get(
            image_urls[i * 2]
        )  # Adjusted to match the product name index
        # Check if the response is successful
        if response.status_code == 200:
            with open(
                "C:/Users/ilyes/OneDrive/Desktop/folders/code/stylistBotv2/web scraping V3/images/"
                + image_name,
                "wb",
            ) as f:
                f.write(response.content)
            print(f"Downloaded {image_name}")
        else:
            print(f"Failed to download {image_name}")
        # Save product details to a JSON file
        product_details = {
            "img_path": image_name,
            "image_url": image_urls[i * 2],
            "product_link": products_links[i],
        }
        with open(
            "C:/Users/ilyes/OneDrive/Desktop/folders/code/stylistBotv2/web scraping V3/products.json",
            "a",
        ) as json_file:
            json.dump(product_details, json_file, indent=4)
            json_file.write("\n")