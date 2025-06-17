# WARNING - THIS DOES NOT WORK YET - DO NOT USE
# WARNING - THIS DOES NOT WORK YET - DO NOT USE
# WARNING - THIS DOES NOT WORK YET - DO NOT USE
# WARNING - THIS DOES NOT WORK YET - DO NOT USE
# WARNING - THIS DOES NOT WORK YET - DO NOT USE









## German Parcel Tracker – Multi-Carrier Integration für Home Assistant

Verfolge deine Pakete von DHL, Hermes und DPD direkt in Home Assistant – mit dieser modularen, erweiterbaren Integration.


> **Hinweis:** Diese Integration ist über [HACS](https://hacs.xyz/) installierbar.

> **Voraussetzung:** Home Assistant 2025.12 oder neuer
>
> **Status:** Die DHL-Anbindung nutzt aktuell die Sandbox-Umgebung
> `https://api-sandbox.dhl.com/parcel/de/tracking/v0/shipments`. Für den
> produktiven Einsatz muss der Endpunkt angepasst werden.

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
Lade das ZIP herunter und entpacke den Ordner `custom_components/german-parcel-tracker/` in dein Home Assistant `config`-Verzeichnis.

Pfad-Beispiel:
```
/config/custom_components/german-parcel-tracker/
```

### 2. Panel einrichten (optional)
Wenn du die UI-Oberfläche verwenden möchtest, füge folgendes in `configuration.yaml` ein:

```yaml
panel_custom:
  - name: pakettracker
    sidebar_title: Paketverfolgung
    sidebar_icon: mdi:truck
    url_path: german-parcel-tracker
    module_url: /local/custom_components/german-parcel-tracker/www/panel.html
    embed_iframe: true
    require_admin: false
```

Stelle sicher, dass `panel.html` unter `www` vorhanden ist:
```
/config/www/custom_components/german-parcel-tracker/panel.html
```

### 3. Home Assistant neustarten

### 4. Integration hinzufügen
Einstellungen → Geräte & Dienste → Integration hinzufügen → **German Parcel Tracker** auswählen

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
