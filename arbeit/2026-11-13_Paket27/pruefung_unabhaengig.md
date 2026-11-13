# Unabhängige Prüfung Paket 27 (Builder-Optik), 13.11.2026, leichte Prüfung

Urteil: freigeben mit 3 kleinen Korrekturen (keine hohen Befunde). Nachgerechnet gegen `builder.py`, `builder_nach_p26.json`; `builder.py` und `mutation_builder.py` laufen (0 Fehler, 15/15).

## Nachrechnung (1)
Y-Werte je Typ (conEdP 648 hoch = 768 - 64 - 56). Eigene Rechnung stimmt mit dem Paket überein:
- ZAHL: conPZahl 232..350, conPRest 356..598 (innen max. 242: ddPKategorie 206+36), btnPNio 604..636 (Rand 12; Paket nennt 636 von 648 korrekt), btnPZahlMehr X 324..528 neben btnPNio 0..316 (8 px Abstand). Nichts überlappt.
- AUSWAHL/MEHRFACH: conPWerte 232..342, conPRest 350..592, btnPNio 598..630. IONIO: 232..292, 296..538, 544..576. TEXT/DATUM/DATUMZEIT: conPRest 232..474, btnPNio 480..512. Alle ok.
- Prüffunktion: wertet Visible/If/REST_Y/Parent.Height per Ersetzung aus, steigt in Container ein, zählt Galerien als ein Rechteck. Mutationen (X=300, +256) werden gefunden. Grenzen: Visible, das nicht auswertbar ist, gilt als sichtbar (konservativ, gut).

## Befunde
1. mittel – Prüfung hätte den alten Überlappungsfehler nicht gefunden. Im Vorher-Stand lag `btnPZahlMehr` (X 316..528, Y 56..82 in conPZahl) rechnerisch nur an `btnPNM` (Y 20..56) an, 0 px Abstand, keine echte Überlappung. Gefunden hätte sie nur das Abschneiden unten (648 > 642). Die Prüfung nutzt strenges `<`, Berührung gilt als ok. Vorschlag: Mindestabstand (z. B. 4 px) zwischen Nachbarn prüfen oder im Paket ehrlich schreiben: Die alte Überlappung ist modellmäßig nur „Berührung“; Josias' Beobachtung (Rahmen/Schriftzug) ist damit erklärt, die Prüfung deckt sie nur mit Abstandsregel ab.
2. niedrig – Rückweg: „YAML aus dem Anhang“ stimmt nicht, der Anhang zeigt die alte Property-Liste (ohne `Control:`, mit `;` und `;;` deutsch). Vorschlag: Rückweg schreiben „Knopf `btnPZahlMehr` in conPZahl neu anlegen (Schaltfläche), Properties aus dem Anhang einsetzen“ oder altes YAML (englisch) beilegen. Rest des Rückwegs (Vorher-Fassungen) ist vollständig: alle 16 Properties im Anhang vorhanden und stimmen mit `builder_nach_p26.json` überein.
3. niedrig – `HoverFill` = `PressedFill` = `clrPrimaerHell` und im „an“-Zustand auch `Fill`: dann gibt es beim Überfahren keine sichtbare Rückmeldung. Der Zustand „an“ ist zudem nur an der Füllung erkennbar (kein Text, kein AccessibleLabel). Vorschlag: bei „an“ Text „Verlauf/Vergleich ✓  ›“ ist zu breit (169 px +10 % von 184, ✓ passt noch knapp) oder `HoverFill` = `ColorFade(clrPrimaerHell, -10%)`.
4. niedrig – Textbreite `btnPNio` längster Text: 291 von 296 px (+10 %-Puffer eingerechnet), passt, aber knapp; Schriftart-Ersatz auf einem anderen Gerät könnte umbrechen. Vorschlag: im Test T5 am Tablet ansehen (steht schon drin).
5. niedrig – B2.5 „Nachprüfen: endet auf `0; (LookUp…`“ beginnt mitten in „350;“, wirkt wie ein Tippfehler. Vorschlag: „endet auf `…; 232) + 248`“.

## Zu (2) Verschieben
Vollständig: Löschen in conPZahl, YAML an `conEdP`, Name bleibt, kein Formelverweis auf den Knopf (grep: nur Generator/Mutation). YAML gültig (Classic/Button@2.2.0, englische `,`/`;`, `=`-Präfix, `|-` bei OnSelect), Y-Formel gleich btnPNio. Z-Reihenfolge: eingefügter Knopf liegt oben, stört nicht (keine Überlappung). Reihenfolge B1 → B2 erzeugt keinen kritischen Zwischenzustand (nur kurz Zahl-Bereich 120 hoch).
## Zu (3)
Tests T1–T5 sind ausführbar (T2 braucht einen Prüfpunkt mit Verlauf, dann hellblau). T3 prüft Typ „Text“ mit; „Datum“ unterster Rand 512, kein Risiko.
