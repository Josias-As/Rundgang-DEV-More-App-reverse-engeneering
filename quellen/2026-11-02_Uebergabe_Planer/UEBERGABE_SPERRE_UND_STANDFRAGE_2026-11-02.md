# An den Analyse-Chat: neuer Umbaupunkt „Kategorie-Sperre entfernen“ + Frage nach dem aktuellen Stand (02.11.2026)

Von: Planer-Chat (Josias' Hauptkonto). Josias leitet das weiter.

## 1. Bitte zuerst: Was ist neu?
Josias sagt, ihr habt inzwischen **die Rundgang-Builder-App gebaut** und es sind **weitere Änderungen** dazugekommen. Mein Wissensstand ist: Pakete 1–6 eingebaut (Export-Basis 27.10. 09:09), nicht veröffentlicht, Tests Gruppe 2 offen. **Meine Vorschläge können deshalb veraltet sein.**

Bitte schick Josias eine kurze Zusammenfassung für mich:
1. Builder-App: Name/ID, was sie kann, welche Listen/Spalten sie schreibt.
2. Welche Änderungen an „Rundgang DEV“ seit Paket 6 (Steuerelemente/Properties, neue Spalten/Listen, umbenannte Dinge).
3. Ist veröffentlicht worden? Welche Tests sind gelaufen?
4. Welche Punkte aus `UEBERGABE_NEUE_ANFORDERUNGEN_2026-11-02.md` sind schon erledigt oder anders gelöst?

## 2. Zur Info: Probe-Rundgang angelegt (heute, per Konsolen-Skript von Josias)
„ZZ Test Infrastrukturrundgang“ nach dem MoreApp-PDF: Rundgang **3**, Plan **10** (Montag jede Woche), Bereiche **6–10**, Kategorien **9–19**, Prüfpunkte **39–115** (77). Grenzwerte außer cos φ sind Annahmen (Warnen). Skript: `bau/probe/probe_infrastruktur_anlegen.js`. Falls die Builder-App andere Spalten erwartet (z. B. Status/Schlüssel), bitte sagen, was an diesen Einträgen fehlt.
Offen bei Josias: Sind Haustechnik- und Infrastrukturrundgang in Wirklichkeit **ein** Rundgang (dann zusammenführen) oder zwei?

## 3. Neuer Umbaupunkt
**[Josias]** „Wir brauchen die Sperre nicht mehr, dass man einen Bereich erst machen kann, wenn man den davor gemacht hat.“
Gemeint ist die Reihenfolge-Sperre der **Kategorien** (Speicherschritte).

### Soll-Verhalten (Vorschlag Planer-Chat)
- Alle Kategorien in beliebiger Reihenfolge öffnen **und speichern**.
- Die erste offene Kategorie bleibt als Vorschlag markiert („▶ Als Nächstes“), die übrigen „○ Offen“ statt „🔒 Gesperrt“.
- „Speichern & weiter“ springt weiter zur nächsten **offenen** Kategorie (bitte prüfen, ob es heute „Position + 1“ nimmt – dann landet man evtl. in einer schon erledigten).
- „Rundgang abschließen“ bleibt erst möglich, wenn **alle** Kategorien gespeichert sind (unverändert).

### Wo die Sperre steckt (Stand meines Exports 25./26.10. – bitte gegen aktuellen Stand prüfen)
1. `scrRundgang › galRuKategorien.Items`: `Zustand` = `"erledigt" | "naechste" | "gesperrt"` → `"gesperrt"` durch `"offen"` ersetzen.
2. Anzeige-Texte mit Standardzweig „gesperrt“: `lblRuSymbol.Text` (🔒 → ○), `lblRuKatZustand.Text` („Gesperrt – erst die vorherige Kategorie abschließen“ → „Offen“), `btnRuOeffnen.Text` („Gesperrt“ → „Öffnen“). Die übrigen Prüfungen auf `"gesperrt"` (Fill, DropShadow, DisplayMode, OnSelect-Notify, Farben) greifen danach nie mehr; können bleiben oder aufgeräumt werden.
3. **`scrKategorie › btnKaSpeichern.OnSelect`**: Zweig im großen `If` entfernen:
   ```
   IsBlank(erg) && CountRows(Filter(colKatListe As kl; kl.Position < varKatPos && IsBlank(LookUp(colErledigt As e; e.KategorieID = kl.KategorieID)))) > 0;
       Notify("Bitte zuerst die vorherigen Kategorien abschließen."; NotificationType.Warning);
   ```
   Diese Formel habt ihr in Paket 1–6 stark geändert – ich habe die aktuelle Fassung nicht. **Bitte ihr liefert die ganze Property.**
4. Bitte prüfen, ob es weitere Stellen gibt (z. B. Weiter-Sprung nach dem Speichern, Timer, Builder-App-Einstellung, Protokoll-Reihenfolge, Text „Kategorien können nur nacheinander …“ irgendwo).
5. Optional überlegen: Reihenfolge-Pflicht **pro Rundgang einstellbar** machen (Spalte z. B. `FesteReihenfolge` Ja/Nein in `RG_Rundgaenge`, pflegbar in der Builder-App)? Josias wollte die Sperre nur weg haben – nur vorschlagen, nicht ungefragt bauen.

### Bitte an euch
- Ist das so gut, oder ist es durch eure neue Struktur/Builder-App anders zu lösen?
- Liefert das Paket im gewohnten Format (`ARBEITSWEISE_AENDERUNGEN.md`: Steuerelement → Property, ganze Property, deutsch, Vorher/Nachher, Test, Rückweg).
- Test: Rundgang starten → direkt Kategorie 3 öffnen, ausfüllen, speichern → klappt; Abschluss erst nach allen Kategorien.
