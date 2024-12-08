import streamlit as st
import pandas as pd
import pydeck as pdk
import wikipedia
import urllib.parse
import requests
from PIL import Image
from io import BytesIO

processed_file_path = "../../processed_data.csv"

try:
    data = pd.read_csv(processed_file_path)
    print("Données chargées avec succès.")
except Exception as e:
    st.error(f"Erreur lors du chargement des données traitées : {e}")
    exit(1)

def set_png_as_page_bg_from_url(image_url):
    st.markdown(f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding-top: 10vh;
            height: 100vh;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            max-width: 900px;
            text-align: justify;
            line-height: 1.6;
        }}
        h1 {{
            color: #2E8B57;
            margin-bottom: 1rem;
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)

background_image_url = (
    "https://img.freepik.com/free-photo/"
    "top-view-camera-with-hat-compass_23-2148315771.jpg?"
    "t=st=1733214407~exp=1733218007~hmac=8c9dd03afdfa4bf48c121c31"
    "400e74aa9fd7d930534d056c6ab9f6da6e86a731&w=2000"
)

st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Aller à :",
    [
        "🏡 Accueil", "ℹ️ Info du moment", 
        "🗺️ Carte des polluants", "📍 Infos touristiques de la ville"
    ]
)

##### Page d'accueil

if options == "🏡 Accueil":
    set_png_as_page_bg_from_url(background_image_url)
    st.title("Bienvenue sur ClimAventure 🌍")
    st.markdown("""
        ClimAventure est votre compagnon idéal pour découvrir le monde tout en 
        restant informé sur la qualité de l'air. Grâce à cette application 
        interactive, vous pouvez explorer les niveaux de pollution des villes 
        tout en accédant à des informations touristiques essentielles.

        ### Fonctionnalités principales :
        - **Niveaux de pollution** : Données détaillées sur la qualité de l'air.
        - **Informations touristiques** : Découvrez des résumés interactifs.
        - **Planification de voyage** : Accédez à des outils pratiques.

        ### Objectifs :
        - Planification de voyage éclairée avec des facteurs environnementaux.
        - Vue complète sur qualité de l'air et attractivité des villes.
        - Facilité de déplacements et séjours avec des outils pratiques.
    """)

elif options == "ℹ️ Info du moment":
    st.subheader("Données les plus récentes mises à jour régulièrement 📝")
    st.markdown(
        "<p style='font-size:16px;'>Découvrez les villes les plus et les moins polluées.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    pollutants = data['Pollutant'].unique()
    selected_pollutant = st.selectbox(
        "Sélectionnez un type de polluant :", 
        options=pollutants
    )

    filtered_data = data[data['Pollutant'] == selected_pollutant]

    statistiques_locations = (
        filtered_data.groupby(['City', 'Country Label'])
        .agg(
            max_pollution=('Value', 'max'),
            min_pollution=('Value', 'min'),
            avg_pollution=('Value', 'mean')
        )
        .reset_index()
        .sort_values(by='avg_pollution', ascending=False)
    )

    pollution_maximale = statistiques_locations.iloc[0]
    pollution_minimale = statistiques_locations.iloc[-1]

    if selected_pollutant:
        st.subheader("Destination avec la Pollution Maximale")
        data_max = {
            "Métrique": [
                "Ville", "Pays", "Pollution Maximale", 
                "Pollution Minimale", "Pollution Moyenne"
            ],
            "Valeur": [
                pollution_maximale['City'],
                pollution_maximale['Country Label'],
                f"{pollution_maximale['max_pollution']:.2f}",
                f"{pollution_maximale['min_pollution']:.2f}",
                f"{pollution_maximale['avg_pollution']:.2f}"
            ]
        }
        st.table(pd.DataFrame(data_max))

        st.subheader("Destination avec la Pollution Minimale")
        data_min = {
            "Métrique": [
                "Ville", "Pays", "Pollution Maximale", 
                "Pollution Minimale", "Pollution Moyenne"
            ],
            "Valeur": [
                pollution_minimale['City'],
                pollution_minimale['Country Label'],
                f"{pollution_minimale['max_pollution']:.2f}",
                f"{pollution_minimale['min_pollution']:.2f}",
                f"{pollution_minimale['avg_pollution']:.2f}"
            ]
        }
        st.table(pd.DataFrame(data_min))
