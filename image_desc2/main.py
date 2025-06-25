import lmstudio as lms
import os
import cv2
import json

model = lms.llm("llava-1.6-mistral-7b")

image_dir = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scrapin V2\images"
output_data = ""
for image in os.listdir(image_dir):
    CLOTHING_ITEM=image.split(".")[0]
    prompt = """You are a fashion analysis AI.

Given an image of a person, describe in detail only the clothing item specified below. Do not describe any other clothing, accessories, the person, or the background.

Clothing item to describe: {CLOTHING_ITEM}
the description should include:
- Type of clothing (e.g., dress, shirt, pants)
- Color
- Fabric/material
- Style (e.g., casual, formal, sporty)
in one line, no more than 20 words.
"""
    image_path=os.path.join(image_dir,image)
    img=lms.prepare_image(image_path)
    chat= lms.Chat()
    chat.add_user_message(prompt, images=[img])
    response = model.respond(chat)
    print(f"Image: {image}")
    print(response.content)
    # Save the response to a file
    output_data += "\n"+ image +":"+response.content.strip()

f= open("products.txt", "w")
f.write(output_data)