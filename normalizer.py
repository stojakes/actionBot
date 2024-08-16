import os
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Ścieżka do folderu z danymi
data_folder = 'dane_akcje'
model_path = 'model_lstm.keras'
scaler = MinMaxScaler(feature_range=(0, 1))

# Minimalny wzrost ceny, który uznamy za atrakcyjny (np. 5% wzrost)
threshold = 1.05

# Funkcja do wczytywania i normalizacji danych
def load_and_process_data(filepath):
    df = pd.read_csv(filepath)
    
    if 'Close' not in df.columns or df['Close'].isna().all():
        print(f"Plik {filepath} jest pusty lub nie zawiera kolumny 'Close'. Pomijanie pliku.")
        return None, None
    
    data = df['Close'].dropna().values.reshape(-1, 1)
    return scaler.fit_transform(data), df['Close']

# Wczytaj model LSTM
model = load_model(model_path)

# Przetwarzanie plików CSV i wybór firm z przewidywanym wzrostem cen
profitable_companies = []

for filename in os.listdir(data_folder):
    if not filename.endswith('.csv'):
        continue
    
    filepath = os.path.join(data_folder, filename)
    
    # Wczytaj dane i znormalizuj
    scaled_data, original_data = load_and_process_data(filepath)
    if scaled_data is None or original_data is None:
        continue
    
    # Tworzenie zestawu danych do przewidywania
    look_back = 60
    x_test = []
    for i in range(len(scaled_data) - look_back):
        x_test.append(scaled_data[i:(i + look_back), 0])
    
    if len(x_test) == 0:
        print(f"Brak wystarczającej liczby danych w pliku {filepath}.")
        continue
    
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    # Przewidujemy przyszłe ceny akcji
    predicted_prices = model.predict(x_test)
    
    # Odskałowanie przewidywanych cen
    predicted_prices = scaler.inverse_transform(predicted_prices)
    
    # Porównanie przewidywanych cen z rzeczywistymi cenami
    last_real_price = original_data.iloc[-1]
    last_predicted_price = predicted_prices[-1][0]
    
    # Sprawdzenie, czy przewidywana cena wzrasta o więcej niż threshold
    if last_predicted_price >= last_real_price * threshold:
        profitable_companies.append({
            'company': filename.split(".")[0],
            'current_price': last_real_price,
            'predicted_price': last_predicted_price,
            'expected_gain': (last_predicted_price - last_real_price) / last_real_price * 100
        })

# Wyniki
if len(profitable_companies) > 0:
    print("Firmy, które mogą przynieść pewny zysk:")
    for company in profitable_companies:
        print(f"Firma: {company['company']}")
        print(f"Obecna cena: {company['current_price']}")
        print(f"Przewidywana cena: {company['predicted_price']}")
        print(f"Oczekiwany zysk: {company['expected_gain']:.2f}%")
        print("-" * 30)
else:
    print("Nie znaleziono firm spełniających kryterium wzrostu cen.")
