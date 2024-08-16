import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych prognozowanych cen z pliku CSV
predictions_file = 'prognozowane_ceny.csv'
historical_data_file = 'historyczne_ceny.csv'  # Plik z danymi historycznymi

try:
    predictions_df = pd.read_csv(predictions_file)
except FileNotFoundError:
    raise FileNotFoundError(f"Plik {predictions_file} nie został znaleziony. Upewnij się, że dane prognozowane istnieją.")

try:
    historical_df = pd.read_csv(historical_data_file)
except FileNotFoundError:
    raise FileNotFoundError(f"Plik {historical_data_file} nie został znaleziony. Upewnij się, że dane historyczne istnieją.")

# Sprawdzenie, czy pliki nie są puste
if predictions_df.empty:
    raise ValueError("Plik z prognozami jest pusty.")
if historical_df.empty:
    raise ValueError("Plik z danymi historycznymi jest pusty.")

# Funkcja wyświetlająca listę firm i pozwalająca użytkownikowi na wybór firmy do wyświetlenia wykresu
def display_menu():
    print("\nLista dostępnych firm do wyświetlenia prognozy:\n")
    for idx, row in predictions_df.iterrows():
        print(f"{idx + 1}. {row['Firma']}")
    print("\nWpisz numer firmy, aby wyświetlić wykres lub '0', aby zakończyć.\n")

# Funkcja do wyświetlania wykresu dla wybranej firmy
def plot_prediction(firma):
    # Znajdź rekord prognozy dla wybranej firmy
    selected_row = predictions_df[predictions_df['Firma'] == firma]
    
    if selected_row.empty:
        print(f"Brak danych dla firmy: {firma}")
        return
    
    # Znajdź dane historyczne dla wybranej firmy
    history = historical_df[historical_df['Firma'] == firma]
    
    if history.empty:
        print(f"Brak danych historycznych dla firmy: {firma}")
        return
    
    # Wyciągnięcie danych historycznych
    history_dates = history['Date'].values
    history_prices = history['Close'].values
    
    # Prognozowana cena
    predicted_price = selected_row['Przewidywana Cena'].values[0]
    
    # Dodanie prognozowanej ceny na koniec danych historycznych
    future_dates = list(history_dates) + ['Prognoza']
    future_prices = list(history_prices) + [predicted_price]
    
    # Wyświetlenie wykresu z danymi historycznymi i prognozowaną ceną
    plt.figure(figsize=(10, 5))
    plt.plot(future_dates, future_prices, marker='o', linestyle='-', color='blue', label='Cena (historyczna + prognoza)')
    plt.axvline(x=len(history_dates) - 1, color='red', linestyle='--', label='Początek prognozy')
    plt.title(f"Historia i Prognoza Ceny Akcji - {firma}")
    plt.xlabel('Data')
    plt.ylabel('Cena Akcji')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Poprawienie wyglądu wykresu
    plt.show()

# Główna pętla programu
while True:
    display_menu()
    
    try:
        choice = int(input("Wybierz firmę (numer): "))
    except ValueError:
        print("Nieprawidłowy wybór. Proszę wpisać numer firmy.")
        continue
    
    # Sprawdzenie, czy użytkownik chce zakończyć program
    if choice == 0:
        print("Zakończono program.")
        break
    
    # Sprawdzenie, czy wybór jest poprawny
    if 1 <= choice <= len(predictions_df):
        # Pobranie nazwy firmy na podstawie wyboru użytkownika
        selected_firma = predictions_df.iloc[choice - 1]['Firma']
        plot_prediction(selected_firma)
    else:
        print("Nieprawidłowy wybór. Spróbuj ponownie.")