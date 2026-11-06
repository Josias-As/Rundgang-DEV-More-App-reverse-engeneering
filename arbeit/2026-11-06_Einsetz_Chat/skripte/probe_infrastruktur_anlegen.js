// Probe-Rundgang „ZZ Test Infrastrukturrundgang“ anlegen (02.11.2026)
// Ausführen: IMS+ (https://technoformgroup.sharepoint.com/sites/IMSKonzept) öffnen → F12 → Konsole → einfügen → Enter.
// Legt an: 1 Rundgang, 5 Bereiche, 11 Kategorien, ~75 Prüfpunkte, 1 Plan (jeden Montag).
// Bricht ab, wenn es den Rundgang schon gibt. Ändert nichts Bestehendes.
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const RUNDGANG = "ZZ Test Infrastrukturrundgang";
  const H = { "Accept": "application/json;odata=nometadata", "Content-Type": "application/json;odata=nometadata" };
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: H })).json()).FormDigestValue;
  const get = async (url) => { const r = await fetch(SITE + url, { headers: H }); if (!r.ok) throw new Error(url + " → " + r.status); return (await r.json()).value; };
  const add = async (liste, daten) => {
    const r = await fetch(SITE + "/_api/web/lists/getbytitle('" + liste + "')/items", { method: "POST", headers: { ...H, "X-RequestDigest": digest }, body: JSON.stringify(daten) });
    if (!r.ok) throw new Error(liste + " „" + daten.Title + "“ → " + r.status + " " + (await r.text()));
    return (await r.json()).Id;
  };

  const vorhanden = await get("/_api/web/lists/getbytitle('RG_Rundgaenge')/items?$select=Id&$filter=Title eq '" + RUNDGANG + "'");
  if (vorhanden.length) { console.warn("ABBRUCH: „" + RUNDGANG + "“ gibt es schon (Id " + vorhanden[0].Id + "). Nichts angelegt."); return; }

  // Kurzschreibweisen für Prüfpunkte
  const io = (t, x = {}) => ({ Title: t, Eingabetyp: "IONIO", ...x });
  const zahl = (t, einheit, modus, min, max, x = {}) => ({ Title: t, Eingabetyp: "ZAHL", Einheit: einheit, Grenzmodus: modus, MinWert: min, MaxWert: max, ...x });
  const zaehler = (t, einheit, x = {}) => zahl(t, einheit, "Sperren", 0, 99999999, x);
  const text = (t, x = {}) => ({ Title: t, Eingabetyp: "TEXT", ...x });
  const raumTemp = (t) => zahl(t, "°C", "Warnen", 18, 26);
  const PLATZHALTER = "Platzhalter: Bezeichnung aus dem Original-PDF übernehmen.";

  const kompressor = (n) => [
    zahl("Kompressor " + n + " – Betriebsdruck", "bar", "Warnen", 6, 9),
    zaehler("Kompressor " + n + " – Betriebsstunden", "h", { Foto: "Optional" }),
    zahl("Kompressor " + n + " – Temperatur", "°C", "Sperren", -20, 150),
    io("Kompressor " + n + " – Druckluftfilter störungsfrei"),
  ];
  const kaeltemaschine = (n, bs1, bs2, hinweis) => [
    io("Kältemaschine " + n + " – Kühllamellen", hinweis ? { Hinweis: hinweis } : {}),
    zahl("Kältemaschine " + n + " – Wassertemperatur Ausgang", "°C", "Warnen", 6, 16, { Foto: "Optional" }),
    zaehler("Kältemaschine " + n + " – Betriebsstunden " + bs1, "h"),
    zaehler("Kältemaschine " + n + " – Betriebsstunden " + bs2, "h"),
    io("Kältemaschine " + n + " – Allgemeinzustand"),
  ];

  const AUFBAU = [
    { bereich: "Batterieraum", kategorien: [
      { name: "Batterieraum", punkte: [ io("Kontrolle, ob störungsfrei") ] } ] },
    { bereich: "Infrastrukturraum", kategorien: [
      { name: "Wasser & Allgemein", punkte: [
        io("Kontrolle Ordnung und Sauberkeit"),
        zaehler("Zählerstand Wasseruhr", "m³"),
        zahl("Wasserdruck", "bar", "Warnen", 1, 4, { Hinweis: PLATZHALTER }) ] },
      { name: "Kompressoren", punkte: [ ...kompressor(3), ...kompressor(2), ...kompressor(1) ] },
      { name: "Kältetrockner & Wasseraufbereitung", punkte: [
        io("Kältetrockner 1"),
        io("Kältetrockner 2"),
        io("Wasseraufbereitung (Jansen) – Sichtkontrolle"),
        io("Kontrolle Wasseraufbereitung störungsfrei"),
        io("Wamat – Wasserqualität mit Teststreifen", { Foto: "Pflicht", Hinweis: "Foto vom Teststreifen neben der Farbskala." , _merke: "wamat" }),
        text("Wamat – gemessener Wert und Maßnahme", { _bedingung: "wamat", BedingungWert: "NIO" }) ] },
      { name: "ONI Kühlanlage", punkte: [
        io("Kontrolle Ordnung und Sauberkeit"),
        zahl("Systemdruck", "bar", "Warnen", 1.5, 3.5),
        io("Siebkorbfilter 1", { Hinweis: "Ab 0,5 bar Reinigung." }),
        io("Siebkorbfilter 2", { Hinweis: "Ab 0,5 bar Reinigung." }),
        io("ONI – Prüfpunkt A", { Hinweis: PLATZHALTER }),
        io("ONI – Prüfpunkt B", { Hinweis: PLATZHALTER }),
        io("Luftfilter Schaltschrank"),
        zaehler("Zählerstand Wasseruhr über Tank", "m³") ] },
      { name: "Kältemaschinen", punkte: [
        ...kaeltemaschine(1, "C1", "C2", "Außenbereich, Display im Infrastrukturraum."),
        ...kaeltemaschine(2, "A1", "B1/C1", "Außenbereich."),
        ...kaeltemaschine(3, "A1", "B1/C1", "Außenbereich, Display im Infrastrukturraum.") ] } ] },
    { bereich: "Produktionshalle", kategorien: [
      { name: "Tore & Halle", punkte: [
        ...[1, 2, 3, 4, 5, 6].map(n => io("Sichtprüfung Tor " + n + " (Funktion, Piktogramm)")),
        io("WZB – Aktivkohlefilter / Gefahrstoffschränke"),
        io("Sichtprüfung Regalanlagen"),
        io("Elektronische Dachfenstersteuerung / Lichtschalter") ] },
      { name: "Mess- & Klimaräume", punkte: [
        zahl("Haftungskabine – Temperatur", "°C", "Warnen", 15, 30),
        io("Analysebüro – Sichtprüfung Stickstoffflasche"),
        zahl("Analysebüro – Füllung Stickstoffflasche", "bar", "Warnen", 30, 300),
        raumTemp("Analysebüro – Temperatur Klimaanlage"),
        raumTemp("Messraum – Temperatur"),
        raumTemp("Wareneingangsbüro – Temperatur Klimaanlage"),
        raumTemp("Warenausgangsbüro – Temperatur Klimaanlage"),
        raumTemp("Büro 1. OG – Temperatur") ] },
      { name: "Zählerstände Wasser", punkte:
        [1, 2, 3, 4, 5, 6, 7, 8].map(n => zaehler("Wasserzähler " + n, "m³", { Hinweis: PLATZHALTER })) } ] },
    { bereich: "Elektro", kategorien: [
      { name: "Kompensation & Hauptverteilung", punkte: [
        zahl("cos φ Kompensationsanlage", "cos φ", "Mangel", 0.9, 1, { Hinweis: "Normalbereich cos φ > 0,90." }),
        io("Sichtprüfung Filtervlies Kompensationsanlage", { Hinweis: "Reinigung nur durch eingewiesenes Fachpersonal." }),
        ...[1, 2, 3, 4].map(n => zaehler("Zählerstand Hauptverteilung " + n, "kWh")) ] } ] },
    { bereich: "Abschluss", kategorien: [
      { name: "Mangelbeschreibung", punkte: [ text("Mangelbeschreibung / Sonstiges", { Pflicht: false }) ] } ] },
  ];

  const ergebnis = { rundgang: 0, plan: 0, bereiche: [], kategorien: [], pruefpunkte: [] };
  const merke = {};
  ergebnis.rundgang = await add("RG_Rundgaenge", { Title: RUNDGANG, Beschreibung: "ZZ Test – Probe nach MoreApp-PDF Infrastrukturrundgang TGI MMS (02.11.2026). Grenzwerte außer cos φ sind Annahmen.", RgReihenfolge: 90, Aktiv: true });
  let bNr = 0;
  for (const b of AUFBAU) {
    const bid = await add("RG_Bereiche", { Title: b.bereich, RundgangID: ergebnis.rundgang, RgReihenfolge: ++bNr * 10, Aktiv: true });
    ergebnis.bereiche.push(bid);
    let kNr = 0;
    for (const k of b.kategorien) {
      const kid = await add("RG_Kategorien", { Title: k.name, BereichID: bid, RgReihenfolge: ++kNr * 10, Aktiv: true });
      ergebnis.kategorien.push(kid);
      let pNr = 0;
      for (const p of k.punkte) {
        const { _merke, _bedingung, ...felder } = p;
        const daten = { KategorieID: kid, RgReihenfolge: ++pNr * 10, Pflicht: true, Aktiv: true, Foto: "Aus", KommentarPflicht: false, ...felder };
        if (_bedingung) daten.BedingungPunkt = merke[_bedingung];
        const pid = await add("RG_Pruefpunkte", daten);
        ergebnis.pruefpunkte.push(pid);
        if (_merke) merke[_merke] = pid;
      }
    }
  }
  ergebnis.plan = await add("RG_Plan", { Title: "ZZ Test Mo jede Woche (Probe Infrastruktur)", RundgangID: ergebnis.rundgang, Wochentag: 1, ZyklusWochen: 1, StartMontag: "2026-10-19", Aktiv: true });

  console.log("FERTIG. Rundgang " + ergebnis.rundgang + " · " + ergebnis.bereiche.length + " Bereiche · " + ergebnis.kategorien.length + " Kategorien · " + ergebnis.pruefpunkte.length + " Prüfpunkte · Plan " + ergebnis.plan);
  console.log("IDS " + JSON.stringify(ergebnis));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken. Bereits Angelegtes bleibt stehen."));
