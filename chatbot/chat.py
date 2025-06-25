import lmstudio as lms
import os

model= lms.llm("model_fashion")
f=open(r"chatbot/products.txt","r")
products=f.read()
prompt= """You are a professional fashion stylist and trend expert.

Your task is to recommend the most suitable clothing items from a given list of available products, based on the user's physical features, preferences, and the context of the occasion.

###  User Profile
- Height: {height}
- Weight: {weight}
- Gender: {gender}
- Body type(s): {body_types}
- Skin tone: {skin_tones}
- Wears a veil: {veils}
- Hair color: {hair_color}
- Hair style: {hair_style}
- Face shape(s): {face_shapes}
- Eye color: {eye_color}
- Favorite colors: {favorite_colors}
- Age: {age}
- Climate: {climate}
- Preferred fashion style(s): {fashion_style}
- Occasion: {occasion}

### Available Products
{products}

### Task
From the available products above, recommend **three** clothing items that best match the user's profile and the occasion. Your selection must be:
- Aligned with the user's body type, skin tone, and fashion preferences.
- Suitable for the occasion and climate.
- Stylish, fashionable, and modern.
- Ordered by best match: from most suitable to least suitable.

### Output Format
Return your recommendations like this:
- Cloth 1: [product name] — brief explanation
- Cloth 2: [product name] — brief explanation
- Cloth 3: [product name] — brief explanation
"""
# height = input("Enter height: ")
# weight = input("Enter weight: ")
# gender = "female"
# body_types = input("Enter body types: ")
# skin_tones = input("Enter skin tones: ")
# veils = input("Does the user wear a veil? (yes/no): ")
# if veils.lower() == 'yes':
#     hair_color = "none"
#     hair_style = "none"
# else:
#     hair_color = input("Enter hair color: ")
#     hair_style = input("Enter hair style: ")
# face_shapes = input("Enter face shapes: ")
# eye_color = input("Enter eye color: ")
# favorite_colors = input("Enter favorite colors: ")
# age = input("Enter age: ")
# climate = input("Enter climate: ")
# fashion_style = input("Enter fashion style: ")
# occasion = input("Enter occasion: ")
height="170 cm"
weight="60 kg"
gender="female"
body_types="curvy"
skin_tones="medium"
veils="no"
hair_color="brown"
hair_style="long"
face_shapes="oval"
eye_color="brown"
favorite_colors="blue, green, red"
age="25"
climate="summer"
fashion_style="casual, trendy"
occasion="party"
products = products.replace("\n", ", ")
prompt=prompt.format(
    products=products,
    height=height,
    weight=weight,
    gender=gender,
    body_types=body_types,
    skin_tones=skin_tones,
    veils=veils,
    hair_color=hair_color,
    hair_style=hair_style,
    face_shapes=face_shapes,
    eye_color=eye_color,
    favorite_colors=favorite_colors,
    age=age,
    climate=climate,
    fashion_style=fashion_style,
    occasion=occasion
)
print("Prompt for the model:")
print(prompt)  # Print only the first 500 characters for brevity
response = model.respond(prompt)
print("Response from the model:")
print(response)