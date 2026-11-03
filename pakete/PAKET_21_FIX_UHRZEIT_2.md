# Paket 21 – Fix: Uhrzeit (zweiter Anlauf)

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket21) und `werkzeuge/doc_paket19.py`. Setzt auf den Stand **nach N + 8–10 + 19 + 20** auf (Paket 20 bleibt drin).

## Kurzfassung

- **Fehler (Studio nach 20):** Stunde wählen → springt sofort zurück, `WertText` bleibt nur das Datum.
- **Ursache (Vermutung Einsetz-Chat, passt zu den Formeln):** Nach dem Schreiben der Stunde wird die Karte neu gezeichnet, `dpKaDatum.OnChange` feuert erneut und baute den Text aus `ddKaStunde.Selected` – das in diesem Moment leer ist → nur Datum.
- **Abhilfe (Vorschlag Einsetz-Chat übernommen):** Jedes der drei Felder ändert nur seinen Teil und liest den Rest aus `ThisItem.WertText`. Jedes schreibt nur bei echter Änderung. Ein erneutes Feuern ändert damit nichts mehr (Logik-Probe: nach jedem Schritt alle drei OnChange noch einmal mit ihrem Default → Wert bleibt gleich, 8 Abläufe).
- 3 Properties (je ganz ersetzen). Generator 0 Fehler, Logik-Probe 115/0. **Nicht in Studio getestet.**

## Schritte

### 21.1 · `dpKaDatum.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › dpKaDatum` → OnChange

```
With({h: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--"); m: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--")};
    If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen && Coalesce(Text(Self.SelectedDate; "dd.mm.yyyy"); "") <> Left(ThisItem.WertText; 10);
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; If(h = "--"; ""; h); If(m = "--"; ""; m); ThisItem.Typ = "DATUMZEIT")});;
        Set(varGeaendert; true)
    )
)
```

```diff
-If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
- Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKa …
-    Set(varGeaendert; true)
+With({h: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--"); m: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--")};
+    If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen && Coalesce(Text(Self.SelectedDate; "dd.mm.yyyy"); "") <> Left(ThisItem.WertText; 10);
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; If(h = "--"; ""; h); If(m = "--"; ""; m); ThisItem.Typ = "DATUMZEIT")});;
+        Set(varGeaendert; true)
+    )
```

**Kurz erklärt:** Schreibt nur, wenn sich das **Datum** wirklich ändert. Die Uhrzeit nimmt es aus dem gespeicherten Wert, nicht aus den Nachbarfeldern. So überschreibt ein erneutes Feuern beim Neuzeichnen nichts mehr.

**Nachprüfen:** endet auf `)`

### 21.2 · `ddKaStunde.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › ddKaStunde` → OnChange

```
With({neu: If(Coalesce(Self.Selected.Value; "") = ""; "--"; Self.Selected.Value); alt: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--"); rest: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--")};
    If(ThisItem.Typ = "DATUMZEIT" && !varNurLesen && Len(ThisItem.WertText) >= 10 && neu <> alt;
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Left(ThisItem.WertText; 10) & If(neu = "--" && rest = "--"; ""; " " & neu & ":" & rest)});;
        Set(varGeaendert; true)
    )
)
```

```diff
-If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
-    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
-    Set(varGeaendert; true)
+With({neu: If(Coalesce(Self.Selected.Value; "") = ""; "--"; Self.Selected.Value); alt: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--"); rest: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--")};
+    If(ThisItem.Typ = "DATUMZEIT" && !varNurLesen && Len(ThisItem.WertText) >= 10 && neu <> alt;
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Left(ThisItem.WertText; 10) & If(neu = "--" && rest = "--"; ""; " " & neu & ":" & rest)});;
+        Set(varGeaendert; true)
+    )
```

**Kurz erklärt:** Ändert nur die Stunde, die Minute kommt aus dem gespeicherten Wert. Schreibt nur bei echter Änderung und nur, wenn ein Datum da ist.

**Nachprüfen:** endet auf `)`

### 21.3 · `ddKaMinute.OnChange`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › ddKaMinute` → OnChange

```
With({neu: If(Coalesce(Self.Selected.Value; "") = ""; "--"; Self.Selected.Value); alt: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--"); rest: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--")};
    If(ThisItem.Typ = "DATUMZEIT" && !varNurLesen && Len(ThisItem.WertText) >= 10 && neu <> alt;
        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Left(ThisItem.WertText; 10) & If(neu = "--" && rest = "--"; ""; " " & rest & ":" & neu)});;
        Set(varGeaendert; true)
    )
)
```

```diff
-If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
-    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
-    Set(varGeaendert; true)
+With({neu: If(Coalesce(Self.Selected.Value; "") = ""; "--"; Self.Selected.Value); alt: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 15; 2); "--"); rest: If(Len(ThisItem.WertText) >= 16; Mid(ThisItem.WertText; 12; 2); "--")};
+    If(ThisItem.Typ = "DATUMZEIT" && !varNurLesen && Len(ThisItem.WertText) >= 10 && neu <> alt;
+        Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: Left(ThisItem.WertText; 10) & If(neu = "--" && rest = "--"; ""; " " & rest & ":" & neu)});;
+        Set(varGeaendert; true)
+    )
```

**Kurz erklärt:** Wie die Stunde, für die Minute.

**Nachprüfen:** endet auf `)`

## Test

| # | Schritt | erwartet (`WertText`) |
|---|---|---|
| T1 | Datum 02.11. | `02.11.2026`, offen „(Uhrzeit)“ |
| T2 | Stunde 08 | `02.11.2026 08:--`, 08 bleibt stehen |
| T3 | Minute 30 | `02.11.2026 08:30`, nicht mehr offen |
| T4 | Datum auf 03.11. ändern | `03.11.2026 08:30` (Uhrzeit bleibt) |
| T5 | neue Karte: erst Minute, dann Stunde | `… 08:30` |
| T6 | speichern, neu öffnen; „Leeren“ | Werte stehen da; danach leer |
| T7 | Typ DATUM | unverändert |

## Rückweg

Vorher-Fassungen aus dem Anhang einsetzen.

## Anhang – Vorher-Fassungen

**`dpKaDatum.OnChange` vorher**

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(Self.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

**`ddKaStunde.OnChange` vorher**

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(Self.Selected.Value; ""); Coalesce(ddKaMinute.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

**`ddKaMinute.OnChange` vorher**

```
If((ThisItem.Typ = "DATUM" || ThisItem.Typ = "DATUMZEIT") && !varNurLesen;
    Patch(colAntworten; LookUp(colAntworten; PruefpunktID = ThisItem.PruefpunktID); {WertText: fnDatumText(dpKaDatum.SelectedDate; Coalesce(ddKaStunde.Selected.Value; ""); Coalesce(Self.Selected.Value; ""); ThisItem.Typ = "DATUMZEIT")});;
    Set(varGeaendert; true)
)
```

