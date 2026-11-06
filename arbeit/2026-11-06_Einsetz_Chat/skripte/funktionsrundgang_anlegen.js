// „ZZ Test Funktionsrundgang“ anlegen (03.11.2026) – zeigt jede Funktion der App, sinnvoll gruppiert
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Bricht ab, wenn es den Rundgang schon gibt. Ändert nichts Bestehendes.
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const RUNDGANG = "ZZ Test Funktionsrundgang";
  const H = { "Accept": "application/json;odata=nometadata", "Content-Type": "application/json;odata=nometadata" };
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: H })).json()).FormDigestValue;
  const get = async (url) => { const r = await fetch(SITE + url, { headers: H }); if (!r.ok) throw new Error(url + " → " + r.status); return (await r.json()).value; };
  const add = async (liste, daten) => {
    const r = await fetch(SITE + "/_api/web/lists/getbytitle('" + liste + "')/items", { method: "POST", headers: { ...H, "X-RequestDigest": digest }, body: JSON.stringify(daten) });
    if (!r.ok) throw new Error(liste + " „" + daten.Title + "“ → " + r.status + " " + (await r.text()).slice(0, 300));
    return (await r.json()).Id;
  };

  if ((await get("/_api/web/lists/getbytitle('RG_Rundgaenge')/items?$select=Id&$filter=Title eq '" + RUNDGANG + "'")).length) {
    console.warn("ABBRUCH: „" + RUNDGANG + "“ gibt es schon. Nichts angelegt."); return;
  }
  const kontakte = await get("/_api/web/lists/getbytitle('RG_Ansprechpartner')/items?$select=Id,Title");
  const kId = (t) => String((kontakte.find(k => k.Title === t) || {}).Id || "");
  let bildId = 0;
  try { bildId = ((await get("/_api/web/lists/getbytitle('RG_Hinweisbilder')/items?$select=Id&$top=1"))[0] || {}).Id || 0; } catch (e) { bildId = 0; }

  const io = (t, x = {}) => ({ Title: t, Eingabetyp: "IONIO", ...x });
  const zahl = (t, einheit, modus, min, max, x = {}) => ({ Title: t, Eingabetyp: "ZAHL", Einheit: einheit, Grenzmodus: modus, ...(min === null ? {} : { MinWert: min }), ...(max === null ? {} : { MaxWert: max }), ...x });
  const text = (t, x = {}) => ({ Title: t, Eingabetyp: "TEXT", ...x });
  const auswahl = (t, werte, x = {}) => ({ Title: t, Eingabetyp: "AUSWAHL", Auswahlwerte: werte, ...x });
  const mehrfach = (t, werte, x = {}) => ({ Title: t, Eingabetyp: "MEHRFACH", Auswahlwerte: werte, ...x });
  const datum = (t, x = {}) => ({ Title: t, Eingabetyp: "DATUM", ...x });
  const datumzeit = (t, x = {}) => ({ Title: t, Eingabetyp: "DATUMZEIT", ...x });
  const abs = (name, punkte) => punkte.map(p => ({ ...p, Abschnitt: name }));

  const AUFBAU = [
    { bereich: "A · Eingabearten", kategorien: [
      { name: "1 · Antworten i.O. / n.i.O.", punkte: [
        ...abs("Grundform", [
          io("Notausgang frei zugänglich", { Hinweis: "Pflichtfrage (*). n.i.O. ergibt einen Mangel, dann ist ein Kommentar Pflicht." }),
          io("Flurbeleuchtung funktioniert", { Pflicht: false, Hinweis: "Freiwillige Frage (kein *): darf leer bleiben." }),
          io("Prüfplakette Feuerlöscher lesbar", { KommentarPflicht: true, Hinweis: "Kommentar immer Pflicht – auch bei i.O. (z. B. Prüfdatum notieren)." }) ]),
        ...abs("Eigene Antwortwörter", [
          io("Legionellenspülung", { TextIO: "durchgeführt", TextNIO: "nicht durchgeführt", Hinweis: "Eigene Knopf-Wörter. „nicht durchgeführt“ zählt wie n.i.O. (Mangel)." }) ]) ] },
      { name: "2 · Auswahl, Text, Datum", punkte: [
        ...abs("Auswahl", [
          auswahl("Zustand Fluchtwegbeschilderung", "gut;verblasst;fehlt", { Hinweis: "Genau eine Antwort aus einer Liste." }),
          mehrfach("Schäden am Rolltor", "keine;Delle;Rost;Laufgeräusch", { Hinweis: "Mehrere Antworten gleichzeitig möglich." }) ]),
        ...abs("Text", [
          text("Ansprechpartner der Fremdfirma vor Ort", { Hinweis: "Freitext." }) ]),
        ...abs("Datum", [
          datum("Letzte Wartung laut Aufkleber", { Hinweis: "Nur ein Datum." }),
          datumzeit("Ablesezeitpunkt Hauptzähler", { Hinweis: "Datum und Uhrzeit: erst das Datum, dann Stunde und Minute wählen." }) ]) ] },
      { name: "3 · Zahlen und Grenzen", punkte: [
        ...abs("Ohne Grenzen", [
          zahl("Zählerstand Wasseruhr", "m³", "Mangel", null, null, { Hinweis: "Zahl ohne Grenzen: jeder Wert ist in Ordnung." }) ]),
        ...abs("Mit Grenzen – drei Modi", [
          zahl("Druck Druckluftnetz", "bar", "Mangel", 6, 9, { Hinweis: "Modus Mangel: außerhalb 6–9 bar wird automatisch n.i.O. (Mangel)." }),
          zahl("Temperatur Serverraum", "°C", "Warnen", 18, 26, { Hinweis: "Modus Warnen: außerhalb 18–26 °C nur Hinweis + Begründung, kein Mangel." }),
          zahl("Öltemperatur Kompressor", "°C", "Sperren", 0, 120, { Hinweis: "Modus Sperren: außerhalb 0–120 °C nicht speicherbar (Schutz vor Tippfehlern)." }) ]),
        ...abs("Nicht messbar", [
          zahl("Wasserdruck Sprinkleranlage", "bar", "Mangel", 1, 10, { NichtMessbar: true, Hinweis: "„nicht messbar“ erlaubt (z. B. Anlage aus): Begründung Pflicht, kein Mangel." }) ]) ] },
      { name: "4 · Fotos", punkte: [
        ...abs("Vier Foto-Regeln", [
          io("Tor 1 – Sichtprüfung", { Foto: "Aus", Hinweis: "Foto aus: kein Foto möglich." }),
          io("Tor 2 – Sichtprüfung", { Foto: "Optional", Hinweis: "Foto optional: Foto möglich, aber nicht nötig." }),
          io("Tor 3 – Sichtprüfung", { Foto: "Pflicht", Hinweis: "Foto Pflicht: ohne Foto nicht speicherbar." }),
          io("Tor 4 – Sichtprüfung", { Foto: "Bei Mangel Pflicht", Hinweis: "Foto bei Mangel Pflicht: nur bei n.i.O. muss ein Foto dazu." }) ]),
        ...(bildId ? abs("Beispielbild", [
          io("Typenschild lesbar", { HinweisBildID: bildId, Hinweis: "Mit Beispielbild: antippen zeigt, wie es aussehen soll." }) ]) : []) ] } ] },
    { bereich: "B · Logik und Sicherheit", kategorien: [
      { name: "5 · Bedingte Folgefragen", punkte: [
        ...abs("Folgefrage bei n.i.O.", [
          io("Ölwanne unter Kompressor trocken", { _merke: "oel", Hinweis: "Bei n.i.O. erscheint darunter eine Folgefrage." }),
          text("Wie viel Öl steht in der Wanne? Maßnahme?", { _bed: "oel", BedingungWert: "NIO", Hinweis: "Erscheint nur, wenn die Frage davor n.i.O. ist." }) ]),
        ...abs("Folgefrage bei bestimmter Auswahl", [
          auswahl("Zustand Kältemittelleitung", "trocken;feucht;tropft", { _merke: "leit", Hinweis: "Bei „tropft“ erscheint eine Folgefrage." }),
          zahl("Tropfen pro Minute", "Tropfen/min", "Mangel", null, null, { _bed: "leit", BedingungWert: "tropft", Hinweis: "Erscheint nur bei „tropft“." }) ]),
        ...abs("Folgefrage bei jeder Antwort", [
          datum("Letzte Filterreinigung", { Pflicht: false, _merke: "filt", Hinweis: "Freiwillig. Sobald ein Datum eingetragen ist, erscheint eine Folgefrage." }),
          text("Wer hat gereinigt?", { _bed: "filt", BedingungWert: "*", Hinweis: "Erscheint bei jeder Antwort auf die Frage davor." }) ]) ] },
      { name: "6 · Rückfrage und kritischer Mangel", punkte: [
        ...abs("Rückfrage", [
          io("Batterieladegerät zeigt Betrieb", { Rueckfrage: true, RueckfrageText: "Normalerweise leuchtet die grüne LED.", Hinweis: "Bei n.i.O. fragt die App „Ist das wirklich so?“." }),
          zahl("Ladestrom", "A", "Mangel", 5, 20, { Rueckfrage: true, Hinweis: "Rückfrage bei Wert außerhalb 5–20 A, nennt die Grenzen." }) ]),
        ...abs("Kritischer Mangel", [
          io("Wasserstoff-Warnanlage ohne Alarm", { Kritisch: true, KritischText: "Raum nicht betreten, Lüftung einschalten.", Ansprechpartner: kId("Elektriker"), Hinweis: "Bei n.i.O. rotes Fenster mit Ansprechpartnern. Speichern erst nach Bestätigung." }),
          io("Klimaanlage Serverraum läuft", { Rueckfrage: true, RueckfrageText: "Normalerweise läuft sie immer.", Kritisch: true, KritischText: "Server-Ausfall droht.", Ansprechpartner: kId("IT-Dienstleister"), Hinweis: "Beides: erst Rückfrage, dann rotes Fenster." }) ]) ] } ] },
    { bereich: "C · Abschluss", ausblenden: true, kategorien: [
      { name: "7 · Abschluss", punkte: [
        io("Alle Türen wieder verschlossen", { Hinweis: "Dieser Bereich ist ausgeblendet: In der Übersicht steht keine Bereichs-Überschrift." }),
        text("Sonstige Bemerkungen", { Pflicht: false, Hinweis: "Freiwilliger Freitext zum Schluss." }) ] } ] },
  ];

  const erg = { rundgang: 0, plaene: [], bereiche: [], kategorien: [], pruefpunkte: [] };
  const merke = {};
  erg.rundgang = await add("RG_Rundgaenge", { Title: RUNDGANG, Beschreibung: "ZZ Test – zeigt jede Funktion der App, sinnvoll gruppiert (03.11.2026).", RgReihenfolge: 95, Aktiv: true });
  let bNr = 0;
  for (const b of AUFBAU) {
    const bid = await add("RG_Bereiche", { Title: b.bereich, RundgangID: erg.rundgang, RgReihenfolge: ++bNr * 10, Aktiv: true, Ausblenden: !!b.ausblenden });
    erg.bereiche.push(bid);
    let kNr = 0;
    for (const k of b.kategorien) {
      const kid = await add("RG_Kategorien", { Title: k.name, BereichID: bid, RgReihenfolge: ++kNr * 10, Aktiv: true });
      erg.kategorien.push(kid);
      let pNr = 0;
      for (const p of k.punkte) {
        const { _merke, _bed, ...felder } = p;
        const daten = { KategorieID: kid, RgReihenfolge: ++pNr * 10, Pflicht: true, Aktiv: true, Foto: "Aus", KommentarPflicht: false, ...felder };
        if (_bed) daten.BedingungPunkt = merke[_bed];
        const pid = await add("RG_Pruefpunkte", daten);
        erg.pruefpunkte.push(pid);
        if (_merke) merke[_merke] = pid;
      }
    }
  }
  const tage = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];
  for (let w = 1; w <= 7; w++) erg.plaene.push(await add("RG_Plan", { Title: "ZZ Test " + tage[w - 1] + " (Funktionsrundgang)", RundgangID: erg.rundgang, Wochentag: w, ZyklusWochen: 1, StartMontag: "2026-10-26", Aktiv: true }));

  console.log("FERTIG. Rundgang " + erg.rundgang + " · " + erg.bereiche.length + " Bereiche · " + erg.kategorien.length + " Kategorien · " + erg.pruefpunkte.length + " Prüfpunkte · " + erg.plaene.length + " Pläne (jeden Tag)" + (bildId ? " · Beispielbild " + bildId : " · kein Beispielbild gefunden"));
  console.log("IDS " + JSON.stringify(erg));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken. Bereits Angelegtes bleibt stehen."));
