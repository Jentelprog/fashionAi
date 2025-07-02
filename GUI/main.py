import streamlit as st
import lmstudio as lms
import json
import os
import re

models = [
    "meta-llama-llama-3.1-8b-instruct-qlora-malaysian-16k",
    "llava-1.6-mistral-7b",
    "model_fashion",
    "llava-phi-3-mini",
    "qwen2.5-omni-7b",
]

# App title
st.set_page_config(page_title="MABLOOK - Styliste IA")
st.title("MABLOOK - 👗 Styliste IA")
st.caption("Obtenez des suggestions de vêtements adaptées à votre profil")

# User inputs
st.subheader("🧍 Votre profil mode")
models1 = st.selectbox(
    "Sélectionnez le modèle LLM",
    models,
    index=0,
    help="Choisissez le modèle pour générer des recommandations. Le modèle par défaut est optimisé pour la mode.",
)
col1, col2 = st.columns(2)
with col1:
    height = st.number_input("Taille (cm)", min_value=100, max_value=250)
    weight = st.number_input("Poids (kg)", min_value=30, max_value=200)
    age = st.slider("Âge", 12, 80, 25)
    climate = st.selectbox("Climat", ["été", "hiver", "printemps", "automne"])
with col2:
    gender = st.selectbox("Genre", ["femme", "homme"])
    body_type = st.selectbox(
        "Type de morphologie", ["mince", "courbée", "athlétique", "grande taille"]
    )
    fashion_style = st.multiselect(
        "Style vestimentaire",
        ["décontracté", "formel", "tendance", "bohème", "sportif"],
    )
    occasion = st.selectbox(
        "Occasion", ["fête", "travail", "sortie décontractée", "mariage"]
    )

skin_tone = st.selectbox("Teint de peau", ["clair", "moyen", "foncé"])
veil = st.radio("Portez-vous un voile ?", ["oui", "non"])
hair_color = st.text_input("Couleur des cheveux", disabled=(veil == "oui"))
hair_style = st.text_input("Style de coiffure", disabled=(veil == "oui"))
eye_color = st.text_input("Couleur des yeux")
favorite_colors = st.text_input("Couleurs préférées (séparées par des virgules)")
face_shape = st.selectbox(
    "Forme du visage", ["ovale", "rond", "carré", "cœur", "diamant"]
)

# Load products
with open(
    r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\image_desc2\products.txt",
    "r",
) as f:
    products = f.read()
products = re.sub(r"\s+", " ", products.strip())  # Clean up product list

# Recommendation button
if st.button("🎯 Obtenir des recommandations"):
    # Create prompt
    prompt = f"""Vous êtes un assistant de stylisme professionnel spécialisé dans les recommandations vestimentaires basées sur le profil utilisateur.

Votre tâche est de recommander **exactement trois** articles de vêtements à partir d’une liste de produits. Vous devez uniquement fournir une **réponse JSON valide**, sans texte supplémentaire, sans explication, sans balises Markdown.

### Profil de l'utilisateur
- Taille : {height}
- Poids : {weight}
- Genre : {gender}
- Morphologie : {body_type}
- Teint : {skin_tone}
- Porte un voile : {veil}
- Couleur des cheveux : {hair_color}
- Style de coiffure : {hair_style}
- Forme du visage : {face_shape}
- Couleur des yeux : {eye_color}
- Couleurs préférées : {favorite_colors}
- Âge : {age}
- Climat : {climate}
- Style vestimentaire préféré : {fashion_style}
- Occasion : {occasion}

### Format de sortie
Tu dois retourner **uniquement** ce format JSON valide (aucun texte autour) :

{{
  "recommendations": [
    {{
      "product_id": "1",
      "product_name": "BLOUSE_JASELIA",
      "reason": "Explication brève de pourquoi cet article est un bon choix."
    }},
    {{
      "product_id": "2",
      "product_name": "CHEMISE_JANSOU",
      "reason": "Explication brève de pourquoi cet article est un bon choix."
    }},
    {{
      "product_id": "3",
      "product_name": "DEBARDEUR_JOBI",
      "reason": "Explication brève de pourquoi cet article est un bon choix."
    }}
  ]
}}

✅ Important :
- Ne retourne **que** cet objet JSON.
- **Aucune explication avant ou après**.
- Pas de commentaires.
- Pas de texte en dehors de la structure JSON.
"""

    # Call model 
    model = lms.llm(models1)
    chat = lms.Chat()
    chat.add_user_message(prompt)
    with st.spinner("Génération des recommandations..."):
        response = model.respond(chat)

    # Clean and extract JSON
    def clean_output(raw):
        match = re.search(r"\{[\s\S]*\}", raw.strip())
        if match:
            return match.group(0)
        else:
            return ""

    output = clean_output(response.content)
    st.subheader("✨ Recommandations vestimentaires")
    st.code(output, language="json")

    try:

        output = output[output.index("{") :]  # Ensure we start from the first '{'
        if not output.endswith("]}"):
            output = output + "]}"
        recommendations = json.loads(output)
        image_dir = r"C:\Users\ilyes\OneDrive\Desktop\folders\code\stylistBotv2\web scrapin V2\images"
        if "recommendations" in recommendations:
            for item in recommendations["recommendations"]:
                st.markdown(f"**🆔 ID Produit :** {item['product_id']}")
                st.markdown(f"**👗 Nom du Produit :** {item['product_name']}")
                st.markdown(f"**💡 Pourquoi :** {item['reason']}")
                image_path = os.path.join(image_dir, f"{item['product_name']}.jpg")
                if os.path.exists(image_path):
                    # st.image(
                    #     image_path,
                    #     caption=item["product_name"],
                    #     width=300,
                    # )
                    st.markdown(
                        f"""
                    <div style='text-align: center;'>
                    <img src='file://{image_path}' width='300' style='margin: auto;'>
                    <p style='font-size: 16px;'>{item["product_name"]}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                else:
                    st.warning(f"⚠️ Image introuvable pour : {item['product_name']}")
                st.markdown("---")
        else:
            st.error("❌ Clé 'recommendations' manquante dans la réponse JSON.")
    except json.JSONDecodeError as e:
        st.error(f"❌ Erreur lors de l'analyse du JSON : {e}")
        st.text(output)
