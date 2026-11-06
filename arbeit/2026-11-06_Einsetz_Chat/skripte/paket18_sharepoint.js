// Paket 18, Schritt A1 (SharePoint) – 06.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht nichts.
// 1) Liste RG_Zugangscodes (Code: Text, Hinweis: mehrzeilig nur Text, Aktiv: Ja/Nein Standard Ja) + 1 Testcode (nur wenn Liste leer)
// 2) RG_Pruefpunkte: ZugangscodeID (Zahl, Standard 0)
(async () => {
  const SITE = "https://technoformgroup.sharepoint.com/sites/IMSKonzept";
  const NM = "application/json;odata=nometadata", VB = "application/json;odata=verbose";
  const digest = (await (await fetch(SITE + "/_api/contextinfo", { method: "POST", headers: { Accept: NM } })).json()).FormDigestValue;
  const req = async (method, url, body, verbose) => {
    const t = verbose ? VB : NM;
    const r = await fetch(SITE + url, { method, headers: { Accept: t, "Content-Type": t, "X-RequestDigest": digest }, body: body ? JSON.stringify(body) : undefined });
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
  const A = "RG_Zugangscodes";
  if (!(await listeDa(A))) { await req("POST", "/_api/web/lists", { __metadata: { type: "SP.List" }, Title: A, BaseTemplate: 100, Description: "Rundgang: Bedien-Codes (keine echten Passwörter)" }, true); log.push(A + " angelegt"); }
  else log.push(A + " war schon da");
  await feld(A, "Code", '<Field Type="Text" DisplayName="Code" Name="Code" StaticName="Code" />');
  await feld(A, "Hinweis", '<Field Type="Note" DisplayName="Hinweis" Name="Hinweis" StaticName="Hinweis" NumLines="6" RichText="FALSE" />');
  await feld(A, "Aktiv", '<Field Type="Boolean" DisplayName="Aktiv" Name="Aktiv" StaticName="Aktiv"><Default>1</Default></Field>');
  await feld("RG_Pruefpunkte", "ZugangscodeID", '<Field Type="Number" DisplayName="ZugangscodeID" Name="ZugangscodeID" StaticName="ZugangscodeID"><Default>0</Default></Field>');
  if ((await req("GET", liste(A) + "/items?$select=Id")).value.length === 0) {
    const id = (await req("POST", liste(A) + "/items", { Title: "ZZ Test Bedienfeld Kältemaschine", Code: "1234", Hinweis: "ZZ Test – nur Bedien-Code, kein echtes Passwort.", Aktiv: true })).Id;
    log.push("Testcode angelegt (ID " + id + ")");
  } else log.push(A + " hatte schon Einträge – kein Testcode angelegt");
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
