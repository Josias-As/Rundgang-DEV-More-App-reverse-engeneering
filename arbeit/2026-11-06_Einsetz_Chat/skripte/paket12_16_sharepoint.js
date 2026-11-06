// Paket 12+16, Schritt 1 (SharePoint) – 03.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht und ändert nichts.
// RG_Pruefpunkte: TextIO (Text), TextNIO (Text), NichtMessbar (Ja/Nein, Standard Nein)
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
  const L = "/_api/web/lists/getbytitle('RG_Pruefpunkte')";
  const log = [];
  const feldDa = async (f) => (await req("GET", L + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  const feld = async (name, xml) => {
    if (await feldDa(name)) { log.push(name + " war schon da"); return; }
    await req("POST", L + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: xml, Options: 24 } }, true);
    if (!(await feldDa(name))) throw new Error(name + " wurde mit anderem internen Namen angelegt – bitte melden");
    log.push(name + " angelegt");
  };
  await feld("TextIO", '<Field Type="Text" DisplayName="TextIO" Name="TextIO" StaticName="TextIO" />');
  await feld("TextNIO", '<Field Type="Text" DisplayName="TextNIO" Name="TextNIO" StaticName="TextNIO" />');
  await feld("NichtMessbar", '<Field Type="Boolean" DisplayName="NichtMessbar" Name="NichtMessbar" StaticName="NichtMessbar"><Default>0</Default></Field>');
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
