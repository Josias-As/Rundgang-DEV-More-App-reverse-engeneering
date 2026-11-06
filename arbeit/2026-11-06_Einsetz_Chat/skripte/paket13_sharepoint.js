// Paket 13, Schritt A1 (SharePoint) – 06.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht nichts.
// 1) Liste RG_Anleitungen (Anleitung: Mehrere Textzeilen nur Text, Aktiv: Ja/Nein Standard Ja) + 1 Testanleitung (nur wenn Liste leer)
// 2) RG_Pruefpunkte: AnleitungID (Zahl, Standard 0)
// 3) Testanleitung an „Prüfplakette Feuerlöscher lesbar“ im ZZ Test Funktionsrundgang (Kategorie 42) hängen
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const NM = "application/json;odata=nometadata", VB = "application/json;odata=verbose";
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: { Accept: NM } })).json()).FormDigestValue;
  const req = async (method, url, body, verbose, extra = {}) => {
    const t = verbose ? VB : NM;
    const r = await fetch(SITE + url, { method, headers: { Accept: t, "Content-Type": t, "X-RequestDigest": digest, ...extra }, body: body ? JSON.stringify(body) : undefined });
    if (!r.ok) throw new Error(method + " " + url + " → " + r.status + " " + (await r.text()).slice(0, 300));
    return r.status === 204 ? null : r.json();
  };
  const liste = (n) => "/_api/web/lists/getbytitle('" + n + "')";
  const log = [];
  const listeDa = async (n) => (await req("GET", "/_api/web/lists?$select=Title&$filter=Title eq '" + n + "'")).value.length > 0;
  const feldDa = async (l, f) => (await req("GET", liste(l) + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  const feld = async (l, name, xml) => {
    if (await feldDa(l, name)) { log.push(l + "." + name + " war schon da"); return; }
    await req("POST", liste(l) + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: xml, Options: 24 } }, true);
    if (!(await feldDa(l, name))) throw new Error(l + "." + name + " wurde mit anderem internen Namen angelegt – bitte melden");
    log.push(l + "." + name + " angelegt");
  };
  const A = "RG_Anleitungen";
  if (!(await listeDa(A))) {
    await req("POST", "/_api/web/lists", { __metadata: { type: "SP.List" }, Title: A, BaseTemplate: 100, Description: "Rundgang: Anleitungen für das ⓘ-Fenster" }, true);
    log.push(A + " angelegt");
  } else log.push(A + " war schon da");
  await feld(A, "Anleitung", '<Field Type="Note" DisplayName="Anleitung" Name="Anleitung" StaticName="Anleitung" NumLines="12" RichText="FALSE" UnlimitedLengthInDocumentLibrary="TRUE" />');
  await feld(A, "Aktiv", '<Field Type="Boolean" DisplayName="Aktiv" Name="Aktiv" StaticName="Aktiv"><Default>1</Default></Field>');
  await feld("RG_Pruefpunkte", "AnleitungID", '<Field Type="Number" DisplayName="AnleitungID" Name="AnleitungID" StaticName="AnleitungID"><Default>0</Default></Field>');
  const vorhanden = (await req("GET", liste(A) + "/items?$select=Id,Title")).value;
  let anlId = (vorhanden.find(x => x.Title === "ZZ Test Feuerlöscher prüfen") || {}).Id;
  if (!anlId && vorhanden.length === 0) {
    anlId = (await req("POST", liste(A) + "/items", { Title: "ZZ Test Feuerlöscher prüfen", Aktiv: true, Anleitung: "So prüfst du den Feuerlöscher:\n1. Prüfplakette suchen (meist seitlich am Behälter).\n2. Datum der nächsten Prüfung ablesen – liegt es in der Vergangenheit, ist der Punkt n.i.O.\n3. Plombe am Griff vorhanden und unbeschädigt?\n4. Manometer (falls vorhanden) im grünen Bereich?\n\nIm Kommentar das Prüfdatum notieren, z. B. „nächste Prüfung 03/2027“." })).Id;
    log.push("Testanleitung angelegt (ID " + anlId + ")");
  } else log.push(A + " hatte schon Einträge – keine Testanleitung angelegt");
  if (anlId) {
    const pp = (await req("GET", liste("RG_Pruefpunkte") + "/items?$select=Id,Title,AnleitungID&$filter=KategorieID eq 42")).value.filter(p => p.Title === "Prüfplakette Feuerlöscher lesbar");
    for (const p of pp) {
      if (!p.AnleitungID) { await req("POST", liste("RG_Pruefpunkte") + "/items(" + p.Id + ")", { AnleitungID: anlId }, false, { "IF-MATCH": "*", "X-HTTP-Method": "MERGE" }); log.push("Anleitung an Prüfpunkt " + p.Id + " gehängt"); }
    }
    if (!pp.length) log.push("Prüfpunkt „Prüfplakette Feuerlöscher lesbar“ nicht gefunden – Anleitung nirgends angehängt");
  }
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
