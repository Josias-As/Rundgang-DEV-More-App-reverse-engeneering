"""Erzeugt die Einbau-Seite (eine HTML-Datei) für die Baukasten-Pakete 1-6.

Je Paket: Kurzfassung, Schritte; je Property: Steuerelement, Property, Pfad, Text zum Kopieren,
Vorher/Nachher mit farbig markierten Änderungen, Vorher-Fassung für den Rückweg, Häkchen.
Aufruf: python3 -I werkzeuge/einbau_seite.py <Export-Schlüssel> [Ausgabedatei]
"""
import difflib
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rg  # noqa: E402
from baukasten_text import PAKET_TEXT  # noqa: E402
from doc_baukasten import yaml_block  # noqa: E402

ARB = os.path.join(rg.REPO, "arbeit", "2026-10-27_Baukasten")
TOK = re.compile(r'"(?:[^"]|"")*"|\'[^\']*\'|\s+|[A-Za-zÄÖÜäöüß_]\w*|\d+(?:,\d+)?|.', re.S)


def esc(s):
    return html.escape(s, quote=False)


def md_inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def md_block(zeilen):
    out = []
    i = 0
    while i < len(zeilen):
        z = zeilen[i]
        if z.strip() == "":
            i += 1
            continue
        if z.startswith("|"):
            rows = []
            while i < len(zeilen) and zeilen[i].startswith("|"):
                rows.append([c.strip() for c in zeilen[i].strip().strip("|").split(" | ")] if " | " in zeilen[i] else
                            [c.strip() for c in zeilen[i].strip().strip("|").split("|")])
                i += 1
            kopf, rest = rows[0], [r for r in rows[1:] if not all(set(c) <= set("-: ") for c in r)]
            for r in rest:
                if len(r) != len(kopf):
                    raise ValueError("Tabellenzeile mit falscher Spaltenzahl: %r" % r)
            t = "<div class='tabelle'><table><thead><tr>" + "".join("<th>%s</th>" % md_inline(c) for c in kopf) + "</tr></thead><tbody>"
            for r in rest:
                t += "<tr>" + "".join("<td>%s</td>" % md_inline(c) for c in r) + "</tr>"
            out.append(t + "</tbody></table></div>")
            continue
        if z.startswith("- "):
            items = []
            while i < len(zeilen) and zeilen[i].startswith("- "):
                items.append(zeilen[i][2:])
                i += 1
            out.append("<ul>" + "".join("<li>%s</li>" % md_inline(x) for x in items) + "</ul>")
            continue
        if re.match(r"\d+\. ", z):
            items = []
            while i < len(zeilen) and re.match(r"\d+\. ", zeilen[i]):
                items.append(re.sub(r"^\d+\. ", "", zeilen[i]))
                i += 1
            out.append("<ol>" + "".join("<li>%s</li>" % md_inline(x) for x in items) + "</ol>")
            continue
        out.append("<p>%s</p>" % md_inline(z))
        i += 1
    return "\n".join(out)


def pfad(app, d, ctl):
    if ctl == "App":
        return "App (in der Strukturansicht ganz oben)"
    if ctl in app.screen and app.typ.get(ctl) == "Screen":
        return "Bildschirm " + ctl
    kette = [ctl]
    cur = ctl
    while True:
        if cur in app.eltern:
            cur = app.eltern[cur]
        elif cur in d["neue_controls"]:
            cur = d["neue_controls"][cur]["eltern"]
        else:
            break
        kette.append(cur)
    return " › ".join(reversed(kette))


def zeilen_html(tokens):
    """tokens: Liste (text, flag). Liefert Zeilen als Liste (html, hat_aenderung)."""
    zeilen, cur, ch = [], [], False
    for text, flag in tokens:
        teile = text.split("\n")
        for k, t in enumerate(teile):
            if k > 0:
                zeilen.append(("".join(cur), ch))
                cur, ch = [], False
            if t:
                if flag:
                    cur.append("<span class='%s'>%s</span>" % (flag, esc(t)))
                    ch = True
                else:
                    cur.append(esc(t))
    zeilen.append(("".join(cur), ch))
    return zeilen


def eingeklappt(zeilen, kontext=1):
    n = len(zeilen)
    behalten = [False] * n
    for i, (_, c) in enumerate(zeilen):
        if c:
            for j in range(max(0, i - kontext), min(n, i + kontext + 1)):
                behalten[j] = True
    out, i = [], 0
    while i < n:
        if behalten[i] or n <= 4:
            out.append("<span class='z'>%s</span>" % (zeilen[i][0] or "&nbsp;"))
            i += 1
        else:
            j = i
            while j < n and not behalten[j]:
                j += 1
            out.append("<span class='z skip'>⋯ %d Zeilen unverändert ⋯</span>" % (j - i))
            i = j
    return "".join(out)


def vergleich(vorher, nachher):
    a, b = TOK.findall(vorher), TOK.findall(nachher)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ta, tb = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            ta += [(x, "") for x in a[i1:i2]]
            tb += [(x, "") for x in b[j1:j2]]
        else:
            ta += [(x, "del") for x in a[i1:i2]]
            tb += [(x, "ins") for x in b[j1:j2]]
    za, zb = zeilen_html(ta), zeilen_html(tb)
    return za, zb


def kopierblock(text, sprache=""):
    return ("<div class='kopier'><div class='kopfzeile'><button type='button' class='kopieren'>Kopieren</button>"
            "<span class='info'></span></div><pre class='text' tabindex='0'>%s</pre></div>" % esc(text))


def property_block(app, d, bid, ctl, prop, vorher_de, nachher_de, standard=False, neu=False):
    h = ["<article class='prop' id='%s'>" % bid,
         "<div class='kopf'><label class='haken'><input type='checkbox' data-key='%s'><span>eingefügt</span></label>"
         "<div class='ziel'><div><span class='etikett'>Steuerelement</span> <code class='gross'>%s</code></div>"
         "<div><span class='etikett'>Property</span> <code class='gross'>%s</code></div>"
         "<div class='pfad'><span class='etikett'>Pfad</span> %s</div></div></div>" % (bid, esc(ctl), esc(prop), esc(pfad(app, d, ctl))),
         "<div class='schritt'><span class='nr'>1</span> Diesen Text kopieren und die ganze Property ersetzen (Strg+A, Strg+V)</div>",
         kopierblock(nachher_de)]
    if neu:
        h.append("<div class='schritt'><span class='nr'>2</span> Neue Property – vorher stand nichts Eigenes drin.</div>")
    else:
        h.append("<div class='schritt'><span class='nr'>2</span> Das ändert sich <span class='legende'><span class='del'>entfernt</span> <span class='ins'>neu</span></span></div>")
        if standard:
            h.append("<div class='hinweis'>Vorher: Standardwert, nichts Eigenes eingetragen (<code>%s</code>).</div>" % esc(vorher_de))
            h.append("<div class='pane'><div class='panetitel'>Nachher</div><pre class='diff'><span class='z'><span class='ins'>%s</span></span></pre></div>" % esc(nachher_de))
        else:
            za, zb = vergleich(vorher_de, nachher_de)
            vor = eingeklappt(za) if any(c for _, c in za) else "<span class='z skip'>nichts entfernt, nur ergänzt</span>"
            h.append("<div class='pane'><div class='panetitel'>Vorher</div><pre class='diff'>%s</pre></div>" % vor)
            h.append("<div class='pane'><div class='panetitel'>Nachher</div><pre class='diff'>%s</pre></div>" % eingeklappt(zb))
        h.append("<details class='rueck'><summary>Vorher-Fassung zum Zurückkopieren (Rückweg)</summary>%s</details>" % kopierblock(vorher_de))
    h.append("</article>")
    return "\n".join(h)


def paket_html(app, d, p, nr):
    t = PAKET_TEXT[nr]
    schritte = {s["nr"] for s in t["schritte"]}
    for c in p["props"]:
        if c["schritt"] not in schritte:
            raise SystemExit("Property %s hat Schritt %s, der im Text fehlt" % (c["key"], c["schritt"]))
    for name in p["neu"]:
        if d["neue_controls"][name]["eltern"] in d["neue_controls"]:
            continue
        if not any(name in s.get("yaml", []) or name in s.get("einzeln", []) for s in t["schritte"]):
            raise SystemExit("Neues Steuerelement %s fehlt im Text" % name)
    h = ["<section class='paket' id='paket-%d' hidden>" % nr,
         "<h2>Paket %d · %s</h2>" % (nr, esc(t["titel"])),
         "<div class='kurz'><h3>Kurzfassung</h3><ul>" + "".join("<li>%s</li>" % md_inline(x) for x in t["kurz"]) + "</ul></div>",
         "<div class='voraus'><h3>Voraussetzungen</h3><ul>" + "".join("<li>%s</li>" % md_inline(x) for x in t["voraus"]) + "</ul></div>"]
    for s in t["schritte"]:
        sid = "p%d-s%s" % (nr, s["nr"])
        props = [c for c in p["props"] if c["schritt"] == s["nr"]]
        h.append("<section class='schrittkarte' id='%s'><h3><span class='snr'>%s</span> %s</h3>" % (sid, esc(s["nr"]), esc(s["titel"])))
        if s.get("text"):
            h.append("<div class='text'>%s</div>" % md_block(s["text"]))
        for c in props:
            key = c["key"]
            ctl, prop = key.split(".", 1)
            nachher = rg.to_de(c["nachher"])
            if c.get("standard"):
                h.append(property_block(app, d, "%s-%s" % (sid, key), ctl, prop, c["vorher"], nachher, standard=True))
            else:
                vorher = rg.to_de(rg.ohne_kommentare(c["vorher"]))
                h.append(property_block(app, d, "%s-%s" % (sid, key), ctl, prop, vorher, nachher))
        for name in s.get("yaml", []):
            alle = d["neue_controls"]
            ziel = alle[name]["eltern"]
            h.append("<article class='prop' id='%s-%s'><div class='kopf'><label class='haken'><input type='checkbox' data-key='%s-%s'><span>eingefügt</span></label>"
                     "<div class='ziel'><div><span class='etikett'>Neues Steuerelement</span> <code class='gross'>%s</code></div>"
                     "<div class='pfad'><span class='etikett'>Vorher markieren</span> %s</div></div></div>"
                     "<div class='schritt'><span class='nr'>1</span> YAML kopieren, in der Strukturansicht das Ziel markieren, Strg+V</div>%s</article>"
                     % (sid, name, sid, name, esc(name), esc(pfad(app, d, ziel) if ziel not in app.screen or app.typ.get(ziel) != "Screen" else "Bildschirm " + ziel),
                        kopierblock("\n".join(yaml_block(name, alle[name], alle)))))
        for name in s.get("einzeln", []):
            info = d["neue_controls"][name]
            for k, v in info["props"].items():
                h.append(property_block(app, d, "%s-%s.%s" % (sid, name, k), name, k, "", rg.to_de(v), neu=True))
        if s.get("pruefen"):
            h.append("<div class='pruefen'><strong>Prüfen nach dem Schritt</strong><ul>%s</ul></div>" % "".join("<li>%s</li>" % md_inline(x) for x in s["pruefen"]))
        if not props and not s.get("yaml") and not s.get("einzeln"):
            h.append("<label class='haken schritthaken'><input type='checkbox' data-key='%s'><span>erledigt</span></label>" % sid)
        h.append("</section>")
    h.append("<section class='schrittkarte test'><h3>Test</h3><div class='text'>%s</div></section>" % md_block(t["test"]))
    h.append("<section class='schrittkarte rueckweg'><h3>Rückweg</h3><div class='text'>%s</div></section>" % md_block(t["rueck"]))
    h.append("</section>")
    return "\n".join(h)


CSS = r"""
:root{
  --bg:#f6f6f2; --fg:#1d2024; --mut:#5d636c; --karte:#ffffff; --rand:#d9dbd6; --akzent:#1f3fae; --akzent-fg:#ffffff;
  --code-bg:#eef0ec; --ok:#17613a; --ok-bg:#dcf1e3; --del-bg:#fbd9d4; --del-fg:#8a1f13; --ins-bg:#cdeed8; --ins-fg:#0d5230;
  --warn-bg:#fff3d6; --warn-fg:#6b4a00;
  --sans:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif; --mono:"IBM Plex Mono",ui-monospace,Consolas,"Courier New",monospace;
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --bg:#14161a; --fg:#e6e8eb; --mut:#9aa1ab; --karte:#1c1f25; --rand:#333842; --akzent:#8aa2ff; --akzent-fg:#10142b;
  --code-bg:#23272f; --ok:#7fd6a0; --ok-bg:#16301f; --del-bg:#4a1f1b; --del-fg:#ffb4aa; --ins-bg:#16402a; --ins-fg:#a8ecc0;
  --warn-bg:#3a2e10; --warn-fg:#f1d58a; color-scheme:dark}}
:root[data-theme="dark"]{
  --bg:#14161a; --fg:#e6e8eb; --mut:#9aa1ab; --karte:#1c1f25; --rand:#333842; --akzent:#8aa2ff; --akzent-fg:#10142b;
  --code-bg:#23272f; --ok:#7fd6a0; --ok-bg:#16301f; --del-bg:#4a1f1b; --del-fg:#ffb4aa; --ins-bg:#16402a; --ins-fg:#a8ecc0;
  --warn-bg:#3a2e10; --warn-fg:#f1d58a; color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:15px/1.55 var(--sans);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:0 64px}
.wrap{max-width:860px;margin:0 auto}
header.top{padding:14px 0 10px}
.leiste{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--rand);display:flex;align-items:center;gap:10px}
.leiste .fortschritt{flex:1;margin:0;min-width:0}
body::before{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}
h1{font-size:20px;margin:0 0 2px;letter-spacing:.01em}
.sub{color:var(--mut);font-size:13px;margin:0 0 10px}
.fortschritt{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.balken{flex:1;height:8px;background:var(--rand);border-radius:4px;overflow:hidden}
.balken>i{display:block;height:100%;width:0;background:var(--akzent)}
.fortschritt .zahl{font-variant-numeric:tabular-nums;font-size:13px;color:var(--mut);min-width:78px;text-align:right}
nav.tabs{display:flex;gap:6px;flex-wrap:wrap}
nav.tabs button{font:inherit;font-size:13px;border:1px solid var(--rand);background:var(--karte);color:var(--fg);padding:6px 10px;border-radius:6px;cursor:pointer;font-variant-numeric:tabular-nums}
nav.tabs button[aria-current="true"]{background:var(--akzent);color:var(--akzent-fg);border-color:var(--akzent)}
nav.tabs button .t{display:block;font-size:11px;opacity:.8}
.warnung{background:var(--warn-bg);color:var(--warn-fg);border-radius:6px;padding:10px 12px;margin:14px 0;font-size:14px}
h2{font-size:21px;margin:22px 0 8px;text-wrap:balance}
h3{font-size:16px;margin:0 0 8px;text-wrap:balance}
.kurz,.voraus{margin:10px 0}
.kurz ul,.voraus ul,.text ul{padding-left:20px;margin:6px 0}
.kurz li,.voraus li{margin:3px 0}
.schrittkarte{background:var(--karte);border:1px solid var(--rand);border-radius:8px;padding:14px 16px;margin:14px 0}
.snr{display:inline-block;font-family:var(--mono);font-size:13px;color:var(--akzent);margin-right:6px}
code{font-family:var(--mono);font-size:.92em;background:var(--code-bg);padding:1px 5px;border-radius:4px}
code.gross{font-size:14px;font-weight:600}
.prop{border:1px solid var(--rand);border-radius:8px;padding:12px;margin:12px 0;background:var(--bg)}
.prop.fertig{border-color:var(--ok);background:var(--ok-bg)}
.kopf{display:flex;gap:12px;align-items:flex-start;flex-wrap:wrap;margin-bottom:8px}
.haken{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--mut);cursor:pointer;white-space:nowrap}
.haken input{width:18px;height:18px;accent-color:var(--akzent)}
.ziel{flex:1;min-width:220px;display:grid;gap:2px}
.etikett{display:inline-block;min-width:96px;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut)}
.pfad{font-size:13px;color:var(--mut)}
.schritt{font-size:13px;color:var(--mut);margin:10px 0 4px}
.nr{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;border-radius:9px;background:var(--akzent);color:var(--akzent-fg);font-size:11px;margin-right:4px}
.kopier{border:1px solid var(--rand);border-radius:6px;overflow:hidden;background:var(--karte)}
.kopfzeile{display:flex;align-items:center;gap:10px;padding:6px 8px;border-bottom:1px solid var(--rand);background:var(--code-bg)}
button.kopieren{font:inherit;font-size:13px;font-weight:600;background:var(--akzent);color:var(--akzent-fg);border:0;border-radius:5px;padding:5px 12px;cursor:pointer}
button.kopieren.ok{background:var(--ok);color:var(--karte)}
.info{font-size:12px;color:var(--mut);font-variant-numeric:tabular-nums;min-width:0;overflow-wrap:anywhere}
pre{margin:0;font:12.5px/1.5 var(--mono);white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word}
pre.text{padding:10px;max-height:240px;overflow:auto}
.pane{margin:6px 0}
.panetitel{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mut);margin-bottom:2px}
pre.diff{padding:8px 10px;border:1px solid var(--rand);border-radius:6px;background:var(--karte)}
.z{display:block;min-height:1.5em}
.z.skip{color:var(--mut);font-style:italic}
.del{background:var(--del-bg);color:var(--del-fg);border-radius:2px;text-decoration:line-through;text-decoration-thickness:1px}
.ins{background:var(--ins-bg);color:var(--ins-fg);border-radius:2px;font-weight:600}
.legende{margin-left:8px;font-size:12px}
.legende .del,.legende .ins{padding:0 6px;text-decoration:none;font-weight:600}
.hinweis{font-size:13px;color:var(--mut);margin:4px 0}
details.rueck{margin-top:8px;font-size:13px}
details.rueck summary{cursor:pointer;color:var(--mut)}
.pruefen{margin-top:10px;font-size:14px;background:var(--code-bg);border-radius:6px;padding:8px 12px}
.tabelle{overflow-x:auto;margin:8px 0}
table{border-collapse:collapse;font-size:13.5px;min-width:100%}
th,td{border:1px solid var(--rand);padding:6px 8px;text-align:left;vertical-align:top}
th{background:var(--code-bg)}
td:first-child{white-space:nowrap}
.schritthaken{margin-top:8px}
.weiter{font:inherit;font-size:13px;border:1px solid var(--akzent);background:var(--karte);color:var(--akzent);padding:6px 10px;border-radius:6px;cursor:pointer;white-space:nowrap}
:focus-visible{outline:2px solid var(--akzent);outline-offset:2px}
@media (max-width:520px){.etikett{display:block}.ziel{min-width:0}}
"""

JS = r"""
(function(){
  var KEY='rundgang-einbau-v1', erledigt={};
  try{erledigt=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){erledigt={}}
  function speichern(){try{localStorage.setItem(KEY,JSON.stringify(erledigt))}catch(e){}}
  var tabs=document.querySelectorAll('nav.tabs button'), pakete=document.querySelectorAll('section.paket');
  function zeige(n){
    pakete.forEach(function(s){s.hidden = s.id!=='paket-'+n});
    tabs.forEach(function(b){b.setAttribute('aria-current', b.dataset.p===String(n)?'true':'false')});
    window.scrollTo(0,0);
  }
  function zaehle(){
    var alle=document.querySelectorAll('input[data-key]'), fertig=0;
    alle.forEach(function(c){ if(c.checked) fertig++;
      var p=c.closest('.prop'); if(p) p.classList.toggle('fertig', c.checked); });
    document.getElementById('zahl').textContent=fertig+' von '+alle.length;
    document.getElementById('balken').style.width=(alle.length? 100*fertig/alle.length:0)+'%';
    tabs.forEach(function(b){
      var s=document.getElementById('paket-'+b.dataset.p), cs=s.querySelectorAll('input[data-key]'), f=0;
      cs.forEach(function(c){if(c.checked)f++});
      b.querySelector('.t').textContent=f+'/'+cs.length;
    });
  }
  document.querySelectorAll('input[data-key]').forEach(function(c){
    c.checked=!!erledigt[c.dataset.key];
    c.addEventListener('change',function(){ if(c.checked) erledigt[c.dataset.key]=1; else delete erledigt[c.dataset.key]; speichern(); zaehle(); });
  });
  document.querySelectorAll('.kopier').forEach(function(k){
    var pre=k.querySelector('pre'), t=pre.textContent;
    var ende=t.replace(/\s+/g,' ').trim(); ende=ende.length>46?'…'+ende.slice(-46):ende;
    k.querySelector('.info').textContent=t.length+' Zeichen · endet mit: '+ende;
  });
  function auswaehlen(pre){var r=document.createRange(); r.selectNodeContents(pre); var s=window.getSelection(); s.removeAllRanges(); s.addRange(r);}
  document.addEventListener('click',function(e){
    var b=e.target.closest('button.kopieren'); if(!b) return;
    var pre=b.closest('.kopier').querySelector('pre'), t=pre.textContent;
    function fertig(txt){b.textContent=txt; b.classList.add('ok'); setTimeout(function(){b.textContent='Kopieren'; b.classList.remove('ok')},2200);}
    function notfall(){pre.style.maxHeight='none'; auswaehlen(pre); b.textContent='Markiert – Strg+C'; setTimeout(function(){b.textContent='Kopieren'},4000);}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(function(){fertig('Kopiert ✓')},notfall);}
    else notfall();
  });
  document.querySelectorAll('nav.tabs button').forEach(function(b){b.addEventListener('click',function(){location.hash='paket-'+b.dataset.p;});});
  document.getElementById('weiter').addEventListener('click',function(){
    var sec=document.querySelector('section.paket:not([hidden])'); if(!sec) return;
    var c=[].filter.call(sec.querySelectorAll('input[data-key]'),function(x){return !x.checked})[0];
    if(c){var z=c.closest('.prop')||c.closest('.schrittkarte'); z.scrollIntoView({behavior:'smooth',block:'start'});}
  });
  function route(){var m=/^#paket-([1-6])$/.exec(location.hash); zeige(m?m[1]:1);}
  window.addEventListener('hashchange',route); route(); zaehle();
})();
"""


def baue(app, d):
    pakete = [paket_html(app, d, p, p["nr"]) for p in d["pakete"]]
    tabs = "".join("<button type='button' data-p='%d'>Paket %d<span class='t'></span></button>" % (p["nr"], p["nr"]) for p in d["pakete"])
    kopf = ("<!-- Layout: ruhige Werkzeugseite, eine Spalte, Karten je Schritt, Kopierfelder in Mono, Änderungen rot/grün markiert -->")
    return """<title>Rundgang Einbau</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>%s</style>
%s
<div class="wrap">
<header class="top">
<h1>Rundgang Einbau</h1>
<p class="sub">Baukasten-Pakete 1–6 für „Rundgang DEV“ · erzeugt aus dem Export %s · nur der Reihe nach einfügen</p>
<nav class="tabs">%s</nav>
</header>
<div class="leiste"><div class="fortschritt"><div class="balken"><i id="balken"></i></div><span class="zahl" id="zahl"></span></div>
<button type="button" class="weiter" id="weiter">Nächster offener ↓</button></div>
<div class="warnung"><strong>Vor jedem Block:</strong> Steht in Studio in der Property etwas anderes als bei „Vorher“, nicht einfügen. Das heißt, die App hat sich seit dem Export verändert. Dann Steuerelement, Property und Inhalt an Claude schicken. Nach dem Einfügen prüfen, ob das Ende der Formel zu „endet mit“ passt (Zwischenablage kann alt sein). Haken und Fortschritt merkt sich nur dieser Browser.</div>
%s
</div>
<script>%s</script>
""" % (CSS, kopf, esc(d["export"].replace("_", " ")), tabs, "\n".join(pakete), JS)


def main():
    schluessel = sys.argv[1]
    ziel = sys.argv[2] if len(sys.argv) > 2 else os.path.join(rg.REPO, "pakete", "EINBAU_ASSISTENT.html")
    d = json.load(open(os.path.join(ARB, "bloecke.json"), encoding="utf-8"))
    if d["export"] != schluessel or d["simulation"]:
        raise SystemExit("bloecke.json passt nicht zum Export %s (oder ist Simulation) – baukasten.py zuerst laufen lassen" % schluessel)
    app = rg.App(schluessel)
    text = baue(app, d)
    open(ziel, "w", encoding="utf-8").write(text)
    print(ziel, len(text) // 1024, "KB")


if __name__ == "__main__":
    main()
