# Eyetracking mit mehreren Kameras in Smart

Masterarbeit im Fach Medieninformatik am Institut für Information und Medien, Sprache und Kultur (I:IMSK)

Vorgelegt von: Markus Guder
Laufendes Semester: SS 2019
Abgegeben am: 30.9.2019

# Repository Struktur

* /0_client: Raspberry Pi Client für Eyetracking Einheit
* /1_python_server: Server zur Annahme und Verarbeitung der EyeTracking Daten
* /2_start_scripts: Start Scripts für Eyetracking Einheiten
* /3_download_scripts: Backups Scripts für Raspberry Pi Daten
* /4_web-client: Webanwendung
* /5_experiment: Experiment Daten + Auswertung
* /4_paper: Wissenschaftliche Arbeit + Quellen

* /[OpenFace_Fork_Guder](https://github.com/marc101101/OpenFace)
: Erweiterung von OpenFace zum abgreifen von Echtzeit Daten

# Architektur
![enter image description here](https://i.imgur.com/9YMWPEF.jpg)

## Eyetracking Einheit
Die primäre Funktion der Eyetracking Einheit ist die Erfassung der Blicke des Nutzers mithilfe der OpenFace Software und die Weiterleitung der Daten an die zentrale Server-Einheit.

### Installation

Das Projekt basiert auf **Python 3.6**.

``
pip3 install requirements.txt
``


### Start Script - Aufbau

``
../../OpenFace/build/bin/FeatureExtraction -device 0 | python3  ../../client/client.py {{SERVER_IP}} {{client_ID}}
``


### Start Script - Beispiel

``
../../OpenFace/build/bin/FeatureExtraction -device 0 | python3  ../../client/client.py 192.168.0.191 cam_3
``

Die Start Scripte befinden sich im Ordner /2_start_scripts. Diese zeigen exemplarisch auf wie die Webclients zu starten sind.

**Wichtig:** Die Servereinheit muss vor den Client Einheiten gestartet werden.

## Server
Die Hauptaufgabe der zentralen Servereinheit ist die Annahme der von den Clients generierten Daten, deren Persistierung, die Client abhänige Transformation der Blickdaten und deren Schnittpunkt Berechnung mit den Küchenelementen. Anschließend müssen die errechneten Daten wiederum einem potentiellen Assistenzsystem bereitgestellt werden. In dieser Arbeit wird hierfür eine Visualisierungskomponente genutzt, die im Punkt 3.3.3 beschrieben wird.

### Installation

Das Projekt basiert auf **Python 3.6**.

``
pip3 install requirements.txt
``

### Start Script 

``
python3 server.py
``

Wenn der Server gestartet ist, dann wird er auf http://0.0.0.0:5000/ bzw. ws://0.0.0.0:5000/ lokal erreichbar sein.

## Web Anwendung
Wie bereits angesprochen ist die Webanwendung nur eine Zusatzkomponente, ohne die das System trotzdem nutzbar wäre. Die öffentlich im Netzwerk verfügbare Schnittstelle der Servereinheit, auf der fortlaufend neue Daten veröffentlicht werden, könnte beispielsweise auch von einem Assistenzsystem als Eingabequelle für Blickdaten genutzt werden. Nichtsdestotrotz erfüllt sie im Kern drei wichtige Aufgaben. Die Darstellung der Daten in Echtzeit, das einfache Konfigurieren der Clients und die Annotierung von Echtzeitdaten für die spätere Evaluierung des Systems.

Es findet sich eine detailierte Ansicht über alle Scripte für die Webanwendung [hier](https://github.com/marc101101/masterarbeit_eye_tracking/tree/master/4_web-client).

### Installation

``
npm install
``

### Start der Webanwendung

``
npm start
``

Wenn die Webanwendung gestartet ist, dann ist diese unter http://localhost:4200 lokal erreichbar.


### Build der Webanwendung

#### Default Build
``
npm run build
``

#### Productive Build
``
ng build --prod  
``

Wenn die Webanwendung gebuildet wurde, dann liegen die gebundelten Dateien unter /dist.


