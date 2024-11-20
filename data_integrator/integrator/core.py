import pandas as pd

raw_file_path = "../../openaq_data.csv"
processed_file_path = "../../processed_data.pkl"

print(f'Reading raw file at: {raw_file_path}')
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

print(data.columns)

# Séparer les coordonnées en latitude et longitude
coord_data = data['Coordinates'].str.split(',', expand=True)
if coord_data.shape[1] == 2:
    data[['Latitude', 'Longitude']] = coord_data.astype(float)
else:
    print("Erreur : les coordonnées ne peuvent pas être séparées correctement. Veuillez vérifier le format.")
    exit(1)

# Sauvegarder les données traitées dans un fichier pickle
data.to_pickle(processed_file_path)
print(f"Données traitées sauvegardées dans {processed_file_path}")
