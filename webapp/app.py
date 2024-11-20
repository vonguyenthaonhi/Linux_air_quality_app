import streamlit as st
import pandas as pd
import pydeck as pdk

# Charger les données traitées depuis le fichier pickle
processed_file_path =  "../processed_data.pkl"

try:
    data = pd.read_pickle(processed_file_path)
    print("Données chargées avec succès.")
except Exception as e:
    st.error(f"Erreur lors du chargement des données traitées : {e}")
    exit(1)

# Configuration de la navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Aller à :", 
    ["Accueil", "Carte des polluants"]
)

# Page d'accueil
if options == "Accueil":
    st.title("Bienvenue sur l'application de visualisation des polluants 🌍")
    st.markdown("""
        Cette application interactive vous permet d'explorer les niveaux de pollution dans différentes régions. 
        Voici ce que vous pouvez faire :
        
        - **Carte des polluants** : Visualisez les polluants tels que NO2, CO, SO2 ou PM2.5 sur une carte thermique.
        - **Filtres dynamiques** : Sélectionnez un type de polluant et un pays pour ajuster la visualisation.
        
        ### Objectifs de l'application
        - Fournir une vue d'ensemble des données sur la qualité de l'air.
        - Identifier les zones les plus affectées par la pollution.
        - Aider les chercheurs et décideurs à mieux comprendre les impacts environnementaux.

        ### Instructions
        - Naviguez via la barre latérale pour accéder aux fonctionnalités.
        - Sélectionnez vos filtres pour personnaliser l'affichage.

        **Commencez dès maintenant en sélectionnant "Carte des polluants" dans la barre latérale.** 🚀
    """)

# Page "Carte des polluants"
elif options == "Carte des polluants":
    st.title("Carte thermique des polluants")


        # Ajouter les filtres dans la barre latérale
    st.sidebar.title("Filtres")

    # Filtres pour le type de polluant
    pollutants = data['Pollutant'].unique()
    selected_pollutant = st.sidebar.selectbox(
        "Sélectionnez un type de polluant :", 
        options=pollutants
    )

    # Filtres pour les pays (multiple selection or All countries)
    countries = data['Country Label'].unique()
    selected_countries = st.sidebar.multiselect(
        "Sélectionnez un ou plusieurs pays :", 
        options=["All"] + list(countries),
        default=["All"]  # Default to "All" countries selected
    )

    if "All" in selected_countries:
        # If "All" is selected, show data for the selected pollutant across all countries
        filtered_data = data[data['Pollutant'] == selected_pollutant]
    else:
        # Otherwise, filter data for the selected pollutant and countries
        filtered_data = data[
            (data['Pollutant'] == selected_pollutant) & 
            (data['Country Label'].isin(selected_countries))
        ]

    # Message si aucune donnée n'est disponible
    if filtered_data.empty:
        st.warning(f"Aucune donnée disponible pour '{selected_pollutant}' dans '{selected_countries}'")
    else:
        # Configurer la carte thermique
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=filtered_data,
            get_position=["Longitude", "Latitude"],
            get_weight="Value",
            radiusPixels=60,
            opacity=0.8,
        )

        # Configurer la vue initiale
        view_state = pdk.ViewState(
            latitude=filtered_data["Latitude"].mean(),
            longitude=filtered_data["Longitude"].mean(),
            zoom=5,
            pitch=50,
        )

        # Configurer la carte Pydeck
        deck = pdk.Deck(
            layers=[heatmap_layer],
            initial_view_state=view_state,
            tooltip={"html": "<b>Valeur:</b> {value}", "style": {"color": "white"}},
        )

        # Afficher la carte dans Streamlit
        st.pydeck_chart(deck)