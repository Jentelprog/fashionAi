import lmstudio as lms
import os
import cv2
import json

model = lms.llm("llava-1.6-mistral-7b")

image_dir = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scrapin V2\images"
output_data = {}
for image in os.listdir(image_dir):
    CLOTHING_ITEM=image.split(".")[0]
    prompt = """You are a fashion analysis AI.

Given an image of a person, describe in detail only the clothing item specified below. Do not describe any other clothing, accessories, the person, or the background.

Clothing item to describe: {CLOTHING_ITEM}  // e.g., "red floral blouse"

Return your response in **valid JSON format** using the following structure:

{
  "item": {
    "name": "{CLOTHING_ITEM}",  // e.g., "red floral blouse"
    "type": "",         // e.g., blouse, dress, hoodie
    "color": "",        // dominant color(s)
    "material": "",     // e.g., cotton, silk, denim
    "pattern": "",      // e.g., floral, striped, solid
    "fit": "",          // e.g., loose, fitted, oversized
    "style": "",        // e.g., casual, formal, boho
    "sleeve": "",       // e.g., long, short, puffed
    "neckline": "",     // e.g., V-neck, round neck
    "length": "",       // e.g., cropped, hip-length
    "details": ""       // buttons, embroidery, ruffles, etc.
  }
}
"""
    image_path=os.path.join(image_dir,image)
    img=lms.prepare_image(image_path)
    chat= lms.Chat()
    chat.add_user_message(prompt, images=[img])
    response = model.respond(chat)
    print(f"Image: {image}")
    print(response.content)
    # Save the response to a file
    f1=open("descriptions.json", "w")
    json_res = json.dump(response.content,f1, indent=4)
    f1.close()
    f1=open("descriptions.json", "r")
    json_response=json.loads(f1.read())
    output_data[image_path]= json_response

output_file = "clothing_descriptions.json"
with open(output_file, "w") as f:
    json.dump(output_data, f, indent=4)