# Monitor Aktywności Użytkownika

Prosta aplikacja desktopowa w Pythonie do monitorowania aktywności użytkownika na komputerze z systemem Windows/Linux.

## Funkcjonalności

- **Monitorowanie aktywności w czasie rzeczywistym**
  - Śledzenie ruchów myszy i kliknięć
  - Rejestrowanie naciśnięć klawiszy
  - Wykrywanie przewijania myszy

- **Zarządzanie czasem bezczynności**
  - Konfigurowalny próg bezczynności (1-60 minut)
  - Automatyczne wykrywanie okresów bezczynności
  - Logowanie rozpoczęcia i zakończenia bezczynności

- **Statystyki i raporty**
  - Wyświetlanie statystyk bieżącej sesji
  - Eksport danych do plików CSV i TXT
  - Szczegółowy log wszystkich aktywności

- **Przyjazny interfejs użytkownika**
  - Intuicyjny interfejs graficzny (tkinter)
  - Kontrola monitorowania (start/stop)
  - Konfiguracja ustawień

## Wymagania systemowe

- Python 3.12 lub nowszy
- System operacyjny: Windows, Linux, lub macOS
- Uprawnienia administratora (mogą być wymagane dla monitorowania klawiatury i myszy)

## Instalacja

1. **Pobierz pliki projektu**
   ```bash
   git clone <url_repozytorium>
   cd activity-monitor
   ```

2. **Zainstaluj wymagane biblioteki**
   ```bash
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację**
   ```bash
   python main.py
   ```

## Instrukcja użycia

### Uruchamianie monitorowania

1. Uruchom aplikację poleceniem `python main.py`
2. W sekcji "Ustawienia" skonfiguruj:
   - **Czas bezczynności**: określ po ilu minutach brak aktywności zostanie uznany za bezczynność
   - **Katalog eksportu**: wybierz folder, gdzie będą zapisywane raporty
3. Kliknij przycisk **"Rozpocznij monitorowanie"**
4. Aplikacja będzie teraz śledzić Twoją aktywność w tle

### Przeglądanie statystyk

W sekcji "Statystyki bieżącej sesji" możesz na bieżąco obserwować:
- Łączny czas aktywności
- Łączny czas bezczynności
- Liczbę ruchów myszy
- Liczbę naciśnięć klawiszy

### Eksport raportów

Aplikacja oferuje dwa formaty eksportu:

#### CSV (Excel-compatible)
- Kliknij **"Eksportuj do CSV"**
- Plik zawiera szczegółowy log z kolumnami: Czas, Typ aktywności, Szczegóły
- Można otworzyć w Excel lub LibreOffice Calc

#### TXT (czytelny raport)
- Kliknij **"Eksportuj do TXT"**
- Plik zawiera podsumowanie statystyk oraz szczegółowy chronologiczny log
- Format czytelny dla człowieka

### Zatrzymywanie monitorowania

1. Kliknij przycisk **"Zatrzymaj monitorowanie"**
2. Możesz wyeksportować dane z sesji przed zamknięciem aplikacji
3. Zamknij aplikację przyciskiem X lub Alt+F4

## Struktura plików

```
activity-monitor/
│
├── main.py                 # Główna aplikacja z interfejsem GUI
├── activity_monitor.py     # Moduł monitorowania aktywności
├── requirements.txt        # Lista wymaganych bibliotek
└── README.md              # Ta instrukcja
```

## Szczegóły techniczne

### Monitorowane zdarzenia

- **Ruch myszy**: pozycja kursora
- **Kliknięcia myszy**: przycisk i pozycja
- **Przewijanie myszy**: kierunek i pozycja
- **Naciśnięcia klawiszy**: wszystkie klawisze (bez zapisywania treści)

### Bezpieczeństwo i prywatność

- Aplikacja **NIE zapisuje** treści wpisywanych tekstów
- Rejestrowane są tylko statystyki naciśnięć klawiszy
- Wszystkie dane pozostają lokalnie na Twoim komputerze
- Brak połączenia z internetem lub wysyłania danych

### Wydajność

- Minimalne zużycie zasobów systemowych
- Monitoring w tle bez wpływu na pracę
- Automatyczne ograniczenie rozmiaru logów (10000 ostatnich zdarzeń)

## Rozwiązywanie problemów

### Problem z uprawnieniami
Jeśli aplikacja nie może monitorować aktywności:
- **Windows**: Uruchom jako administrator
- **Linux**: Użyj `sudo python main.py` lub dodaj użytkownika do grupy `input`
- **macOS**: Zezwól aplikacji na dostęp w Ustawieniach → Prywatność i bezpieczeństwo

### Błędy instalacji
Jeśli masz problem z instalacją `pynput`:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk python3-dev

# macOS
xcode-select --install

# Windows
# Upewnij się, że masz zainstalowany Visual Studio Build Tools
```

### Aplikacja się zawiesza
- Upewnij się, że używasz Python 3.12+
- Sprawdź czy wszystkie zależności są zainstalowane
- Uruchom aplikację z terminala, aby zobaczyć komunikaty błędów

## Rozwój i modyfikacje

Aplikacja została napisana w sposób modularny:
- `main.py` - interfejs użytkownika (tkinter)
- `activity_monitor.py` - logika monitorowania (pynput)

Możesz łatwo rozszerzyć funkcjonalność poprzez:
- Dodanie nowych typów zdarzeń do monitorowania
- Modyfikację formatu eksportu
- Rozszerzenie interfejsu użytkownika

## Licencja

Ten projekt jest udostępniony na licencji MIT. Możesz go swobodnie używać, modyfikować i dystrybuować.

## Wsparcie

W przypadku problemów:
1. Sprawdź tę instrukcję
2. Upewnij się, że spełniasz wymagania systemowe
3. Sprawdź czy aplikacja ma odpowiednie uprawnienia
4. Uruchom z terminala aby zobaczyć komunikaty błędów