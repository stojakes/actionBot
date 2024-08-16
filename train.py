import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM

# Funkcja do wczytania i przetworzenia danych z jednego pliku CSV
def load_and_process_data(filepath):
    df = pd.read_csv(filepath)
    
    # Sprawdź, czy plik zawiera kolumnę 'Close' i czy ma dane
    if 'Close' not in df.columns or df['Close'].isna().all():
        print(f"Plik {filepath} jest pusty lub nie zawiera kolumny 'Close'. Pomijanie pliku.")
        return None
    
    data = df['Close'].dropna().values  # Usunięcie brakujących wartości
    if len(data) == 0:
        print(f"Plik {filepath} nie zawiera wystarczających danych do przetwarzania. Pomijanie pliku.")
        return None
    
    data = data.reshape(-1, 1)
    return data

# Funkcja do stworzenia zbioru danych do trenowania modelu
def create_dataset(dataset, look_back=60):
    x, y = [], []
    for i in range(len(dataset) - look_back):
        x.append(dataset[i:(i + look_back), 0])
        y.append(dataset[i + look_back, 0])
    return np.array(x), np.array(y)

# Inicjalizacja modelu LSTM
def build_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Funkcja do zapisywania danych treningowych do CSV
def save_training_data(train_data, filename, folder="dane_treningowe"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, filename)
    np.savetxt(filepath, train_data, delimiter=",")

# Ścieżka do folderu z danymi
data_folder = 'dane_akcje'

# Sprawdzenie, czy folder istnieje
if not os.path.exists(data_folder):
    raise ValueError(f"Folder '{data_folder}' nie istnieje!")

# Lista wszystkich plików CSV w folderze
files = [f for f in os.listdir(data_folder) if f.endswith('.csv')]

# Sprawdzenie, czy mamy pliki CSV do przetworzenia
if len(files) == 0:
    raise ValueError("Brak dostępnych plików CSV w folderze!")

# Parametry modelu
look_back = 60
batch_size = 1
epochs = 1

# Inicjalizacja zmiennej modelu
model = None

# Przetwarzanie każdego pliku CSV osobno
for file_name in files:
    filepath = os.path.join(data_folder, file_name)
    
    # Wczytaj i przetwórz dane
    data = load_and_process_data(filepath)
    
    # Sprawdzenie, czy dane zostały poprawnie wczytane
    if data is None:
        continue  # Pomijanie tego pliku, jeśli dane są puste lub niepoprawne
    
    # Ograniczenie danych do maksymalnie 5000 próbek
    max_samples = 5000
    if len(data) > max_samples:
        data = data[:max_samples]

    # Normalizuj dane do zakresu [0, 1]
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Podział danych na dane treningowe i testowe (80/20)
    training_data_len = int(np.ceil(len(scaled_data) * .8))
    train_data = scaled_data[0:training_data_len]
    test_data = scaled_data[training_data_len:]
    
    # Zapis danych treningowych do pliku CSV
    save_training_data(train_data, f"train_{file_name}")
    
    # Stworzenie zestawów treningowych i testowych
    x_train, y_train = create_dataset(train_data, look_back)
    x_test, y_test = create_dataset(test_data, look_back)
    
    # Sprawdzenie, czy mamy wystarczającą ilość danych do trenowania
    if len(x_train) == 0 or len(x_test) == 0:
        print(f"Plik {file_name} nie zawiera wystarczającej ilości danych po podziale. Pomijanie pliku.")
        continue
    
    # Przekształcenie danych na odpowiedni format dla LSTM
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    # Budowa lub załadowanie modelu LSTM
    if model is None:
        model = build_model((x_train.shape[1], 1))
    
    # Trenowanie modelu na danych z pliku
    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1)
    
    # Zapis modelu do pliku po każdym treningu
    model.save('model_lstm.keras')
    
    # Przewidywanie danych testowych
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    
    # Wizualizacja wyników dla aktualnego pliku
    train = pd.DataFrame(scaled_data[:training_data_len], columns=['Close'])
    valid = pd.DataFrame(scaled_data[training_data_len:], columns=['Close'])
    
    # Przycinanie valid do długości predykcji
    valid = valid[-len(predictions):]
    valid['Predictions'] = predictions
    
    # Wyświetlenie wykresu
    plt.figure(figsize=(16, 8))
    plt.title(f'Model dla {file_name}')
    plt.xlabel('Data', fontsize=18)
    plt.ylabel('Cena Zamknięcia PLN', fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Treningowe', 'Prawdziwe', 'Prognozy'], loc='lower right')
    #plt.show()