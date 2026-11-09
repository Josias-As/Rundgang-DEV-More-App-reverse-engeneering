// Paket 11, Schritt A1 (SharePoint) – 09.11.2026
// Ausführen: IMS+ öffnen → F12 → Konsole → einfügen → Enter. Legt nur an, was fehlt. Löscht nichts.
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
  const neueListe = async (n, beschr) => {
    if (await listeDa(n)) { log.push(n + " war schon da"); return; }
    await req("POST", "/_api/web/lists", { __metadata: { type: "SP.List" }, Title: n, BaseTemplate: 100, Description: beschr }, true);
    log.push(n + " angelegt");
  };
  const feldDa = async (l, f) => (await req("GET", liste(l) + "/fields?$select=InternalName&$filter=InternalName eq '" + f + "'")).value.length > 0;
  const feld = async (l, name, xml) => {
    if (await feldDa(l, name)) { log.push(l + "." + name + " war schon da"); return; }
    await req("POST", liste(l) + "/fields/createfieldasxml", { parameters: { __metadata: { type: "SP.XmlSchemaFieldCreationInformation" }, SchemaXml: xml, Options: 24 } }, true);
    if (!(await feldDa(l, name))) throw new Error(l + "." + name + " wurde mit anderem internen Namen angelegt – bitte melden");
    log.push(l + "." + name + " angelegt");
  };
  const text = (n) => '<Field Type="Text" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '" />';
  const note = (n) => '<Field Type="Note" DisplayName="' + n + '" Name="' + n + '" StaticName="' + n + '" NumLines="6" RichText="FALSE" />';
  await neueListe("RG_Pruefer", "Rundgang: Prüfer (Auswahl beim Start)");
  await feld("RG_Pruefer", "Email", text("Email"));
  await feld("RG_Pruefer", "Aktiv", '<Field Type="Boolean" DisplayName="Aktiv" Name="Aktiv" StaticName="Aktiv"><Default>1</Default></Field>');
  for (const f of ["Standort", "Adresse", "Auftraggeber"]) await feld("RG_Rundgaenge", f, text(f));
  await neueListe("RG_Unterschriften", "Rundgang: Unterschriften (Bild als Text)");
  await feld("RG_Unterschriften", "DurchfuehrungID", '<Field Type="Number" DisplayName="DurchfuehrungID" Name="DurchfuehrungID" StaticName="DurchfuehrungID" />');
  await feld("RG_Unterschriften", "Bild", note("Bild"));
  await feld("RG_Durchfuehrungen", "UnterschriftUrl", note("UnterschriftUrl"));
  await feld("RG_Durchfuehrungen", "UnterschriftName", text("UnterschriftName"));
  await feld("RG_Durchfuehrungen", "UnterschriftZeit", '<Field Type="DateTime" DisplayName="UnterschriftZeit" Name="UnterschriftZeit" StaticName="UnterschriftZeit" Format="DateTime" />');
  await feld("RG_Durchfuehrungen", "Geraetekonto", text("Geraetekonto"));
  console.log("FERTIG\n" + log.join("\n"));
})().catch(e => console.error("FEHLER: " + e.message + " – bitte diese Zeile an Claude schicken."));
