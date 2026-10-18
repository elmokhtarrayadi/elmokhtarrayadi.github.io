"""Génère les pages du portfolio (accueil, conception, maintenance)."""
import os, math

BASE = "https://elmokhtarrayadi.github.io"
GH = "https://github.com/elmokhtarrayadi"

PROJECTS = {
    "conception": [
        dict(img="genou.webp", fit="contain", tools="CATIA V5 · Cinématique 4R · RDM · SimScale · Usinage",
             title="Genou prothétique polycentrique",
             desc="Conception complète d’un genou prothétique à quatre barres, du cahier des charges aux gammes d’usinage : synthèse cinématique, dimensionnement, CAO des pièces en Ti-6Al-4V et calcul éléments finis.",
             pts=["<b>452 g</b> pour l’assemblage (cible ≤ 900 g)",
                  "<b>S ≈ 2,4</b> en statique sous 4 000 N, <b>n ≈ 1,3</b> en fatigue",
                  "<b>21,7 mm</b> de migration du centre instantané de rotation"],
             links=[("Démo interactive", f"{BASE}/conception-genou-polycentrique/", True),
                    ("Dossier technique", f"{BASE}/conception-genou-polycentrique/dossier-technique.html", False),
                    ("Dépôt GitHub", f"{GH}/conception-genou-polycentrique", False)]),
        dict(img="engrenage.webp", fit="cover", tools="CATIA V5 · ANSYS · Fatigue · AGMA",
             title="Optimisation d’un engrenage à denture droite",
             desc="Réduction de la contrainte de flexion au pied de la dent : CAO paramétrique, calcul éléments finis validé par la méthode AGMA, puis comparaison de trois modifications de géométrie.",
             pts=["<b>−17 %</b> de contrainte au pied de la dent (1 008 → 834 MPa)",
                  "<b>+64 %</b> de durée de vie en fatigue",
                  "<b>0,015 %</b> d’écart entre simulation et calcul AGMA"],
             links=[("Démo interactive", f"{BASE}/optimisation-engrenage-denture-droite/", True),
                    ("Dépôt GitHub", f"{GH}/optimisation-engrenage-denture-droite", False)]),
        dict(img="aero.jpg", fit="cover", tools="CATIA V5 · Altair Inspire · PolyNURBS · Cura",
             title="Optimisation topologique d’une pièce aéronautique",
             desc="Allègement d’un support de porte de train d’atterrissage : optimisation topologique, reconstruction de la forme, plan d’expériences de fabrication additive et étude de coûts.",
             pts=["<b>55 g → 24 g</b> : −56 % de masse",
                  "<b>12 configurations</b> d’impression comparées",
                  "Analyse critique du résultat mécanique et prochaine itération"],
             links=[("Démo interactive", f"{BASE}/optimisation-topologique-aeronautique/", True),
                    ("Dépôt GitHub", f"{GH}/optimisation-topologique-aeronautique", False)]),
    ],
    "maintenance": [
        dict(img="iso.png", fit="contain", bg="#0f2531", tools="Audit · ISO 21001 · Ishikawa 5M · PDCA · KPI",
             title="Diagnostic qualité ISO 21001",
             desc="Diagnostic du système de management de la qualité d’une école d’ingénieurs : évaluation de la conformité, analyse des causes et plan d’amélioration chiffré.",
             pts=["<b>72 critères</b> évalués sur les 7 chapitres d’exigences",
                  "<b>15 causes</b> analysées, <b>14 actions</b> avec responsable, délai et KPI",
                  "Priorité identifiée : planification (<b>46 %</b> de conformité)"],
             links=[("Démo interactive", f"{BASE}/diagnostic-iso-21001/", True),
                    ("Dépôt GitHub", f"{GH}/diagnostic-iso-21001", False)]),
    ],
}
SKILLS = {
    "conception": [("CAO & mise en plan", "CATIA V5 (paramétrique), SpaceClaim", "Genou · Engrenage · Optimisation topologique"),
                   ("Calcul de structures", "RDM, ANSYS, SimScale, Altair Inspire, fatigue", "Genou · Engrenage · Optimisation topologique"),
                   ("Dimensionnement d’organes", "Engrenages (Lewis, AGMA), liaisons, matériaux", "Engrenage · Genou"),
                   ("Cinématique", "Mécanisme 4 barres, CIR, Python / MATLAB", "Genou"),
                   ("Optimisation & fabrication", "Optimisation topologique, Cura, gammes d’usinage, coûts", "Optimisation topologique · Genou"),
                   ("Analyse fonctionnelle", "APTE, SysML, cahier des charges", "Genou")],
    "maintenance": [("Analyse des causes", "Ishikawa 5M, analyse des écarts, priorisation", "Diagnostic ISO 21001"),
                    ("Management de la qualité", "ISO 21001, ISO 9001, audit, KPI", "Diagnostic ISO 21001"),
                    ("Amélioration continue", "PDCA, plan d’action, tableaux de bord", "Diagnostic ISO 21001")],
}
ARROW = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h12M11 5l5 5-5 5"/></svg>'


def head(title, desc, root, url, image):
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/img/{image}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%230f2531'/%3E%3Ctext x='16' y='21' font-family='Arial' font-weight='700' font-size='13' fill='%236ad8cc' text-anchor='middle'%3EER%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/style.css">
</head>'''


def nav(root, active):
    item = lambda href, label, key, cls: f'<li><a href="{href}" class="{cls}{" on" if active == key else ""}">{label}</a></li>'
    return f'''<header class="nav"><div class="wrap">
  <a class="brand" href="{root}"><i>ER</i><span>Elmokhtar Rayadi</span></a>
  <ul>{item(root, "Accueil", "home", "")}{item(root + "conception/", "Conception", "c", "c")}{item(root + "maintenance/", "<span class=\"long\">Maintenance &amp; Qualité</span><span class=\"short\">Maintenance</span>", "m", "m")}<li><a href="{GH}">GitHub</a></li></ul>
</div></header>'''


FOOT = lambda root: f'''<footer class="wrap">Elmokhtar Rayadi · Élève ingénieur en Génie Mécanique des Systèmes Industriels · <a href="{GH}">github.com/elmokhtarrayadi</a></footer>
<script>
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('in');io.unobserve(e.target)}}}}),{{threshold:.12}});
document.querySelectorAll('.reveal').forEach((el,i)=>{{el.style.transitionDelay=(i%4)*80+'ms';io.observe(el)}});
</script>
</body></html>'''


def gear_svg(col):
    n, r = 12, 34
    d = ""
    for i in range(n * 2):
        a0, a1 = math.pi * i / n, math.pi * (i + 1) / n
        R = r if i % 2 == 0 else r * 0.8
        d += f"{'M' if i == 0 else 'L'}{R*math.cos(a0+0.06):.1f} {R*math.sin(a0+0.06):.1f} L{R*math.cos(a1-0.06):.1f} {R*math.sin(a1-0.06):.1f} "
    g = lambda cx, cy, s, dur, dirn: f'<g transform="translate({cx} {cy}) scale({s})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{360*dirn}" dur="{dur}s" repeatCount="indefinite"/><path d="{d}Z" fill="none" stroke="{col}" stroke-width="{2.4/s:.2f}" stroke-linejoin="round"/><circle r="10" fill="none" stroke="{col}" stroke-width="{2.4/s:.2f}"/></g></g>'
    return f'<svg width="190" height="90" viewBox="0 0 190 90">{g(48,45,1.15,12,1)}{g(122,38,0.78,12*0.78/1.15,-1)}</svg>'


def bath_svg(col):
    pts = []
    for k in range(61):
        u = k / 60; y = 0.85 * math.exp(-u / 0.07) + 0.12 + 0.9 * u ** 6
        pts.append(f"{10+170*u:.1f} {80-62*y/1.05:.1f}")
    d = "M" + " L".join(pts)
    return f'''<svg width="190" height="90" viewBox="0 0 190 90"><path d="M10 8 V82 H186" fill="none" stroke="#6f939c" stroke-width="1.2"/>
<path id="bt" d="{d}" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-dasharray="260" stroke-dashoffset="260"><animate attributeName="stroke-dashoffset" values="260;0;0;260" keyTimes="0;.45;.9;1" dur="6s" repeatCount="indefinite"/></path>
<circle r="5" fill="#e8f6f5" stroke="{col}" stroke-width="2.5"><animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;1;0" keyTimes="0;.45;.9;1" calcMode="linear"><mpath href="#bt"/></animateMotion></circle></svg>'''


def index():
    return head("Elmokhtar Rayadi — Portfolio d’ingénierie mécanique",
                "Portfolio d’Elmokhtar Rayadi, élève ingénieur en génie mécanique : conception et simulation, maintenance, fiabilité et qualité.",
                "", BASE + "/", "engrenage.webp") + f'''
<body>
{nav("", "home")}
<main class="wrap">
  <section class="hero reveal"><img src="assets/hero.svg" alt="Elmokhtar Rayadi — Je conçois, je simule, j’optimise" width="1280" height="440"></section>
  <section class="intro reveal">
    <h1>Élève ingénieur · Génie Mécanique des Systèmes Industriels</h1>
    <p>Mes projets sont rangés en deux univers. Choisissez celui qui correspond à votre poste.</p>
  </section>
  <section class="doors">
    <a class="door c reveal" href="conception/">
      <div class="art">{gear_svg("#6ad8cc")}</div>
      <small>UNIVERS 01</small>
      <h2>Conception &amp; Simulation</h2>
      <p>Je conçois des pièces et des mécanismes, je les calcule et je les optimise : CATIA V5, ANSYS, SimScale, Altair Inspire.</p>
      <div class="nums"><div><b>−17 %</b><span>contrainte au pied de dent</span></div><div><b>−56 %</b><span>masse pièce aéronautique</span></div><div><b>S = 2,4</b><span>sécurité du genou</span></div></div>
      <span class="go">Voir les 3 projets {ARROW}</span>
    </a>
    <a class="door m reveal" href="maintenance/">
      <div class="art">{bath_svg("#f2b45a")}</div>
      <small>UNIVERS 02</small>
      <h2>Maintenance, Fiabilité &amp; Qualité</h2>
      <p>J’analyse les défaillances, je fiabilise les équipements et j’améliore les processus : AMDEC, fiabilité, ISO, PDCA.</p>
      <div class="nums"><div><b>72</b><span>critères ISO évalués</span></div><div><b>15</b><span>causes analysées</span></div><div><b>14</b><span>actions d’amélioration</span></div></div>
      <span class="go">Voir les projets {ARROW}</span>
    </a>
  </section>
</main>
{FOOT("")}'''


def univers(key):
    c = key == "conception"
    root = "../"
    other = ("maintenance/", "Maintenance, Fiabilité &amp; Qualité", "var(--amber)") if c else ("conception/", "Conception &amp; Simulation", "var(--teal)")
    title = "Conception & Simulation" if c else "Maintenance, Fiabilité & Qualité"
    cards = ""
    for p in PROJECTS[key]:
        lk = "".join(f'<a class="btn{" p" if prim else ""}" href="{u}">{l}{" " + ARROW if prim else ""}</a>' for l, u, prim in p["links"])
        cards += f'''
    <article class="proj reveal">
      <a class="pic" href="{p["links"][0][1]}" style="background:{p.get('bg', '#fff')}"><img src="{root}assets/img/{p["img"]}" alt="{p["title"]}" loading="lazy" style="object-fit:{p["fit"]}"></a>
      <div class="body">
        <div class="tools">{p["tools"]}</div>
        <h3>{p["title"]}</h3>
        <p>{p["desc"]}</p>
        <ul>{"".join(f"<li>{x}</li>" for x in p["pts"])}</ul>
        <div class="btns">{lk}</div>
      </div>
    </article>'''
    soon = "" if c else '''
    <div class="soon reveal"><i>🔧</i><div><b>Projets de maintenance et de fiabilité en cours de mise en ligne.</b><br>AMDEC, analyses de fiabilité et plans de maintenance arrivent bientôt sur cette page.</div></div>'''
    rows = "".join(f"<tr><td>{a}</td><td>{b}</td><td>{d}</td></tr>" for a, b, d in SKILLS[key])
    n = len(PROJECTS[key])
    return head(f"{title} — Elmokhtar Rayadi",
                ("Projets de conception mécanique et de simulation : genou polycentrique, engrenage, optimisation topologique." if c
                 else "Projets de maintenance, fiabilité et qualité : diagnostic ISO 21001, analyse des causes, amélioration continue."),
                root, f"{BASE}/{key}/", "engrenage.webp" if c else "iso.png") + f'''
<body class="{"page-c" if c else "page-m"}">
{nav(root, "c" if c else "m")}
<main class="wrap">
  <section class="uhead reveal"><img src="{root}assets/univers-{key}.svg" alt="{title}" width="1280" height="230"></section>
  <section class="metrics reveal"><img src="{root}assets/metrics-{key}.svg" alt="Chiffres clés — {title}" width="1280" height="190"></section>
  <div class="section-title"><h2>Projets</h2><span>{n} projet{"s" if n > 1 else ""} · démo interactive en ligne pour chacun</span></div>
  <section class="projects">{cards}{soon}
  </section>
  <div class="section-title"><h2>Compétences démontrées</h2></div>
  <table class="skills reveal"><thead><tr><th>Compétence</th><th>Outils et méthodes</th><th>Projets</th></tr></thead><tbody>{rows}</tbody></table>
  <a class="switch reveal" href="{root}{other[0]}" style="--other:{other[2]}"><div><small>VOIR AUSSI</small><strong>{other[1]}</strong></div>{ARROW}</a>
</main>
{FOOT(root)}'''


os.makedirs("conception", exist_ok=True); os.makedirs("maintenance", exist_ok=True)
open("index.html", "w").write(index())
open("conception/index.html", "w").write(univers("conception"))
open("maintenance/index.html", "w").write(univers("maintenance"))
open("404.html", "w").write(index().replace('<title>Elmokhtar Rayadi', '<base href="/"><title>Elmokhtar Rayadi'))
print("ok")
