# Calendrier Économique

Une application desktop en Python utilisant Tkinter pour afficher un calendrier économique avec les événements de la semaine en cours.

---

## Fonctionnalités

- **Affichage des événements économiques** avec date, heure, devise, impact, et description.
- **Filtres dynamiques** par devise et par impact économique (High, Medium, Low, Holiday).
- **Export des données filtrées** au format CSV.
- **Design simple et épuré**, facile à utiliser.

---

## Sources des données

Les données sont récupérées en temps réel depuis la source publique JSON :  
https://nfs.faireconomy.media/ff_calendar_thisweek.json

---

## Installation et utilisation

1. Cloner ce dépôt  
```bash
git clone https://github.com/Rayanne92/economic-calendar.git
cd economic-calendar
```

2. Installer les dépendances

```bash
pip install requests
```

3. Lancer l’application

```bash
python economic_calendar_ui.py
```