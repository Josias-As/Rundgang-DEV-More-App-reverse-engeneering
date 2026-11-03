# Paket 22 – Hinweis „(mehrere möglich)“ an Mehrfach-Fragen

Stand 03.11.2026. Erzeugt mit `werkzeuge/baukasten.py` (paket22) und `werkzeuge/doc_paket19.py`. Setzt auf den Stand nach N + 8–10 + 19–21 auf. Paket 13 ändert nur `lblKaFrage.Width`, nicht `Text` → passt danach unverändert (Kette 21 → 22 → 12 … 13, geprüft).

## Kurzfassung

- Bei Typ MEHRFACH steht hinter der Frage (und hinter dem Pflicht-Stern) `  (mehrere möglich)`, z. B. „ZZ Test Mängelarten  *  (mehrere möglich)“.
- Textbreite geprüft: Beispiel 470 px bei Größe 17, Platz im ungünstigsten Fall (Bild + ⓘ) 530 px → passt in eine Zeile. Sehr lange Fragen werden wie bisher abgeschnitten (Höhe 32 ist fest, nicht neu).
- Das Auswahlfeld zeigt schon „Auswählen (mehrere möglich)“, solange nichts gewählt ist. Der Hinweis an der Frage bleibt auch nach der Auswahl sichtbar.
- 1 Property. Generator 0 Fehler. **Nicht in Studio getestet.**

## Schritt

### 22.1 · `lblKaFrage.Text`

**Pfad:** `scrKategorie › galKaPruefpunkte › conKaKarte › lblKaFrage` → Text

```
ThisItem.Frage & If(ThisItem.Pflicht; "  *"; "") & If(ThisItem.Typ = "MEHRFACH"; "  (mehrere möglich)"; "")
```

```diff
-ThisItem.Frage & If(ThisItem.Pflicht; "  *"; "")
+ThisItem.Frage & If(ThisItem.Pflicht; "  *"; "") & If(ThisItem.Typ = "MEHRFACH"; "  (mehrere möglich)"; "")
```

**Kurz erklärt:** Hängt bei Mehrfachauswahl den Hinweis an. Alle anderen Typen unverändert.

**Nachprüfen:** endet auf `m.Pflicht; "  *"; "") & If(ThisItem.Typ = "MEHRFACH"; "  (mehrere möglich)"; "")`

## Test

1. Mehrfach-Frage (Pflicht): „… *  (mehrere möglich)“. 2. Mehrfach ohne Pflicht: „…  (mehrere möglich)“. 3. Andere Typen: unverändert.

## Rückweg

```
ThisItem.Frage & If(ThisItem.Pflicht; "  *"; "")
```

