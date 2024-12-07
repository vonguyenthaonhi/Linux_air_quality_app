import pandas as pd

# Chemins des fichiers
raw_file_path = "../openaq_data.csv"
processed_file_path = "../processed_data.csv"

print(f'Getting data file at: {raw_file_path}')

# Lire le fichier brut
try:
    data = pd.read_csv(
        raw_file_path,
        sep=";",  
        header=0,  
        skipinitialspace=True,  
        encoding='utf8'  
    )
    print("Raw file read successfully.")
except Exception as e:
    print(f"Error reading the raw file: {e}")
    exit(1)

# Extraire les coordonnées à partir de la colonne "Coordinates"
if 'Coordinates' in data.columns:
    coord_data = data['Coordinates'].str.split(',', expand=True)
    if coord_data.shape[1] == 2:
        data[['Latitude', 'Longitude']] = coord_data.astype(float)
    else:
        print("Erreur : les coordonnées ne peuvent pas être séparées correctement. Veuillez vérifier le format.")
        exit(1)
else:
    print("Erreur : la colonne 'Coordinates' est manquante.")
    exit(1)


# Traitements des données
data = data.dropna(subset=['Latitude', 'Longitude'])
data=data.drop(columns="Coordinates")
data=data.dropna(subset=['City','Country Label'])
data=data[data['Unit']!="ppm"]
data = data[data['Value'] >= 0]

data ["Last Updated"] = data ["Last Updated"].astype(str)
data ["Last Updated"] = data ["Last Updated"].str[:10]
data ["Last Updated"] = pd.to_datetime(data["Last Updated"], format='%Y-%m-%d', errors='coerce')
data = data[data['Last Updated'].dt.year == 2024]

data['City'] = data['City'].astype(str).str.title()
df_valid_cities=pd.read_csv("world_cities_clean.csv")
valid_cities = set(df_valid_cities['city'].str.strip().str.title())
data['City'] = data['City'].str.strip().str.title()
data = data[data['City'].isin(valid_cities)]


# Conversion des unités de concentration
molar_masses = {
    'O3': 48,     # Ozone
    'CO': 28,     # Monoxyde de carbone
    'NO2': 46,    # Dioxyde d'azote
    'SO2': 64,    # Dioxyde de soufre
    'PM10': None, # Particules (pas de conversion nécessaire)
    'PM2.5': None,# Particules fines (pas de conversion nécessaire)
    'NO': 30,     # Monoxyde d'azote
    'NOX': 38     # Moyenne pondérée
}

print("Converting 'Unit' to standard µg/m³ for comparison...")

def convert_to_ugm3(row):
    """
    Convertit les unités de concentration en µg/m³ et met à jour l'unité correspondante.
    """
    unit = row['Unit']
    pollutant = row['Pollutant']
    value = row['Value']
    
    
    molar_mass = molar_masses.get(pollutant, None)
    
    # Unité déjà en µg/m³ 
    if unit == 'µg/m³':
        return value, 'µg/m³'
    
    # Unité en ppm
    elif unit == 'ppm' and molar_mass:
        converted_value = value * (molar_mass / 24.45)  
        return converted_value, 'µg/m³'

    # Unité en ppb
    elif unit == 'ppb' and molar_mass:
        converted_value = value * (molar_mass / 24.45) / 1000 
        return converted_value, 'µg/m³'

    # Unité non supportée
    else:
        return value, unit 

data[['Value', 'Unit']] = data.apply(
    lambda row: pd.Series(convert_to_ugm3(row)), axis=1
)


try:
    data.to_csv(processed_file_path, index=False)
    print(f"Données traitées sauvegardées dans {processed_file_path}")
except Exception as e:
    print(f"Erreur lors de la sauvegarde des données traitées : {e}")