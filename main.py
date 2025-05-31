import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import csv
import os
from datetime import datetime, timedelta
from activity_monitor import ActivityMonitor


class ActivityMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor Aktywności Użytkownika")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        # Inicjalizacja monitora aktywności
        self.activity_monitor = ActivityMonitor()
        self.monitoring_thread = None
        self.is_monitoring = False

        # Utworzenie interfejsu
        self.create_interface()

        # Protokół zamykania aplikacji
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_interface(self):
        # Główny frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Konfiguracja grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Tytuł
        title_label = ttk.Label(main_frame, text="Monitor Aktywności Użytkownika",
                                font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Status monitorowania
        ttk.Label(main_frame, text="Status:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.status_label = ttk.Label(main_frame, text="Zatrzymany",
                                      foreground="red", font=('Arial', 10, 'bold'))
        self.status_label.grid(row=1, column=1, sticky=tk.W, pady=5)

        # Przyciski kontroli
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=2, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(control_frame, text="Rozpocznij monitorowanie",
                                       command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(control_frame, text="Zatrzymaj monitorowanie",
                                      command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Ustawienia
        settings_frame = ttk.LabelFrame(main_frame, text="Ustawienia", padding="10")
        settings_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        settings_frame.columnconfigure(1, weight=1)

        ttk.Label(settings_frame, text="Czas bezczynności (minuty):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.idle_time_var = tk.StringVar(value="5")
        idle_spinbox = ttk.Spinbox(settings_frame, from_=1, to=60, textvariable=self.idle_time_var, width=10)
        idle_spinbox.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(settings_frame, text="Katalog eksportu:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.export_path_var = tk.StringVar(value=os.getcwd())
        export_entry = ttk.Entry(settings_frame, textvariable=self.export_path_var, width=40)
        export_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))

        browse_button = ttk.Button(settings_frame, text="Przeglądaj",
                                   command=self.browse_directory)
        browse_button.grid(row=1, column=2, pady=5)

        # Statystyki
        stats_frame = ttk.LabelFrame(main_frame, text="Statystyki bieżącej sesji", padding="10")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        stats_frame.columnconfigure(1, weight=1)

        ttk.Label(stats_frame, text="Czas aktywności:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.active_time_label = ttk.Label(stats_frame, text="00:00:00")
        self.active_time_label.grid(row=0, column=1, sticky=tk.W, pady=2)

        ttk.Label(stats_frame, text="Czas bezczynności:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.idle_time_label = ttk.Label(stats_frame, text="00:00:00")
        self.idle_time_label.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(stats_frame, text="Ruchy myszy:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.mouse_moves_label = ttk.Label(stats_frame, text="0")
        self.mouse_moves_label.grid(row=2, column=1, sticky=tk.W, pady=2)

        ttk.Label(stats_frame, text="Naciśnięcia klawiszy:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.key_presses_label = ttk.Label(stats_frame, text="0")
        self.key_presses_label.grid(row=3, column=1, sticky=tk.W, pady=2)

        # Przyciski eksportu
        export_frame = ttk.Frame(main_frame)
        export_frame.grid(row=5, column=0, columnspan=3, pady=10)

        ttk.Button(export_frame, text="Eksportuj do CSV",
                   command=self.export_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Eksportuj do TXT",
                   command=self.export_txt).pack(side=tk.LEFT, padx=5)

        # Aktualizacja statystyk
        self.update_stats()

    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.export_path_var.set(directory)

    def start_monitoring(self):
        try:
            idle_minutes = int(self.idle_time_var.get())
            self.activity_monitor.set_idle_threshold(idle_minutes * 60)

            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self.activity_monitor.start_monitoring)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Aktywny", foreground="green")

        except ValueError:
            messagebox.showerror("Błąd", "Podaj prawidłową wartość czasu bezczynności")

    def stop_monitoring(self):
        self.is_monitoring = False
        self.activity_monitor.stop_monitoring()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Zatrzymany", foreground="red")

    def update_stats(self):
        if hasattr(self.activity_monitor, 'stats'):
            stats = self.activity_monitor.get_stats()

            # Formatowanie czasu
            active_time = str(timedelta(seconds=int(stats['active_time'])))
            idle_time = str(timedelta(seconds=int(stats['idle_time'])))

            self.active_time_label.config(text=active_time)
            self.idle_time_label.config(text=idle_time)
            self.mouse_moves_label.config(text=str(stats['mouse_moves']))
            self.key_presses_label.config(text=str(stats['key_presses']))

        # Zaplanuj kolejną aktualizację
        self.root.after(1000, self.update_stats)

    def export_csv(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"activity_report_{timestamp}.csv"
            filepath = os.path.join(self.export_path_var.get(), filename)

            data = self.activity_monitor.get_detailed_log()

            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Czas', 'Typ aktywności', 'Szczegóły'])

                for entry in data:
                    writer.writerow([
                        entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
                        entry['type'],
                        entry['details']
                    ])

            messagebox.showinfo("Sukces", f"Raport został wyeksportowany do:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować do CSV:\n{str(e)}")

    def export_txt(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"activity_report_{timestamp}.txt"
            filepath = os.path.join(self.export_path_var.get(), filename)

            stats = self.activity_monitor.get_stats()
            data = self.activity_monitor.get_detailed_log()

            with open(filepath, 'w', encoding='utf-8') as txtfile:
                txtfile.write("RAPORT AKTYWNOŚCI UŻYTKOWNIKA\n")
                txtfile.write("=" * 40 + "\n\n")
                txtfile.write(f"Data generowania: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                txtfile.write("PODSUMOWANIE:\n")
                txtfile.write("-" * 20 + "\n")
                txtfile.write(f"Czas aktywności: {timedelta(seconds=int(stats['active_time']))}\n")
                txtfile.write(f"Czas bezczynności: {timedelta(seconds=int(stats['idle_time']))}\n")
                txtfile.write(f"Ruchy myszy: {stats['mouse_moves']}\n")
                txtfile.write(f"Naciśnięcia klawiszy: {stats['key_presses']}\n\n")

                txtfile.write("SZCZEGÓŁOWY LOG:\n")
                txtfile.write("-" * 20 + "\n")

                for entry in data:
                    txtfile.write(f"{entry['timestamp'].strftime('%H:%M:%S')} - {entry['type']}: {entry['details']}\n")

            messagebox.showinfo("Sukces", f"Raport został wyeksportowany do:\n{filepath}")

        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wyeksportować do TXT:\n{str(e)}")

    def on_closing(self):
        if self.is_monitoring:
            self.stop_monitoring()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ActivityMonitorApp(root)
    root.mainloop()