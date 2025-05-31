import time
import threading
from datetime import datetime
from pynput import mouse, keyboard
from collections import deque

class ActivityMonitor:
    def __init__(self):
        self.is_monitoring = False
        self.idle_threshold = 300  # 5 minut w sekundach
        self.last_activity_time = time.time()
        
        # Statystyki
        self.stats = {
            'active_time': 0,
            'idle_time': 0,
            'mouse_moves': 0,
            'key_presses': 0,
            'start_time': None
        }
        
        # Szczegółowy log aktywności
        self.activity_log = deque(maxlen=10000)  # Przechowuje ostatnie 10000 zdarzeń
        
        # Listenery
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Thread do monitorowania bezczynności
        self.idle_monitor_thread = None
        
        # Mutex dla thread-safe operacji
        self.lock = threading.Lock()
        
    def set_idle_threshold(self, seconds):
        """Ustawia próg bezczynności w sekundach"""
        self.idle_threshold = seconds
        
    def on_mouse_move(self, x, y):
        """Callback dla ruchu myszy"""
        if not self.is_monitoring:
            return
            
        with self.lock:
            self.last_activity_time = time.time()
            self.stats['mouse_moves'] += 1
            
            self.activity_log.append({
                'timestamp': datetime.now(),
                'type': 'Ruch myszy',
                'details': f'Pozycja: ({x}, {y})'
            })
    
    def on_mouse_click(self, x, y, button, pressed):
        """Callback dla kliknięć myszy"""
        if not self.is_monitoring:
            return
            
        if pressed:  # Tylko naciśnięcia, nie puszczenia
            with self.lock:
                self.last_activity_time = time.time()
                
                self.activity_log.append({
                    'timestamp': datetime.now(),
                    'type': 'Kliknięcie myszy',
                    'details': f'Przycisk: {button.name}, Pozycja: ({x}, {y})'
                })
    
    def on_mouse_scroll(self, x, y, dx, dy):
        """Callback dla przewijania myszy"""
        if not self.is_monitoring:
            return
            
        with self.lock:
            self.last_activity_time = time.time()
            
            self.activity_log.append({
                'timestamp': datetime.now(),
                'type': 'Przewijanie myszy',
                'details': f'Kierunek: ({dx}, {dy}), Pozycja: ({x}, {y})'
            })
    
    def on_key_press(self, key):
        """Callback dla naciśnięć klawiszy"""
        if not self.is_monitoring:
            return
            
        with self.lock:
            self.last_activity_time = time.time()
            self.stats['key_presses'] += 1
            
            # Bezpieczne formatowanie nazwy klawisza
            try:
                key_name = key.char if hasattr(key, 'char') and key.char else str(key)
            except AttributeError:
                key_name = str(key)
            
            self.activity_log.append({
                'timestamp': datetime.now(),
                'type': 'Naciśnięcie klawisza',
                'details': f'Klawisz: {key_name}'
            })
    
    def monitor_idle_time(self):
        """Monitoruje czas bezczynności w osobnym wątku"""
        last_check_time = time.time()
        was_idle = False
        idle_start_time = None
        
        while self.is_monitoring:
            current_time = time.time()
            time_since_activity = current_time - self.last_activity_time
            
            with self.lock:
                if time_since_activity >= self.idle_threshold:
                    # Użytkownik jest bezczynny
                    if not was_idle:
                        # Początek okresu bezczynności
                        was_idle = True
                        idle_start_time = current_time - self.idle_threshold
                        
                        self.activity_log.append({
                            'timestamp': datetime.now(),
                            'type': 'Rozpoczęcie bezczynności',
                            'details': f'Próg: {self.idle_threshold} sekund'
                        })
                    
                    # Aktualizacja czasu bezczynności
                    self.stats['idle_time'] += current_time - last_check_time
                else:
                    # Użytkownik jest aktywny
                    if was_idle:
                        # Koniec okresu bezczynności
                        was_idle = False
                        idle_duration = current_time - idle_start_time
                        
                        self.activity_log.append({
                            'timestamp': datetime.now(),
                            'type': 'Koniec bezczynności',
                            'details': f'Czas bezczynności: {idle_duration:.1f} sekund'
                        })
                    
                    # Aktualizacja czasu aktywności
                    self.stats['active_time'] += current_time - last_check_time
            
            last_check_time = current_time
            time.sleep(1)  # Sprawdzaj co sekundę
    
    def start_monitoring(self):
        """Rozpoczyna monitorowanie aktywności"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        self.last_activity_time = time.time()
        
        # Reset statystyk
        with self.lock:
            self.stats = {
                'active_time': 0,
                'idle_time': 0,
                'mouse_moves': 0,
                'key_presses': 0,
                'start_time': datetime.now()
            }
            self.activity_log.clear()
            
            self.activity_log.append({
                'timestamp': datetime.now(),
                'type': 'Start monitorowania',
                'details': 'Rozpoczęto śledzenie aktywności'
            })
        
        # Uruchomienie listenerów
        try:
            self.mouse_listener = mouse.Listener(
                on_move=self.on_mouse_move,
                on_click=self.on_mouse_click,
                on_scroll=self.on_mouse_scroll
            )
            self.mouse_listener.start()
            
            self.keyboard_listener = keyboard.Listener(
                on_press=self.on_key_press
            )
            self.keyboard_listener.start()
            
            # Uruchomienie monitora bezczynności
            self.idle_monitor_thread = threading.Thread(target=self.monitor_idle_time)
            self.idle_monitor_thread.daemon = True
            self.idle_monitor_thread.start()
            
        except Exception as e:
            self.is_monitoring = False
            raise Exception(f"Nie udało się uruchomić monitorowania: {str(e)}")
    
    def stop_monitoring(self):
        """Zatrzymuje monitorowanie aktywności"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        
        # Zatrzymanie listenerów
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
            
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        
        # Dodanie wpisu o zatrzymaniu
        with self.lock:
            self.activity_log.append({
                'timestamp': datetime.now(),
                'type': 'Stop monitorowania',
                'details': 'Zatrzymano śledzenie aktywności'
            })
    
    def get_stats(self):
        """Zwraca aktualne statystyki"""
        with self.lock:
            return self.stats.copy()
    
    def get_detailed_log(self):
        """Zwraca szczegółowy log aktywności"""
        with self.lock:
            return list(self.activity_log)
    
    def is_active(self):
        """Sprawdza czy monitoring jest aktywny"""
        return self.is_monitoring
    
    def get_current_status(self):
        """Zwraca aktualny status aktywności"""
        if not self.is_monitoring:
            return "Monitorowanie zatrzymane"
        
        time_since_activity = time.time() - self.last_activity_time
        
        if time_since_activity >= self.idle_threshold:
            return f"Bezczynny od {time_since_activity:.0f} sekund"
        else:
            return "Aktywny"