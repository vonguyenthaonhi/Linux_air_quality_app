import pandas as pd
import streamlit as st
import pydeck as pdk


raw_file_path = "../../openaq.csv" #changer le chemin!!!!

print(f'Reading raw file at: {raw_file_path}')
try:
    data = pd.read_csv(
        raw_file_path,
        sep=";",  # Specify separator as semicolon
        header=0,  # The first row contains column names
        skipinitialspace=True,  # Ignore spaces after separators
        encoding='utf8'  # Ensure proper encoding for special characters
    )
    print("Raw file read successfully.")
except Exception as e:
    print(f"Error reading the raw file: {e}")
    exit(1)

print(data.columns)

# Séparer les coordonnées en latitude et longitude
coord_data = data['Coordinates'].str.split(',', expand=True)
if coord_data.shape[1] == 2:
    # Ajouter latitude et longitude au DataFrame existant sans décaler les autres colonnes
    data[['Latitude', 'Longitude']] = coord_data.astype(float)
    st.write("Données avec coordonnées séparées :", data[['Country Code', 'City', 'Location', 'Latitude', 'Longitude', 'Pollutant',
       'Source Name', 'Unit', 'Value', 'Last Updated', 'Country Label']])
else:
    st.error("Erreur : les coordonnées ne peuvent pas être séparées correctement. Veuillez vérifier le format.")

# Titre de l'application
st.title("Carte thermique des polluants")

# Ajouter un filtre pour sélectionner le type de polluant
pollutants = data['pollutant'].unique()
selected_pollutant = st.selectbox(
    "Sélectionnez un type de polluant :", 
    options=pollutants
)

# Filtrer les données en fonction du type de polluant sélectionné
filtered_data = data[data['pollutant'] == selected_pollutant]

# Message si aucune donnée n'est disponible
if filtered_data.empty:
    st.warning(f"Aucune donnée disponible pour le polluant '{selected_pollutant}'")
else:
    # Configurer la carte thermique
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        data=filtered_data,
        get_position=["longitude", "latitude"],
        get_weight="value",
        radiusPixels=60,
        opacity=0.8,
    )

    # Configurer la vue initiale
    view_state = pdk.ViewState(
        latitude=filtered_data["latitude"].mean(),
        longitude=filtered_data["longitude"].mean(),
        zoom=11,
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


# Define the Pydeck Layer
layer = pdk.Layer(
    'ScatterplotLayer',  # Specify the layer type
    data,  # The data source
    get_position='[Longitude, Latitude]',  # Columns for longitude and latitude
    get_fill_color='[200, 30, 0, 160]',  # RGBA color for the points
    get_radius=10000,  # Radius of the points
    pickable=True
)

# Set the initial view state
view_state = pdk.ViewState(
    latitude=data['Latitude'].mean(),
    longitude=data['Longitude'].mean(),
    zoom=4,
    pitch=50
)

# Create the Pydeck Deck
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "Coordinates: {Longitude}, {Latitude}"}))

