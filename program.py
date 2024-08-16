import tkinter as tk
import subprocess
import pygetwindow as gw
import time
from datetime import datetime, timedelta
import threading
import schedule

# Globalne zmienne
next_run_time = None

# Funkcja do uruchamiania cmd.exe i ustawiania jego pozycji
def run_terminal_and_position(script_name, x, y):
    # Uruchom cmd.exe w tle
    subprocess.Popen(['start', 'cmd', '/k', f'python {script_name}'], shell=True)

    # Poczekaj, aż okno cmd.exe się pojawi
    time.sleep(1)

    # Znajdź okno cmd.exe
    windows = gw.getWindowsWithTitle('Command Prompt')
    if not windows:
        raise RuntimeError("Nie udało się znaleźć okna cmd.exe.")

    # Zakładamy, że cmd.exe jest jedynym oknem z tym tytułem
    cmd_window = windows[0]

    # Ustaw położenie okna
    cmd_window.moveTo(x, y)

# Funkcja do uruchamiania skryptów
def run_script(script_name):
    # Pobierz położenie okna Tkinter
    x = root.winfo_rootx() + terminal_frame.winfo_x()
    y = root.winfo_rooty() + terminal_frame.winfo_y()

    # Uruchom terminal i ustaw położenie
    run_terminal_and_position(script_name, x, y)

# Funkcja do codziennego uruchamiania skryptów
def scheduled_tasks():
    run_script("csv_generator.py")
    # Poczekaj, aż csv_generator.py zakończy działanie przed uruchomieniem następnego skryptu
    time.sleep(10)  # Możesz dostosować ten czas w zależności od czasu trwania skryptu
    run_script("train.py")

# Funkcja do aktualizacji timera
def update_timer():
    global next_run_time
    if next_run_time:
        now = datetime.now()
        remaining_time = next_run_time - now
        if remaining_time.total_seconds() <= 0:
            remaining_time_label.config(text="Czas do następnego uruchomienia: 00:00:00")
        else:
            hours, remainder = divmod(remaining_time.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            remaining_time_label.config(text=f"Czas do następnego uruchomienia: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")
    root.after(1000, update_timer)  # Aktualizuj co 1 sekundę

# Funkcja uruchamiająca harmonogram
def run_scheduler():
    global next_run_time
    while True:
        now = datetime.now()
        next_run_time = now.replace(hour=8, minute=30, second=0, microsecond=0)
        if now > next_run_time:
            next_run_time += timedelta(days=1)
        schedule.run_pending()
        update_timer()
        time.sleep(1)

# Tworzenie głównego okna Tkinter
root = tk.Tk()
root.title("Python Shell GUI")
root.geometry("800x500")

# Zmiana koloru tła formy
root.configure(bg='black')

# Nagłówek
label = tk.Label(root, text="Wybierz skrypt do uruchomienia:", font=("Arial", 14), fg='white', bg='black')
label.pack(pady=10)

# Przycisk do uruchamiania csv_generator.py
btn_csv_generator = tk.Button(root, text="Uruchom csv_generator.py", command=lambda: run_script("csv_generator.py"), width=30, bg='gray', fg='white')
btn_csv_generator.pack(pady=5)

# Przycisk do uruchamiania train.py
btn_train = tk.Button(root, text="Uruchom train.py", command=lambda: run_script("train.py"), width=30, bg='gray', fg='white')
btn_train.pack(pady=5)

# Przycisk do uruchamiania normalizer.py
btn_normalizer = tk.Button(root, text="Uruchom normalizer.py", command=lambda: run_script("normalizer.py"), width=30, bg='gray', fg='white')
btn_normalizer.pack(pady=5)

# Przycisk do uruchamiania viewer.py
btn_viewer = tk.Button(root, text="Uruchom viewer.py", command=lambda: run_script("viewer.py"), width=30, bg='gray', fg='white')
btn_viewer.pack(pady=5)

# Ramka do wyświetlania informacji (symulacja terminala)
terminal_frame = tk.Frame(root, width=80, height=20, bg='black')
terminal_frame.pack(pady=10)

# Timer
remaining_time_label = tk.Label(root, text="", font=("Arial", 12), fg='white', bg='black')
remaining_time_label.pack(pady=10)

# Harmonogram uruchamiania skryptów codziennie o 8:30
schedule.every().monday.at("08:30").do(scheduled_tasks)
schedule.every().tuesday.at("08:30").do(scheduled_tasks)
schedule.every().wednesday.at("08:30").do(scheduled_tasks)
schedule.every().thursday.at("08:30").do(scheduled_tasks)
schedule.every().friday.at("08:30").do(scheduled_tasks)

# Uruchomienie pętli Tkinter i harmonogramu
def start_gui_and_scheduler():
    # Uruchom harmonogram w osobnym wątku
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Uruchom Tkinter GUI
    root.mainloop()

start_gui_and_scheduler()