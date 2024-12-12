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
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            display: flex;
            justify-content: center; /* Centrer horizontalement */
            align-items: flex-start; /* Positionner le conteneur en bas */
            padding-top: 10vh; /* Descendre le conteneur de 10% de la hauteur de la page */
            height: 100vh; /* Prendre toute la hauteur de la page */
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.85); /* Fond semi-transparent */
            padding: 2rem;
            border-radius: 15px; /* Bords arrondis */
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3); /* Légère ombre */
            max-width: 900px; /* Largeur maximale plus large */
            text-align: justify; /* Texte justifié */
            line-height: 1.6; /* Espacement entre les lignes */
        }}
        h1 {{
            color: #2E8B57;  /* Couleur verte pour le titre */
            margin-bottom: 1rem;
            text-align: center; /* Centrer le titre */
        }}
        </style>
    """,
        unsafe_allow_html=True,
    )


background_image_url = "https://img.freepik.com/free-photo/top-view-camera-with-hat-compass_23-2148315771.jpg?t=st=1733214407~exp=1733218007~hmac=8c9dd03afdfa4bf48c121c31400e74aa9fd7d930534d056c6ab9f6da6e86a731&w=2000"


st.sidebar.title("Navigation")
options = st.sidebar.radio(
    "Aller à :",
    [
        "🏡 Accueil",
        "ℹ️ Info du moment",
        "🗺️ Carte des polluants",
        "📍 Infos touristiques de la ville",
    ],
)

##### Page d'accueil

if options == "🏡 Accueil":
    set_png_as_page_bg_from_url(background_image_url)

    st.title("Bienvenue sur ClimAventure 🌍")
    st.markdown(
        """
        ClimAventure est une application innovante conçue pour vous informer sur la qualité de l'air tout en vous offrant des compléments d'informations touristiques. 
        Notre priorité est de vous permettre de découvrir les niveaux de pollution dans les régions et villes de votre choix, tout en enrichissant votre expérience de voyage avec des données culturelles et pratiques.

        ### Fonctionnalités principales :
        
        - **Qualité de l'air** : Consultez des données précises sur les niveaux de pollution (NO2, CO, SO2, PM2.5, et autres polluants) pour chaque destination.
        - **Informations complémentaires** : Accédez à des descriptions touristiques pour en apprendre davantage sur l’histoire, les monuments emblématiques et les spécificités locales, grâce à des résumés interactifs de Wikipédia.
        - **Planification simplifiée** : Trouvez des outils pour organiser facilement votre voyage :
            - Réservez votre hébergement sur Booking.com.
            - Consultez les guides et avis sur TripAdvisor.
            - Planifiez vos trajets avec Rome2Rio.
            - Visionnez des vidéos inspirantes sur YouTube.

        ### Pourquoi utiliser ClimAventure ?
        - **Priorité à la qualité de l'air** : Prenez des décisions éclairées grâce à une visualisation claire des niveaux de pollution.
        - **Complément d'informations touristiques** : Enrichissez votre voyage avec des données culturelles et pratiques sans effort.
        - **Voyage responsable et bien préparé** : Combinez environnement et exploration pour une aventure harmonieuse.

        ### Comment utiliser l'application ?
        1. **Explorez la carte des polluants** : Identifiez les régions ou villes avec des niveaux de pollution adaptés à vos attentes.
        2. **Découvrez les atouts touristiques** : Apprenez-en davantage sur votre destination grâce à des informations complémentaires.
        3. **Planifiez votre séjour** : Profitez des outils intégrés pour organiser chaque détail de votre voyage.

        **Avec ClimAventure, soyez informé, soyez inspiré, et faites de votre voyage une expérience responsable !** 🌍
    """
    )
    image_path = "../image/11zon_cropped.png"

    image = Image.open(image_path)

    width, height = image.size
    new_size = (width // 6, height // 6)
    resized_image = image.resize(new_size)

    st.image(
        resized_image,
        caption="ClimAventure - Air Quality",
        use_container_width=False,
    )

elif options == "ℹ️ Info du moment":
    st.subheader(
        "Comme vous le savez, nos données sont régulièrement mises à jour. 📝"
    )
    st.markdown(
        "<p style='font-size:16px;'> Voici la ville la plus et la moins polluée, avec les informations les plus récentes!</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    pollutants = data["Pollutant"].unique()
    selected_pollutant = st.selectbox(
        "Sélectionnez un type de polluant :", options=pollutants
    )
    st.divider()

    filtered_data = data[data["Pollutant"] == selected_pollutant]

    statistiques_locations = (
        filtered_data.groupby(["City", "Country Label"])
        .agg(
            max_pollution=("Value", "max"),
            min_pollution=("Value", "min"),
            avg_pollution=("Value", "mean"),
        )
        .reset_index()
        .sort_values(by="avg_pollution", ascending=False)
    )

    pollution_maximale = statistiques_locations.iloc[0]
    pollution_minimale = statistiques_locations.iloc[-1]

    if selected_pollutant:
        st.subheader("Destination avec la Pollution Maximale")
        data_max = {
            "Métrique": [
                "Ville",
                "Pays",
                "Pollution Maximale",
                "Pollution Minimale",
                "Pollution Moyenne",
            ],
            "Valeur": [
                pollution_maximale["City"],
                pollution_maximale["Country Label"],
                f"{pollution_maximale['max_pollution']:.2f}",
                f"{pollution_maximale['min_pollution']:.2f}",
                f"{pollution_maximale['avg_pollution']:.2f}",
            ],
        }
        data_max = pd.DataFrame(data_max)
        st.table(data_max)

        st.divider()

        st.subheader("Destination avec la Pollution Minimale")
        data_min = {
            "Métrique": [
                "Ville",
                "Pays",
                "Pollution Maximale",
                "Pollution Minimale",
                "Pollution Moyenne",
            ],
            "Valeur": [
                pollution_minimale["City"],
                pollution_minimale["Country Label"],
                f"{pollution_minimale['max_pollution']:.2f}",
                f"{pollution_minimale['min_pollution']:.2f}",
                f"{pollution_minimale['avg_pollution']:.2f}",
            ],
        }
        data_min = pd.DataFrame(data_min)
        st.table(data_min)


##### Page "Carte des polluants"

elif options == "🗺️ Carte des polluants":
    st.subheader(
        "Vous avez une idée du pays où passer votre séjour? 🤔"
    )

    st.markdown(
        "<p style='font-size:16px;'>Consultez notre carte mondiale pour visualiser les niveaux de pollution par région.</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        countries = sorted(data["Country Label"].unique())
        selected_countries = st.multiselect(
            "Sélectionnez un ou plusieurs pays :",
            options=["All"] + list(countries),
            default=["All"],
        )

    with col2:
        if "All" in selected_countries:
            pollutants = sorted(data["Pollutant"].unique())
        else:
            filtered_data_for_countries = data[
                data["Country Label"].isin(selected_countries)
            ]
            pollutants = sorted(
                filtered_data_for_countries["Pollutant"].unique()
            )

        if not pollutants:
            st.warning(
                "Aucun polluant disponible pour le(s) pays sélectionné(s)."
            )
            selected_pollutant = None
        else:
            selected_pollutant = st.selectbox(
                "Sélectionnez un type de polluant :",
                options=pollutants,
            )

    if selected_pollutant:
        # Limites normales pour chaque polluant
        pollutant_limits = {
            "O3": "100 µg/m³ (8h moyenne, OMS)",
            "CO": "10 mg/m³ (8h moyenne, OMS)",
            "NO2": "40 µg/m³ (annuel, OMS)",
            "SO2": "20 µg/m³ (24h moyenne, OMS)",
            "PM10": "20 µg/m³ (annuel, OMS)",
            "PM2.5": "10 µg/m³ (annuel, OMS)",
            "NO": "Non spécifié (OMS)",
            "NOX": "Non spécifié (OMS)",
            "BC": "Non spécifié (OMS)",
            "PM1": "Non spécifié (OMS)",
        }

        # Conseils pour chaque polluant
        pollutant_tips = {
            "O3": "Évitez les activités physiques intenses en plein air lors des pics d'ozone.",
            "CO": "Assurez une bonne ventilation à l'intérieur et évitez les appareils de combustion non ventilés.",
            "NO2": "Réduisez l'exposition dans les zones à fort trafic routier.",
            "SO2": "Limitez le temps passé près des industries émettrices de SO2.",
            "PM10": "Portez un masque en cas de forte poussière dans l'air.",
            "PM2.5": "Utilisez des purificateurs d'air à l'intérieur pour limiter l'exposition.",
            "NO": "Limitez l'exposition à proximité des émissions industrielles.",
            "NOX": "Réduisez votre présence dans les zones à fort trafic automobile.",
            "BC": "Minimisez l'exposition près des moteurs diesel ou des combustions.",
            "PM1": "Aérez les espaces intérieurs et utilisez des purificateurs d'air.",
        }

        st.markdown(
            f"### À propos du polluant sélectionné : {selected_pollutant}"
        )
        st.markdown(
            f"- **Limite normale recommandée** : {pollutant_limits.get(selected_pollutant, 'Non disponible')}"
        )
        st.markdown(
            f"- **Conseil** : {pollutant_tips.get(selected_pollutant, 'Aucune recommandation disponible.')}"
        )
        st.markdown(
            f"[🌐 En savoir plus sur {selected_pollutant}](https://fr.wikipedia.org/wiki/{selected_pollutant})"
        )

        if "All" in selected_countries:
            filtered_data = data[
                data["Pollutant"] == selected_pollutant
            ]
        else:
            filtered_data = data[
                (data["Pollutant"] == selected_pollutant)
                & (data["Country Label"].isin(selected_countries))
            ]

        if filtered_data.empty:
            st.warning(
                f"Aucune donnée disponible pour '{selected_pollutant}' dans '{', '.join(selected_countries)}'."
            )
        else:
            heatmap_layer = pdk.Layer(
                "HeatmapLayer",
                data=filtered_data,
                get_position=["Longitude", "Latitude"],
                get_weight="Value",
                radiusPixels=60,
                opacity=0.8,
            )

            view_state = pdk.ViewState(
                latitude=filtered_data["Latitude"].mean(),
                longitude=filtered_data["Longitude"].mean(),
                zoom=5,
                pitch=50,
            )

            deck = pdk.Deck(
                layers=[heatmap_layer],
                initial_view_state=view_state,
                tooltip={
                    "html": "<b>Valeur:</b> {Value}",
                    "style": {"color": "white"},
                },
            )

            st.pydeck_chart(deck)
            st.divider()

            st.subheader("Classement des villes")
            cities = sorted(filtered_data["City"].dropna().unique())
            selected_city = st.selectbox(
                "Sélectionnez une ville :", options=cities
            )

            # Mise à jour des valeurs de session pour le pays et la ville
            if selected_countries and selected_countries[0] != "All":
                st.session_state["selected_country"] = (
                    selected_countries[0]
                )
            else:
                st.session_state["selected_country"] = None

            if cities:
                st.session_state["selected_city"] = selected_city
            else:
                st.session_state["selected_city"] = None

            city_data = filtered_data[
                filtered_data["City"] == selected_city
            ]

            city_pollution = (
                filtered_data.groupby("City")["Value"]
                .mean()
                .sort_values(ascending=False)
                .reset_index()
            )
            city_pollution["Rang"] = city_pollution.index + 1

            if not city_data.empty:
                selected_city_rank = city_pollution[
                    city_pollution["City"] == selected_city
                ]
                st.write(
                    f"La ville **{selected_city}** est classée **#{selected_city_rank['Rang'].values[0]}** avec une pollution moyenne de **{selected_city_rank['Value'].values[0]:.2f}**."
                )
                st.table(city_pollution)

##### Page Infos touristiques de la ville

elif options == "📍 Infos touristiques de la ville":
    st.subheader(
        "Envie d'en savoir plus sur la ville sélectionnée ? 🏙️"
    )

    st.markdown(
        "<p style='font-size:16px;'>Découvrez des informations touristiques sur la ville que vous avez sélectionnée grâce à Wikipédia et d'autres services interactifs.</p>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Récupérer les pays disponibles
    countries = sorted(data["Country Label"].unique())
    default_country = st.session_state.get("selected_country", None)
    selected_country = st.selectbox(
        "Sélectionnez un pays :",
        options=[None] + countries,
        index=([None] + countries).index(default_country),
    )

    # Filtrer les villes en fonction du pays sélectionné
    if selected_country:
        filtered_data = data[
            data["Country Label"] == selected_country
        ]
        cities = sorted(filtered_data["City"].dropna().unique())
    else:
        cities = []

    default_city = st.session_state.get("selected_city", None)
    selected_city = st.selectbox(
        "Sélectionnez une ville :",
        options=[None] + cities,
        index=(
            ([None] + cities).index(default_city)
            if default_city in cities
            else 0
        ),
    )

    # Mettre à jour les valeurs sélectionnées dans la session
    st.session_state["selected_country"] = selected_country
    st.session_state["selected_city"] = selected_city

    # Afficher les informations touristiques
    if selected_city and selected_country:
        st.write(
            f"Ville sélectionnée : **{selected_city}** ({selected_country})"
        )

        try:
            search_query = f"{selected_city}, {selected_country}"

            # Récupérer les informations depuis Wikipédia
            try:
                summary = wikipedia.summary(
                    search_query, sentences=3, auto_suggest=True
                )
                page = wikipedia.page(search_query)
            except (
                wikipedia.exceptions.DisambiguationError,
                wikipedia.exceptions.PageError,
            ):
                summary = wikipedia.summary(
                    selected_city, sentences=3, auto_suggest=True
                )
                page = wikipedia.page(selected_city)

            # Filtrer les images pertinentes
            keywords = [
                "landmark",
                "skyline",
                "view",
                "monument",
                "tourism",
                "architecture",
                "attraction",
            ]
            exclusion_keywords = ["flag", "logo", "map", "symbol"]
            filtered_images = [
                img
                for img in page.images
                if any(keyword in img.lower() for keyword in keywords)
                and not any(
                    keyword in img.lower()
                    for keyword in exclusion_keywords
                )
            ]

            # Vérifier la résolution des images
            def is_high_resolution(image_url):
                try:
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    width, height = image.size
                    return width > 500 and height > 300
                except Exception:
                    return False

            high_res_images = [
                img
                for img in filtered_images
                if is_high_resolution(img)
            ]

            # Afficher une image si disponible
            if high_res_images:
                st.image(
                    high_res_images[0],
                    caption=f"Image emblématique de {selected_city}",
                    use_container_width=True,
                )
            elif filtered_images:
                st.image(
                    filtered_images[0],
                    caption=f"Image de {selected_city}",
                    use_container_width=True,
                )

            # Afficher le résumé et les liens utiles
            st.markdown(f"### À propos de {selected_city}")
            st.write(summary)
            st.markdown(
                f"[🌐 Lire l'article complet sur Wikipédia]({page.url})"
            )

            city_encoded = urllib.parse.quote(selected_city)
            country_encoded = urllib.parse.quote(selected_country)

            st.markdown(
                f"""
            ### Planifiez votre voyage à {selected_city}
            - [Booking.com](https://www.booking.com/searchresults.html?ss={city_encoded})
            - [TripAdvisor](https://www.tripadvisor.com/Search?q={city_encoded})
            - [Rome2Rio](https://www.rome2rio.com/s/{city_encoded})
            - [🎥 Regardez des vidéos touristiques sur YouTube](https://www.youtube.com/results?search_query={city_encoded}+{country_encoded}+tourism)
            """
            )

        except wikipedia.exceptions.PageError:
            st.warning(
                f"Il n'y a pas de page Wikipédia pour **{selected_city}**."
            )
        except wikipedia.exceptions.DisambiguationError:
            st.warning(
                f"La recherche pour **{selected_city}** a renvoyé plusieurs résultats. Soyez plus précis."
            )
        except Exception as e:
            st.warning(
                "Une erreur s'est produite. Veuillez réessayer avec une autre ville."
            )
    else:
        st.warning(
            "Veuillez sélectionner une ville et un pays pour afficher les informations touristiques."
        )
