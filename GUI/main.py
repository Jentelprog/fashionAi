import streamlit as st
import lmstudio as lms
import json
import os
import re
models=["meta-llama-llama-3.1-8b-instruct-qlora-malaysian-16k","llava-1.6-mistral-7b","model_fashion","llava-phi-3-mini","qwen2.5-omni-7b"]
# App title
st.set_page_config(page_title="AI Fashion Stylist")
st.title("👗 AI Fashion Stylist")
st.caption("Get clothing suggestions based on your profile")


# User inputs
st.subheader("🧍 Your Fashion Profile")
models1=st.selectbox("Select LLM Model", models, index=0, help="Choose the model to generate recommendations. The default is a fashion-specific model.")
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Height (cm)", min_value=100, max_value=250)
    weight = st.number_input("Weight (kg)", min_value=30, max_value=200)
    age = st.slider("Age", 12, 80, 25)
    climate = st.selectbox("Climate", ["summer", "winter", "spring", "fall"])
with col2:
    gender = st.selectbox("Gender", ["female", "male"])
    body_type = st.selectbox("Body Type", ["slim", "curvy", "athletic", "plus-size"])
    fashion_style = st.multiselect("Fashion Style", ["casual", "formal", "trendy", "boho", "sporty"])
    occasion = st.selectbox("Occasion", ["party", "work", "casual outing", "wedding"])

skin_tone = st.selectbox("Skin Tone", ["fair", "medium", "dark"])
veil = st.radio("Do you wear a veil?", ["yes", "no"])
hair_color = st.text_input("Hair Color", disabled=(veil == "yes"))
hair_style = st.text_input("Hair Style", disabled=(veil == "yes"))
eye_color = st.text_input("Eye Color")
favorite_colors = st.text_input("Favorite Colors (comma separated)")
face_shape = st.selectbox("Face Shape", ["oval", "round", "square", "heart", "diamond"])

f=open(r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\image_desc2\products.txt","r")
products=f.read()
products = products.replace("\n", " ")  # Clean up product list
products = re.sub(r"\s+", " ", products)  # Remove extra spaces
# Submit button
if st.button("🎯 Get Recommendations"):
    # Create prompt for LLM
    prompt =f"""You are a professional fashion stylist and trend expert.

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
From the available products , recommend **three** clothing items that best match the user's profile and the occasion. Your selection must be:
- Aligned with the user's body type, skin tone, and fashion preferences.
- Suitable for the occasion and climate.
- Stylish, fashionable, and modern.
- Ordered by best match: from most suitable to least suitable.

### Output Format
Return the result in valid JSON format like this:

{{
  "recommendations": [
    {{
      "product_id": "1",
      "product_name": "BLOUSE_JASELIA",
      "reason": "Brief explanation why it's the best match"
    }},
    {{
      "product_id": "2",
      "product_name": "BLOUSE_JAXS",
      "reason": "Brief explanation why it's a good match"
    }},
    {{
      "product_id": "3",
      "product_name": "BLOUSE_JELAYA",
      "reason": "Brief explanation why it's also a suitable choice"
    }}
  ]
}}
"""


    # Chat with model
    # Init LLM model from LM Studio
    model = lms.llm(models1)
    chat = lms.Chat()
    chat.add_user_message(prompt)
    with st.spinner("Generating recommendations..."):
      response = model.respond(chat)
    # Clean response
    output = response.content.strip()
    if output.startswith("```"):
        output = re.sub(r"^```[a-z]*\n?", "", output)
        output = re.sub(r"\n?```$", "", output)
    st.subheader("✨ Recommended Clothes")
    #st.markdown(output)
    recommendations = json.loads(output)
    image_dir = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scrapin V2\images"
    
    # Display recommendations
    if "recommendations" in recommendations:
        for item in recommendations["recommendations"]:
            st.markdown(f"**Product ID:** {item['product_id']}")
            st.markdown(f"**Product Name:** {item['product_name']}")
            st.markdown(f"**Reason:** {item['reason']}")
            st.markdown("---")
            st.image(os.path.join(image_dir, f"{item['product_name']}.jpg"), caption=item['product_name'], use_container_width=True)
    else:
        st.error("No recommendations found. Please check your input and try again.")