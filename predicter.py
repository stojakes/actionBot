import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

# Ścieżka do zapisanego modelu
model_path = 'model_lstm.keras'

# Sprawdzenie, czy model istnieje
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model nie został znaleziony w lokalizacji: {model_path}")

# Wczytanie modelu
model = load_model(model_path)

# Wczytanie danych do przewidywania
data_folder = 'dane_akcje'

all_data = []
for file_name in os.listdir(data_folder):
    file_path = os.path.join(data_folder, file_name)
    
    # Sprawdzenie, czy plik jest CSV i czy nie jest pusty
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_path)
        
        if len(df) == 0:
            print(f"Pominięto plik: {file_name} z powodu braku danych.")
            continue
        
        if 'Close' not in df.columns:
            print(f"Pominięto plik: {file_name} - brak kolumny 'Close'.")
            continue
        
        all_data.append((file_name, df['Close'].values))

if len(all_data) == 0:
    raise ValueError("Brak dostępnych danych do przewidywania.")

# Lista na prognozy
predictions = []

# Normalizacja i prognozowanie dla każdej firmy
scaler = MinMaxScaler(feature_range=(0, 1))

for file_name, data in all_data:
    data = data.reshape(-1, 1)

    # Normalizacja danych
    scaled_data = scaler.fit_transform(data)

    # Ustawienie zakresu look_back dla przewidywań
    look_back = 60

    # Wybór najnowszych danych do przewidywań
    test_data = scaled_data[-look_back:]

    # Przekształcenie danych na format dla LSTM
    test_data = np.reshape(test_data, (1, look_back, 1))

    # Prognoza kursu na podstawie najnowszych danych
    predicted_price_scaled = model.predict(test_data)

    # Odwzorowanie znormalizowanych danych na rzeczywiste wartości
    predicted_price = scaler.inverse_transform(predicted_price_scaled)

    # Zapis prognozy
    predictions.append({
        "Firma": file_name.replace('.csv', ''),
        "Przewidywana Cena": predicted_price[0][0]
    })

# Zapisanie prognoz do pliku CSV
predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv('prognozowane_ceny.csv', index=False)

print("Prognozy zostały zapisane w pliku 'prognozowane_ceny.csv'.")