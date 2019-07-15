# Messwertstatistik

__11.06.2018, Sebastian Schmidt (sebastian.seb.schmidt@fau.de)__

__[github.com/schmidtseb/RaspberryPiUebung]()__

## Vergleich der Speicherverfahren

Verglichen wird die Geschwindigkeit der Messwerterfassung für zwei verschiedene Arten der Speicherung:

- Öffnen einer Datei und direktes Wegschreiben von erfassten Daten - Zeile für Zeile
- Speichern der Daten im Arbeitsspeicher des Systems. Erst bei Beendigung der Messung werden diese auf die SD-Karte gespeichert.

Messungen mit dem Raspberry Pi Zero W liefern hierbei die folgenden Ergebnisse

| Messung #  | Messfrequenz direkt (Hz) | Messfrequenz über RAM (Hz) |
| ---------- | ------------------------ | -------------------------- |
| 1          | 1308.6                   | 1821.2                     |
| 2          | 1415.1                   | 1742.4                     |
| 3          | 1398.4                   | 1648.2                     |
| Mittelwert | 1374 +/- 27              | 1740 +/-40                 |

## Maximale Anzahl von Messwerten

In der Annahme, dass die Speicherkapazität der verwendeten Speicherkarte groß genug ist, wird die maximale Anzahl an Messwerten durch die Größe des Arbeitsspeichers des Systems begrenzt. Um also herauszufinden, wie viel RAM für eine gewisse Anzahl an Messwerten benötigt wird, muss der Speicherbedarf bei Ausführen eines Programms beobachtet werden.

Dies soll nun mittels des Programms `ps` erfolgen. Dazu wird zuerst eine Funktion im `bash`-Terminal definiert, die bei jedem Programmaufruf gestartet wird:

```python
logpid() { while sleep 1; do  ps -p $1 -o pcpu= -o pmem= ; done; }
```

Die Funktion wird in einer Endlosschleife ausgeführt und gibt im Sekundentakt den aktuellen Wert der verwendeten Ressourcen - CPU und RAM - aus. 

Wird ein Programm im Terminal ausgeführt, so gibt dieses seine eigene PID (*P*rocess *ID*) zurück, wobei über `$!` auf sie zugegriffen werden kann. Diese soll nun der Funktion `logpid()` übergeben werden. Dies geschieht über:

```python
python <Programmname> & logpid $!
```

Über den Operator `>>` kann die Ausgabe zusätzlich in eine Datei umgeleitet werden, sodass letztendlich Folgendes ausgeführt werden kann:

```python
python <Programmname> & logpid $! >> RAMusage.dat
```

Ein direkter Blick in die Datei `RAMusage.dat` zeigt sofort den maximalen Arbeitsspeicherbedarf des Programms. Dies kann nun für mehrere Messzeiten wiederholt werden, sodass am Ende eine Liste von Wertepaaren - jeweils bestehend aus Anzahl der Messwerte und Arbeitsspeicherbedarf - erhält. 

Trage diese Daten in eine Datei ein und plotte sie. Gibt es eine Funktion, die eine Regression und damit eine Extrapolation erlaubt? Bei Bekanntheit des maximalen RAMs des Systems kann man dadurch direkt auf die maximale Anzahl der Messwerte schließen.

Eine Messung mit dem Raspberry Pi Zero W ergab folgende Werte:

| Anzahl Messwerte | RAM (%) | Messfrequenz (Hz) |
| ---------------- | ------- | ----------------- |
| 1416             | 3.5     | 1416              |
| 4202             | 3.6     | 1400.6            |
| 6024             | 3.7     | 1204.8            |
| 15222            | 3.9     | 1522.2            |
| 30946            | 4.2     | 1547.3            |
| 39200            | 5.5     | 1306.6            |
| 78518            | 5.5     | 1308.6            |
| 176908           | 7.0     | 1474.2            |

<div style="page-break-after: always;"></div>

## Finden von Maxima

Um die Maxima in einem Frequenzspektrum zu finden, müssen dessen Daten zuerst geladen werden. Dies kann z.B. über die Funktion

```python
f, A, Ar, Ai = np.genfromtxt('<file name>').T
```

geschehen. Das Spektrum kann einen Peak bei einer Frequenz von 0 Hz enthalten. Da wir an diesem nicht interessiert sind, verwerfen wir ihn über:

```python
A = A[f > 0]
f = f[f > 0]
```

Beachte hierbei die Reihenfolge der Kommandos. Sobald die zweite Zeile ausgeführt wird, verändert `f` seine Länge. Beim Ausführen der ersten Zeile, müssen `A` und `f` jedoch die selbe Länge besitzen. Andernfalls gibt das Programm einen Fehler aus. Eine einfache Lösung - wie hier bereits angewandt - ist es die Zeilen in die entsprechende Reihenfolge zu setzen.

Um später sicherzustellen, dass sich ein gefundener Peak signifikant vom Rest des Spektrums abhebt, werden zuerst Mittelwert und Standardabweichung des Spektrums über

```python
AMean = np.mean( A )
AStd = np.std( A )
```

berechnet. 

`numpy` bietet eine einfache Möglichkeit das maximale Argument in einer Liste zu finden - die Funktion `np.argmax()`. Diese gibt jedoch nicht den Wert selbst, sondern dessen Index in der Liste aus. Dies erlaubt es nun, sowohl Frequenz als auch zugehörigen Wert auszulesen via:

```python
idx = np.argmax( A )
f_, A_ = f[idx], A[idx]
```

Verwendet werden sollen nun nur Werte, die sich signifikant vom gesamten Spektrum abheben. Dies wird geprüft über:

```python
abs(AMean - A_) > 3 * AStd
```

Hierbei wurde die dreifache Standardabweichung gewählt, wobei der Wert nach Bedarf auch erhöht werden kann.

Die Prozedur zum Auffinden der maximalen Werte innerhalb eines Spektrums kann nun mehrfach wiederholt werden. Wurde ein Peak gefunden, so muss dieser auf null gesetzt werden, um eine erneute Suche zu starten. Wurde kein Peak gefunden, so bricht das Programm ab.

Anbei das komplette Programm zum Auffinden der Maxima

```python
import numpy as np

f, A, Ar, Ai = np.genfromtxt('<file name>').T

# Herausfiltern der 0 Hz - Linie
A = A[f > 0]
f = f[f > 0]

# Mittelwert und Standardabweichung
AMean = np.mean( A )
AStd = np.std( A )

# Endlosschleife
print '# f (Hz)\t A (a.u.)'
while True:
    # Finden des Maximums
    idx = np.argmax( A )
    f_, A_ = f[idx], A[idx]
    
    # Hebt sich das Maximum signifikant vom Rest des Spektrums ab?
    if abs(AMean - A_) > 3 * AStd:
        print '%.2f\t%.2f' % f_, A_
        
        # Zuruecksetzen des Peaks
        A[idx] = 0
    else:
        break
```

