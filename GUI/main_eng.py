import streamlit as st
import json
import os
import re
from openai import OpenAI
import difflib

# Initialize OpenAI client for LM Studio
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")

models = [
    "meta-llama-llama-3.2-1b-instruct-qlora-malaysian-16k-i1",
    "model_fashion",
    "llava-1.6-mistral-7b",
    "meta-llama-llama-3.1-8b-instruct-qlora-malaysian-16k",
    "llama-3-8b-lexi-uncensored",
    "text-embedding-nomic-embed-text-v1.5",
    "DeepSeek-R1-Distill-Qwen-1.5B",
    "meta-llama-Llama-3.2-3B-Instruct-untied",
]

# App title
st.set_page_config(page_title="AI Fashion Stylist")
st.title("\U0001f457 AI Fashion Stylist")
st.caption("Get clothing suggestions based on your profile")

# User inputs
st.subheader("\U0001f9cd Your Fashion Profile")
models1 = st.selectbox(
    "Select LLM Model",
    models,
    index=0,
    help="Choose the model to generate recommendations.",
)
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm)", min_value=160, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=60, max_value=200)
    age = st.slider("Age", 12, 80, 18)
    climate = st.selectbox("Climate", ["summer", "winter", "spring", "fall"])
with col2:
    gender = st.selectbox("Gender", ["female", "male"])
    body_type = st.selectbox("Body Type", ["slim", "curvy", "athletic", "plus-size"])
    fashion_style = st.multiselect(
        "Fashion Style", ["casual", "formal", "trendy", "boho", "sporty"]
    )
    occasion = st.selectbox("Occasion", ["party", "work", "casual outing", "wedding"])

skin_tone = st.selectbox("Skin Tone", ["fair", "medium", "dark"])
veil = st.radio("Do you wear a veil?", ["yes", "no"])
hair_color = st.text_input("Hair Color", disabled=(veil == "yes"))
hair_style = st.text_input("Hair Style", disabled=(veil == "yes"))
eye_color = st.text_input("Eye Color")
favorite_colors = st.text_input("Favorite Colors (comma separated)")
face_shape = st.selectbox("Face Shape", ["oval", "round", "square", "heart", "diamond"])

# Load products
with open(
    r"C:\\Users\\ilyes\\OneDrive\\Desktop\\folders\\code\\stylistBotv2\\image_desc2\\products.txt",
    "r",
) as f:
    products = re.sub(r"\s+", " ", f.read().strip())

# Recommendation button
if st.button("\U0001f3af Get Recommendations"):
    # Create prompt
    prompt = f"""You are a professional fashion stylist and trend expert.

Your task is to recommend the most suitable clothing items from a given list of available products, based on the user's physical features, preferences, and the context of the occasion.

### User Profile
- Height: {height}
- Weight: {weight}
- Gender: {gender}
- Body type(s): {body_type}
- Skin tone: {skin_tone}
- Wears a veil: {veil}
- Hair color: {hair_color}
- Hair style: {hair_style}
- Face shape(s): {face_shape}
- Eye color: {eye_color}
- Favorite colors: {favorite_colors}
- Age: {age}
- Climate: {climate}
- Preferred fashion style(s): {fashion_style}
- Occasion: {occasion}

### Task
From the available products, recommend clothing items that best match the user's profile and the occasion. Your selection must be:
- Aligned with the user's body type, skin tone, and fashion preferences.
- Align the color palette with the user's favorite colors and skin tone.
- Consider the user's age and the occasion.
- Suitable for the occasion and climate.
- Stylish, fashionable, and modern.
- Ordered by best match: from most suitable to least suitable.
- Provide a brief reason for each recommendation.
- make sure that the recommendations are diverse in style and type.
- make sure that the recommendations name and id are exactly the same as in the products list and return theme as they are don't add anythink to theme.
### Recommendation Priorities (from highest to lowest) ###
1. STRICTLY adhere to the user's FAVORITE COLOR.
2. Ensure suitability for the OCCASION.
3. Match the user's STYLE PREFERENCE.
4. Consider BODY TYPE and CLIMATE.
"""
    json_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "fashion_recommendations",
            "schema": {
                "type": "object",
                "properties": {
                    "recommendations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "product_id": {"type": "string"},
                                "product_name": {"type": "string"},
                                "reason": {"type": "string"},
                            },
                            "required": ["product_id", "product_name", "reason"],
                        },
                        "minItems": 3,
                        "maxItems": 10,
                    }
                },
                "required": ["recommendations"],
            },
        },
    }
    fe = open(
        r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\GUI\context1.txt",
        "r",
    )
    content = fe.read()
    fe.close()
    messages = [
        {
            "role": "system",
            "content": content,
        },
        {"role": "user", "content": prompt},
    ]
    with st.spinner("Generating recommendations..."):
        completion = client.chat.completions.create(
            model=models1,
            messages=messages,
            response_format=json_schema,
        )
        output = json.loads(completion.choices[0].message.content)
        output = json.dumps(output, indent=2, ensure_ascii=False)
    st.subheader("\u2728 Recommended Clothes")
    st.code(output, language="json")

    try:
        recommendations = json.loads(output)
        f = open(
            r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scraping V3\products.json",
            "r",
        )
        products_links = json.loads(f.read())
        f.close()
        products = os.listdir(
            r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scraping V3\images"
        )
        # products = [p.replace(".jpg", "") for p in products]
        image_dir = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scraping V3\images"
        if "recommendations" in recommendations:
            for item in recommendations["recommendations"]:
                product = difflib.get_close_matches(
                    item["product_name"].upper(), products
                )
                st.write(product[0] if product else "No close match found for :")
                st.write(item["product_name"])
                item["product_name"] = product[0] if product else "unknown_product"
                item["product_name"] = item["product_name"].replace(" ", "_")
                if item["product_name"][-4:] == ".jpg":
                    item["product_name"] = item["product_name"][:-4]
                img = item["product_name"] + ".jpg"
                image_path = os.path.join(image_dir, img)
                if not os.path.exists(image_path):
                    continue
                link = "https://mabrouk.tn/categorie-produit/nouvelle-collection/"
                for productx in products_links["items"]:
                    if productx["img_path"] == img:
                        link = productx["product_link"]
                        break
                col3, col4 = st.columns(2)
                with col3:
                    st.markdown(f"**\U0001f194 Product ID:** {item['product_id']}")
                    st.markdown(
                        f"**\U0001f457 Product Name:** [{item['product_name']}]({link})"
                    )
                    st.markdown(f"**\U0001f4a1 Reason:** {item['reason']}")
                with col4:
                    st.image(
                        image_path,
                        caption=item["product_name"],
                        use_container_width=True,
                    )
                st.markdown("---")
            st.session_state["recommendations"] = recommendations
            st.session_state["prompt"] = prompt
        else:
            st.error("\u274c No 'recommendations' key in JSON response.")
    except json.JSONDecodeError as e:
        st.error(f"\u274c Failed to parse JSON: {e}")
        st.text(output)
if st.button("\U0001f4e5 Save Recommendations"):
    if "recommendations" in st.session_state and "prompt" in st.session_state:
        save_data = {
            "prompt": st.session_state["prompt"],
            "recommendations": st.session_state["recommendations"],
        }
        st.write("Saving recommendations...")
        file_path = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\recommendations.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = [existing_data]
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        existing_data.append(save_data)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        st.success("\U0001f4be Recommendations saved successfully!")
    else:
        st.warning("⚠️ No recommendations to save. Please generate them first.")
