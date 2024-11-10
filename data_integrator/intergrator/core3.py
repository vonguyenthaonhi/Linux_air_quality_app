import os
import streamlit as st
import pandas as pd
import pydeck as pdk

# Chemin vers le fichier CSV
csv_path = '../../data.csv'

# Vérification de l'existence du fichier
if not os.path.isfile(csv_path):
    st.error(f"Erreur : le fichier '{csv_path}' est introuvable. Veuillez vérifier le chemin.")
else:
    st.success(f"Le fichier '{csv_path}' a été trouvé avec succès.")

    # Lecture du fichier CSV directement sans modifier la première ligne
    data = pd.read_csv(csv_path, sep=";")

    # Afficher le DataFrame dans l'application Streamlit sans l'index
    st.dataframe(data)


    # Séparer les coordonnées en latitude et longitude
    coord_data = data['coordonnees'].str.split(',', expand=True)
    if coord_data.shape[1] == 2:
        # Ajouter latitude et longitude au DataFrame existant sans décaler les autres colonnes
        data[['latitude', 'longitude']] = coord_data.astype(float)
        st.write("Données avec coordonnées séparées :", data[['depcom', 'libcom', 'latitude', 'longitude']])
    else:
        st.error("Erreur : les coordonnées ne peuvent pas être séparées correctement. Veuillez vérifier le format.")

    # Configurer la carte pydeck pour visualiser les points de coordonnées
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_radius=1000,           # Rayon des points (ajustez si besoin)
        get_color=[255, 0, 0],     # Couleur des points en RGB (ici, rouge)
        pickable=True              # Permettre la sélection des points pour affichage
    )

    # Définir les paramètres de la vue initiale de la carte
    view_state = pdk.ViewState(
        latitude=data['latitude'].mean(),   # Centrage sur la latitude moyenne
        longitude=data['longitude'].mean(), # Centrage sur la longitude moyenne
        zoom=6,                             # Niveau de zoom
        pitch=0
    )

    # Créer la carte avec Streamlit
    st.pydeck_chart(pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "Commune: {libcom}\nNaissances: {naissances}"}  # Affiche le nom et le nombre de naissances
    ))

