import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import csv
import datetime

# === Configuration des couleurs d'impact ===
IMPACT_COLORS = {
    "High": "#FF6B6B",     # Rouge vif
    "Medium": "#FFA500",   # Orange
    "Low": "#87CEEB",      # Bleu clair
    "Holiday": "#A9A9A9",  # Gris
    "": "white"              # Valeur par défaut
}

# === Fonction pour récupérer les données ===
def fetch_calendar_data():
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        if not response.content:
            print("Réponse vide")
            return []
        return response.json()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de charger les données : {e}")
        return []

# === Fonction d'export CSV ===
def export_to_csv(data):
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Heure", "Devise", "Impact", "Événement"])
            for row in data:
                writer.writerow([row['date'], row['time'], row['currency'], row['impact'], row['event']])
        messagebox.showinfo("Exporté", "Les données ont été exportées avec succès.")

# === Fonction principale ===
def start_ui():
    root = tk.Tk()
    root.title("Calendrier Économique")
    root.geometry("1000x600")
    root.configure(bg="#F5F5F5")

    # === Barre de filtres ===
    top_frame = tk.Frame(root, bg="#F5F5F5")
    top_frame.pack(fill="x", padx=10, pady=10)

    country_var = tk.StringVar()
    impact_var = tk.StringVar()

    tk.Label(top_frame, text="Filtrer par devise :", bg="#F5F5F5").pack(side="left", padx=5)
    country_combo = ttk.Combobox(top_frame, textvariable=country_var, width=10)
    country_combo.pack(side="left", padx=5)

    tk.Label(top_frame, text="Filtrer par impact :", bg="#F5F5F5").pack(side="left", padx=5)
    impact_combo = ttk.Combobox(top_frame, textvariable=impact_var, values=["", "High", "Medium", "Low", "Holiday"], width=10)
    impact_combo.pack(side="left", padx=5)

    def apply_filters():
        filtered = [
            e for e in events
            if (not country_var.get() or e['currency'] == country_var.get()) and
               (not impact_var.get() or e['impact'] == impact_var.get())
        ]
        display_data(filtered)

    def refresh_data():
        nonlocal events
        events = fetch_calendar_data()
        update_filters(events)
        display_data(events)

    def update_filters(data):
        currencies = sorted(set(e['currency'] for e in data))
        country_combo['values'] = [""] + currencies

    # === Tableau ===
    columns = ("date", "time", "currency", "impact", "event")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
    tree.pack(fill="both", expand=True, padx=10, pady=5)

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")

    def display_data(data):
        tree.delete(*tree.get_children())
        for e in data:
            tree.insert("", "end", values=(e['date'], e['time'], e['currency'], e['impact'], e['event']), tags=(e['impact'],))
        for impact, color in IMPACT_COLORS.items():
            tree.tag_configure(impact, background=color)

    # === Bas de page ===
    bottom_frame = tk.Frame(root, bg="#F5F5F5")
    bottom_frame.pack(fill="x", padx=10, pady=10)

    tk.Button(bottom_frame, text="Rafraîchir", command=refresh_data, bg="#007BFF", fg="white").pack(side="left", padx=5)
    tk.Button(bottom_frame, text="Appliquer les filtres", command=apply_filters, bg="#28A745", fg="white").pack(side="left", padx=5)
    tk.Button(bottom_frame, text="Exporter", command=lambda: export_to_csv(tree_data()), bg="#6C757D", fg="white").pack(side="right", padx=5)

    def tree_data():
        return [
            {
                'date': tree.item(i)['values'][0],
                'time': tree.item(i)['values'][1],
                'currency': tree.item(i)['values'][2],
                'impact': tree.item(i)['values'][3],
                'event': tree.item(i)['values'][4]
            }
            for i in tree.get_children()
        ]

    # === Lancement initial ===
    events = fetch_calendar_data()
    update_filters(events)
    display_data(events)

    root.mainloop()

if __name__ == "__main__":
    start_ui()
