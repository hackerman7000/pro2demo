# Problembeschreibung / Ausgangslage 
Mit dieser Seite soll für spezifisch für DBM-Student*innen eine Lösung geboten werden, um einen Überblick über den Fortschritt und die Leistung im Studium zu bekommen.
Da das Studium durch Wahlpflichtmodule zu einem grossen Teil selbst gestaltet werden kann, geht die Übersicht über die erreichten ECTS Punkte schnell verloren. 
Dieses Tool soll helfen, der studierenden Personen aufzuzeigen, wie viele Module in welchen Bereich noch zu absolvieren sind.
Ausserden soll ein Notenrechner integriert werden, welcher den aktuellen Notenschnitt ausrechnen kann.

**Relevante Informationen für den ECTS-Rechner:**
Pflichtmodule: Müssen während dem Studium absolviert werden.
Wahlpflichtmodule: Können von den Studierenden selber ausgewählt werden.
Modulgruppen der Wahlpflichtmodule: "User Experience", "Information Technology", "Digital Innovation" und "Sozial- und Methodenkompetenz"

Folgende Anzahl ECTS Punkte benötigt man:
Insgesamt: 180 ECTS
Minimum pro Modulgruppe: Mind. 8 ECTS für die Modulgruppen "User Experience", "Information Technology" und "Digital Innovation" und mind. 4 ECTS in "Sozial- und Methodenkompetenz"
Major: Für einen Major benötigt man mind. 20 ECTS in den Modulgruppen "User Experience", "Information Technology" und "Digital Innovation". In "Sozial- und Methodenkompetenz" kann man keinen Major machen.


# Funktionalitäten
## Funktionalität 1: ECTS-Rechner
Anhand der ausgewählten Module soll ausgerechnet werden, wie viel ECTS man im Studium gemacht (insgesamt und pro Modulgruppe).

## Funktionalität 2: Übersicht Studium mit Plotly Grafik


# Ablauf
![Diagramm](./img/ablaufdiagram.svg)

# Workflow
## 1. Dateneingabe: Auswahl der besuchten Module
Auf der Startseite des Programms die besuchten Module auswählen.
Danach auf "Weiter" klicken.

## 2. Datenverarbeitung: Speichern der ausgewählten Module in json
(Die Datenverarbeitung erfolgt ohne Handlung des Users.)
Für jedes ausgewählte Modul wird im json der boolean Wert "Absolviert" von false auf true gesetzt.

## 3. Datenausgabe: Berechneter Studiumsfortschritt
Auf der Seite "ECTS" sieht man den berechneten Fortschritt des Studiums. Insgesamt und pro Modulgruppe.
Bei den Modulgruppen wird zudem angezeigt, wie viel ECTS man minimun benötigt oder für den Major.


# Probleme


