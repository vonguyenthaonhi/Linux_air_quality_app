import pandas as pd

##### Importation des bases

raw_path_air = "../openaq_data.csv"
world_cities_path = "../world_cities.csv"
processed_file_path = "../processed_data.csv"

print(f'Téléchargement de la base air quality à: {raw_path_air}')

try:
    data = pd.read_csv(
        raw_path_air,
        sep=";",  
        header=0,  
        skipinitialspace=True,  
        encoding='utf8'  
    )
    print("Données qualité de l'air importées avec succès.")
except Exception as e:
    print(f"Erreur lors de la lecture des données qualité de l'air : {e}")
    exit(1)

print(f'Téléchargement de la base des villes à: {world_cities_path}')

try:
    df_valid_cities = pd.read_csv(
        world_cities_path,
        encoding='utf8'  
    )
    print("Données des villes importées avec succès.")
except Exception as e:
    print(f"Erreur lors de la lecture des données des villes : {e}")
    exit(1)

#### Traitements des données

if 'Coordinates' in data.columns:
    coord_data = data['Coordinates'].str.split(',', expand=True)
    if coord_data.shape[1] == 2:
        data[['Latitude', 'Longitude']] = coord_data.astype(float)
    else:
        print("Erreur : format des coordonnées incorrect. Vérifiez le format.")
        exit(1)
else:
    print("Erreur : la colonne 'Coordinates' est manquante.")
    exit(1)

data = data.dropna(subset=['Latitude', 'Longitude'])
data = data.drop(columns="Coordinates")
data = data.dropna(subset=['City', 'Country Label'])
data = data[data['Unit'] != "ppm"]
data = data[data['Value'] >= 0]

data["Last Updated"] = data["Last Updated"].astype(str).str[:10]
data["Last Updated"] = pd.to_datetime(
    data["Last Updated"], format='%Y-%m-%d', errors='coerce'
)
data = data[data['Last Updated'].dt.year == 2024]

data['City'] = data['City'].astype(str).str.title()
valid_cities = set(df_valid_cities['name'].str.strip().str.title())
data['City'] = data['City'].str.strip().str.title()
data = data[data['City'].isin(valid_cities)]

##### Conversion des unités de concentration
molar_masses = {
    'O3': 48, 'CO': 28, 'NO2': 46, 'SO2': 64,
    'PM10': None, 'PM2.5': None, 'NO': 30, 'NOX': 38
}

print("Convertit les unités en µg/m³ pour comparaison...")

def convert_to_ugm3(row):
    """
    Convertit les unités en µg/m³ et met à jour l'unité correspondante.
    """
    unit = row['Unit']
    pollutant = row['Pollutant']
    value = row['Value']
    molar_mass = molar_masses.get(pollutant, None)
    
    if unit == 'µg/m³':
        return value, 'µg/m³'
    elif unit == 'ppm' and molar_mass:
        converted_value = value * (molar_mass / 24.45)
        return converted_value, 'µg/m³'
    elif unit == 'ppb' and molar_mass:
        converted_value = value * (molar_mass / 24.45) / 1000
        return converted_value, 'µg/m³'
    else:
        return value, unit 

data[['Value', 'Unit']] = data.apply(
    lambda row: pd.Series(convert_to_ugm3(row)), axis=1
)

##### Exportation des données
try:
    data.to_csv(processed_file_path, index=False)
    print(f"Données sauvegardées dans {processed_file_path}")
except Exception as e:
    print(f"Erreur lors de la sauvegarde des données : {e}")
