import streamlit as st
import pandas as pd
import pydeck as pdk

# Charger les données traitées depuis le fichier pickle
processed_file_path =  "../../processed_data.csv"

try:
    data = pd.read_csv(processed_file_path)
    print("Données chargées avec succès.")
except Exception as e:
    st.error(f"Erreur lors du chargement des données traitées : {e}")
    exit(1)

# Configuration de la navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Aller à :", 
    ["🏡 Accueil",  "ℹ️ Info du moment", "🗺️ Carte des polluants"]
)

# Page d'accueil
if options == "🏡 Accueil":
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

elif options == "ℹ️ Info du moment":
    st.subheader("Comme vous le savez, nos données sont régulièrement mises à jour. 📝")
    st.markdown(
        "<p style='font-size:16px;'> Voici la ville la plus et la moins polluée, avec les informations les plus récentes!</p>",
        unsafe_allow_html=True
    )
    st.divider()


# Afficher un filtre pour le type de polluant

    # Filtres pour le type de polluant
    pollutants = data['Pollutant'].unique()
    selected_pollutant = st.selectbox(
        "Sélectionnez un type de polluant :", 
        options=pollutants
    )
    st.divider()
    # Filtrer les données en fonction du polluant sélectionné
    filtered_data = data[data['Pollutant'] == selected_pollutant]

    # Effectuer l'agrégation sur les données filtrées
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

    # Pollution maximale et minimale
    pollution_maximale = statistiques_locations.iloc[0]
    pollution_minimale = statistiques_locations.iloc[-1]

    # Affichage du tableau de bord
    if selected_pollutant:
        st.subheader("Destination avec la Pollution Maximale")
        data_max = {
            "Métrique": ["Ville", "Pays", "Pollution Maximale", "Pollution Minimale", "Pollution Moyenne"],
            "Valeur": [
                pollution_maximale['City'],
                pollution_maximale['Country Label'],
                f"{pollution_maximale['max_pollution']:.2f}",
                f"{pollution_maximale['min_pollution']:.2f}",
                f"{pollution_maximale['avg_pollution']:.2f}"
            ]
        }
        data_max = pd.DataFrame(data_max)
        st.table(data_max)

        st.divider()

        st.subheader("Destination avec la Pollution Minimale")
        data_min = {
            "Métrique": ["Ville", "Pays", "Pollution Maximale", "Pollution Minimale", "Pollution Moyenne"],
            "Valeur": [
                pollution_minimale['City'],
                pollution_minimale['Country Label'],
                f"{pollution_minimale['max_pollution']:.2f}",
                f"{pollution_minimale['min_pollution']:.2f}",
                f"{pollution_minimale['avg_pollution']:.2f}"
            ]
        }
        data_min = pd.DataFrame(data_min)
        st.table(data_min)


# Page "Carte des polluants"
elif options == "🗺️ Carte des polluants":
    st.subheader("Vous avez une idée du pays où passer votre séjour? 🤔")

    st.markdown(
        "<p style='font-size:16px;'>Consultez notre carte mondiale pour visualiser les niveaux de pollution par région.</p>",
        unsafe_allow_html=True
    )
    st.divider()

    # Créer des colonnes pour afficher les filtres côte à côte
    col1, col2 = st.columns(2)

    # Filtres pour le type de polluant dans la première colonne
    with col1:
        pollutants = data['Pollutant'].unique()
        selected_pollutant = st.selectbox(
            "Sélectionnez un type de polluant :", 
            options=pollutants
        )

    # Filtres pour les pays dans la deuxième colonne
    with col2:
        countries = data['Country Label'].unique()
        selected_countries = st.multiselect(
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
        st.divider()

        st.subheader("Et si vous avez déjà une idée de la ville...")
        st.markdown("<p style='font-size:16px;'>Choisissez-la ici pour en savoir plus! 👇</p>",
        unsafe_allow_html=True
    )

        cities = filtered_data['City'].dropna().unique()
        cities_with_none = ['None'] + list(cities)
        selected_city = st.selectbox("Sélectionnez une ville :", options=cities)

        # les données pour la ville sélectionnée
        city_data = filtered_data[filtered_data['City'] == selected_city]

        # Calculer le classement des villes en fonction des niveaux de pollution moyens
        city_pollution = (
            filtered_data.groupby("City")["Value"]
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        city_pollution["Rang"] = city_pollution.index + 1  # Ajouter le classement

        # Trouver le rang de la ville sélectionnée
        if not city_data.empty:
            selected_city_rank = city_pollution[city_pollution["City"] == selected_city]
            st.divider()
            # Afficher les résultats
            st.subheader(f"Classement des villes pour le polluant : {selected_pollutant}")
            st.write(f"La ville **{selected_city}** est classée **#{selected_city_rank['Rang'].values[0]}** avec une pollution moyenne de **{selected_city_rank['Value'].values[0]:.2f}**.")

            # Afficher le classement
            st.table(city_pollution)

