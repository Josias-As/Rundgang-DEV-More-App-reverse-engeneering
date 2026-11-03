# Paket 19 – Fix: Datum (und andere Eingaben) werden überschrieben

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket19) und `werkzeuge/doc_paket19.py`. Setzt auf den Stand **nach Paket N + 8–10** auf. Die 6 Properties ändert kein anderes Paket → passt auch, wenn später 12–17/13 eingefügt werden (Reihenfolge egal).

## Kurzfassung

- **Fehler (Studio-Test 03.11.):** Datum wählen → Feld springt auf „Datum wählen“ zurück, `WertText` bleibt leer, Punkt bleibt offen.
- **Ursache (geschlussfolgert, passt zum Befund):** In jeder Karte liegen alle Eingabe-Steuerelemente, nur das passende ist sichtbar. Die unsichtbaren hängen mit `Default`/`DefaultSelectedItems` an `ThisItem.WertText`. Schreibt das Datum `WertText`, setzen `cboKaMehrfach` und `ddKaAuswahl` ihre Auswahl neu, ihr `OnChange` feuert und schreibt "" zurück. Derselbe Fehler hätte auch Mehrfachauswahl und Auswahl getroffen.
- **Abhilfe:** Jede Schreibstelle schreibt nur beim eigenen Typ (und Mehrfach/Auswahl/Text nur bei echter Änderung). 6 Properties, keine neuen Steuerelemente, keine Spalten.
- Generator 0 Fehler, Mutation 12/12, Logik-Probe 104/0. **Nicht in Studio getestet.** Nicht unabhängig geprüft (kleiner Fix).

## Schritte

### 19.1 · `cboKaMehrfach.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › cboKaMehrfach` → OnChange

```
With({neu: Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As i; i.Value <> "" && i.Value in Self.SelectedItems.Value); Value; "; ")};
    If(ThisItem.Typ = "MEHRFACH" && !varNurLesen && neu <> ThisItem.WertText;
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: neu});;
        Set(varGeaendert; true)
    )
)
```

```diff
- Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As i; i.V …
-Set(varGeaendert; true)
+With({neu: Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As i; i.Value <> "" && i.Value in Self.SelectedItems.Value); Value; "; ")};
+    If(ThisItem.Typ = "MEHRFACH" && !varNurLesen && neu <> ThisItem.WertText;
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: neu});;
+        Set(varGeaendert; true)
+    )
+)
```

**Kurz erklärt:** **Hauptursache.** Das unsichtbare Kombinationsfeld hängt mit `DefaultSelectedItems` an `WertText`. Ändert das Datum `WertText`, wählt es neu aus, `OnChange` feuert und schrieb "" zurück. Jetzt schreibt es nur bei Mehrfachauswahl und nur, wenn sich wirklich etwas ändert.

**Nachprüfen:** endet auf `)`

### 19.2 · `ddKaAuswahl.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › ddKaAuswahl` → OnChange

```
If(ThisItem.Typ = "AUSWAHL" && !varNurLesen && Coalesce(Self.Selected.Value; "") <> ThisItem.WertText;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Coalesce(Self.Selected.Value; "")});;
    Set(varGeaendert; true)
)
```

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Coalesce(Self.Selected.Value; "")});;
-Set(varGeaendert; true)
+If(ThisItem.Typ = "AUSWAHL" && !varNurLesen && Coalesce(Self.Selected.Value; "") <> ThisItem.WertText;
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Coalesce(Self.Selected.Value; "")});;
+    Set(varGeaendert; true)
+)
```

**Kurz erklärt:** Gleiches Muster (`Default = ThisItem.WertText`): schreibt nur bei Auswahl-Punkten und nur bei echter Änderung.

**Nachprüfen:** endet auf `)`

### 19.3 · `dpKaDatum.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › dpKaDatum` → OnChange

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
-Set(varGeaendert; true)
+If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
+ Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKa …
+    Set(varGeaendert; true)
+)
```

**Kurz erklärt:** Schreibt nur bei Datum/Datum+Uhrzeit. Sonst unverändert.

**Nachprüfen:** endet auf `)`

### 19.4 · `ddKaStunde.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › ddKaStunde` → OnChange

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
-Set(varGeaendert; true)
+If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
+    Set(varGeaendert; true)
+)
```

**Kurz erklärt:** Wie `dpKaDatum`.

**Nachprüfen:** endet auf `)`

### 19.5 · `ddKaMinute.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › ddKaMinute` → OnChange

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
-Set(varGeaendert; true)
+If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
+    Set(varGeaendert; true)
+)
```

**Kurz erklärt:** Wie `dpKaDatum`.

**Nachprüfen:** endet auf `)`

### 19.6 · `txtKaText.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › txtKaText` → OnChange

```
If(ThisItem.Typ = "TEXT" && !varNurLesen && Self.Text <> ThisItem.WertText;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Self.Text});;
    Set(varGeaendert; true)
)
```

```diff
-Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Self.Text});;
-Set(varGeaendert; true)
+If(ThisItem.Typ = "TEXT" && !varNurLesen && Self.Text <> ThisItem.WertText;
+    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Self.Text});;
+    Set(varGeaendert; true)
+)
```

**Kurz erklärt:** Vorsorglich gleich gebaut: schreibt nur bei Text-Punkten und nur bei echter Änderung.

**Nachprüfen:** endet auf `)`

## Test

| # | Schritt | erwartet |
|---|---|---|
| T1 | „ZZ Test Datum letzte Wartung“: Datum wählen | Datum bleibt stehen, Punkt verschwindet aus „Noch offen“ |
| T2 | Kategorie speichern, wieder öffnen | Datum steht noch da |
| T3 | „Leeren“ | Feld leer, Punkt wieder offen |
| T4 | Datum + Uhrzeit: Datum, Stunde, Minute wählen | alles bleibt stehen, Text „TT.MM.JJJJ HH:MM“ im Protokoll |
| T5 | Mehrfachauswahl: zwei Werte wählen, einen abwählen | Auswahl bleibt, Protokoll zeigt die Werte mit „; “ |
| T6 | Auswahl (Dropdown) und Text | bleiben gespeichert (Gegenprobe) |

## Rückweg

Vorher-Fassungen aus dem Anhang einsetzen.

## Anhang – Vorher-Fassungen

**`cboKaMehrfach.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Concat(Filter(ForAll(Split(ThisItem.Auswahl; ";") As s; {Value: Trim(s.Value)}) As i; i.Value <> "" && i.Value in Self.SelectedItems.Value); Value; "; ")});;
Set(varGeaendert; true)
```

**`ddKaAuswahl.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Coalesce(Self.Selected.Value; "")});;
Set(varGeaendert; true)
```

**`dpKaDatum.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
Set(varGeaendert; true)
```

**`ddKaStunde.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
Set(varGeaendert; true)
```

**`ddKaMinute.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
Set(varGeaendert; true)
```

**`txtKaText.OnChange` vorher**

```
Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Self.Text});;
Set(varGeaendert; true)
```

