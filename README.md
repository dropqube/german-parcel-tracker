# DHL Tracker – Multi-Carrier Integration für Home Assistant

Verfolge deine Pakete von DHL, Hermes und DPD direkt in Home Assistant – mit dieser modularen, erweiterbaren Integration.


> **Hinweis:** Diese Integration ist über [HACS](https://hacs.xyz/) installierbar.

> **Voraussetzung:** Home Assistant 2025.12 oder neuer

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

### Installation über HACS
1. Sorge dafür, dass die **aktuellste HACS-Version** installiert ist. Anleitung unter [hacs.xyz](https://hacs.xyz/).
2. Füge dieses Repository in HACS als **Benutzerdefiniertes Repository** (Typ *Integration*) hinzu.
3. Suche nach "German Parcel Tracker" und installiere das Paket.
4. Starte Home Assistant neu.

### Manuelle Installation

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
