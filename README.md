# DHL Tracker – Multi-Carrier Integration für Home Assistant

Verfolge deine Pakete von DHL, Hermes und DPD direkt in Home Assistant – mit dieser modularen, erweiterbaren Integration.

> **Voraussetzung:** Home Assistant 2025 oder neuer

---

## ✨ Unterstützte Dienste
- ✅ DHL (offizielle API)
- 🔶 Hermes (Platzhalter)
- 🔶 DPD (Platzhalter)
- 🔜 Erweiterbar: Amazon, UPS, GLS …

---

## 📦 Funktionen
- Sensor je Trackingnummer
- Übersicht im Lovelace-Panel (HTML-Frontend)
- Erweiterbares Carrier-Modulkonzept
- Mehrere Nummern gleichzeitig trackbar
- Optionen konfigurierbar über GUI (kein YAML nötig)

---

## 🛠 Installation

### 1. Dateien kopieren
Lade das ZIP herunter und entpacke den Ordner `custom_components/dhl_tracker/` in dein Home Assistant `config`-Verzeichnis.

Pfad-Beispiel:
```
/config/custom_components/dhl_tracker/
```

### 2. Panel einrichten (optional)
Wenn du die UI-Oberfläche verwenden möchtest, füge folgendes in `configuration.yaml` ein:

```yaml
panel_custom:
  - name: pakettracker
    sidebar_title: Paketverfolgung
    sidebar_icon: mdi:truck
    url_path: dhl-tracker
    module_url: /local/custom_components/dhl_tracker/www/panel.html
    embed_iframe: true
    require_admin: false
```

Stelle sicher, dass `panel.html` unter `www` vorhanden ist:
```
/config/www/custom_components/dhl_tracker/panel.html
```

### 3. Home Assistant neustarten

### 4. Integration hinzufügen
Einstellungen → Geräte & Dienste → Integration hinzufügen → **DHL Tracker** auswählen

---

## ➕ Neue Sendung hinzufügen
- Träger (z. B. DHL, Hermes, DPD) auswählen
- Sendungsnummer eingeben
- Sensor erscheint automatisch

---

## 🔐 Datenschutz
- Keine persönlichen Daten werden gespeichert oder weitergegeben.
- Trackinginformationen werden nur zur Anzeige verarbeitet.

---

## 🔧 Hinweise
- Hermes & DPD liefern derzeit **symbolische Daten** (kein Live-Tracking).
- Das System ist vorbereitet für echte API-Implementierungen.

---

## 🧩 Erweiterungsideen
- Benachrichtigungen
- Historie & Timeline
- Sprachassistenz-Integration (z. B. Alexa)
- Anbindung an Dienste wie AfterShip

---

**Mitgedacht für die Praxis – für Entwickler erweiterbar.**
