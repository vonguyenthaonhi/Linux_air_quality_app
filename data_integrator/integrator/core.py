import pandas as pd


raw_file_path = "../../openaq_data.csv" 

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
    # Ajouter latitude et longitude au DataFrame existant sans afficher
    data[['Latitude', 'Longitude']] = coord_data.astype(float)
else:
    st.error("Erreur : les coordonnées ne peuvent pas être séparées correctement. Veuillez vérifier le format.")



