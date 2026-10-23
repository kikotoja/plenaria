"""Láminas científicas de la web, dibujadas aquí mismo en SVG (sin imágenes de terceros).

Una por área, al estilo de los grabados de las revistas médicas antiguas: trazo de tinta, tramas
de líneas y punteado, con un solo color de realce. El trazo usa currentColor y el realce las clases
.ac (relleno) y .acs (trazo), así que siguen el modo claro u oscuro de la página.
"""
import math
import random

W, H = 480, 360


def f(x):
    return f"{x:.1f}".rstrip("0").rstrip(".")


def pts(ps):
    return " ".join(f"{f(x)},{f(y)}" for x, y in ps)


def suave(ps, cerrado=False):
    """Curva Catmull-Rom que pasa por los puntos, como path SVG."""
    n = len(ps)
    if n < 3:
        return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in ps)
    d = f"M{f(ps[0][0])} {f(ps[0][1])}"
    if cerrado:
        cuatro = [(ps[i - 1], ps[i], ps[(i + 1) % n], ps[(i + 2) % n]) for i in range(n)]
    else:
        p = [ps[0]] + ps + [ps[-1]]
        cuatro = [(p[i], p[i + 1], p[i + 2], p[i + 3]) for i in range(n - 1)]
    for p0, p1, p2, p3 in cuatro:
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + (" Z" if cerrado else "")


def blob(cx, cy, r, rng, n=14, irr=0.12, ry=None):
    ry = ry or r
    ps = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 1 + rng.uniform(-irr, irr)
        ps.append((cx + math.cos(a) * r * k, cy + math.sin(a) * ry * k))
    return suave(ps, True)


def tramas(p):
    return (f'<defs>'
            f'<pattern id="{p}-h" width="3.2" height="3.2" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><line x1="0" y1="0" x2="0" y2="3.2" stroke="currentColor" stroke-width=".7"/></pattern>'
            f'<pattern id="{p}-x" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(-50)"><line x1="0" y1="0" x2="0" y2="3" stroke="currentColor" stroke-width=".6"/></pattern>'
            f'<pattern id="{p}-f" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(40)"><line x1="0" y1="0" x2="0" y2="5" stroke="currentColor" stroke-width=".45"/></pattern>'
            f'</defs>')


def punteado(rng, dentro, n, caja, r=(0.5, 1.1), cls=""):
    x0, y0, x1, y1 = caja
    out = []
    intentos = 0
    while len(out) < n and intentos < n * 20:
        intentos += 1
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        if dentro(x, y):
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(rng.uniform(*r))}"{cls}/>')
    return "".join(out)


def svg(p, cuerpo, titulo):
    return (f'<svg class="lamina-svg" viewBox="0 0 {W} {H}" role="img" aria-label="{titulo}" '
            f'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">'
            f'{tramas(p)}{cuerpo}</svg>')


# ---------------------------------------------------------------- I. VIH
def vih():
    rng = random.Random(7)
    p = "l-vih"
    cx, cy, R = 240, 182, 118
    o = []
    # glicoproteínas de la envoltura (trímeros)
    for i in range(15):
        a = 2 * math.pi * i / 15 + rng.uniform(-.08, .08)
        x1, y1 = cx + math.cos(a) * R, cy + math.sin(a) * R
        x2, y2 = cx + math.cos(a) * (R + 20), cy + math.sin(a) * (R + 20)
        o.append(f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke-width="2.4"/>')
        for k in (-1, 0, 1):
            b = a + k * .085
            hx, hy = cx + math.cos(b) * (R + 27 + (k == 0) * 3), cy + math.sin(b) * (R + 27 + (k == 0) * 3)
            o.append(f'<circle cx="{f(hx)}" cy="{f(hy)}" r="5.2" fill="url(#{p}-h)" stroke-width="1"/>')
    # bicapa lipídica
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" stroke-width="1.6"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R - 8}" stroke-width="1.1"/>')
    for i in range(140):
        a = 2 * math.pi * i / 140
        o.append(f'<line x1="{f(cx + math.cos(a) * (R - 1.5))}" y1="{f(cy + math.sin(a) * (R - 1.5))}" x2="{f(cx + math.cos(a) * (R - 6.5))}" y2="{f(cy + math.sin(a) * (R - 6.5))}" stroke-width=".5"/>')
    # matriz
    for i in range(46):
        a = 2 * math.pi * i / 46
        o.append(f'<circle cx="{f(cx + math.cos(a) * (R - 15))}" cy="{f(cy + math.sin(a) * (R - 15))}" r="3" stroke-width=".8"/>')
    # cápside cónica
    ang = math.radians(-28)
    def rot(x, y):
        return (cx + 6 + x * math.cos(ang) - y * math.sin(ang), cy + 4 + x * math.sin(ang) + y * math.cos(ang))
    cono = [rot(-62, -14), rot(-58, -24), rot(-40, -30), rot(30, -48), rot(56, -44), rot(66, -24), rot(66, 24), rot(56, 44), rot(30, 48), rot(-40, 30), rot(-58, 24), rot(-62, 14)]
    o.append(f'<path d="{suave(cono, True)}" fill="url(#{p}-x)" stroke-width="2"/>')
    hueco = [rot(-50, -8), rot(-36, -18), rot(30, -34), rot(52, -26), rot(56, 0), rot(52, 26), rot(30, 34), rot(-36, 18), rot(-50, 8)]
    o.append(f'<path d="{suave(hueco, True)}" fill="var(--papel)" stroke-width=".9"/>')
    # dos hebras de ARN
    for desf, sw in ((0, 1.4), (math.pi, 1.4)):
        ps = [rot(-40 + t * 9, math.sin(t * .9 + desf) * (6 + t * 1.5)) for t in range(11)]
        o.append(f'<path d="{suave(ps)}" stroke-width="{sw}"/>')
    # enzimas (realce)
    for x, y in ((-18, 10), (8, -14), (26, 16), (40, -6)):
        X, Y = rot(x, y)
        o.append(f'<circle class="ac" cx="{f(X)}" cy="{f(Y)}" r="3.6" stroke="none"/>')
    return svg(p, "".join(o), "Virión del VIH en corte")


# ---------------------------------------------------------------- II. Cardiovascular
def cardio():
    rng = random.Random(11)
    p = "l-car"
    cx, cy, R = 240, 180, 128
    o = []
    # núcleo lipídico punteado
    o.append(punteado(rng, lambda x, y: (x - cx) ** 2 + (y - cy) ** 2 < (R - 26) ** 2, 900, (cx - R, cy - R, cx + R, cy + R), (.5, 1.25)))
    # gotas de colesterol esterificado (anillos)
    for _ in range(9):
        a, d = rng.uniform(0, 2 * math.pi), rng.uniform(0, R - 50)
        o.append(f'<circle cx="{f(cx + math.cos(a) * d)}" cy="{f(cy + math.sin(a) * d)}" r="{f(rng.uniform(5, 9))}" stroke-width=".8"/>')
    # monocapa de fosfolípidos: cabeza + dos colas
    n = 74
    for i in range(n):
        a = 2 * math.pi * i / n
        hx, hy = cx + math.cos(a) * R, cy + math.sin(a) * R
        o.append(f'<circle cx="{f(hx)}" cy="{f(hy)}" r="4.3" fill="url(#{p}-h)" stroke-width="1"/>')
        for k in (-.018, .018):
            b = a + k
            ps = [(cx + math.cos(b) * (R - 5), cy + math.sin(b) * (R - 5)),
                  (cx + math.cos(b + .008) * (R - 12), cy + math.sin(b + .008) * (R - 12)),
                  (cx + math.cos(b - .006) * (R - 19), cy + math.sin(b - .006) * (R - 19))]
            o.append(f'<path d="{suave(ps)}" stroke-width=".7"/>')
    # apolipoproteína B: cinta ancha que abraza la partícula
    ps1 = [(cx + math.cos(a) * (R + 9 + 3 * math.sin(a * 7)), cy + math.sin(a) * (R + 9 + 3 * math.sin(a * 7))) for a in [math.radians(t) for t in range(150, 395, 15)]]
    ps2 = [(cx + math.cos(a) * (R + 17 + 3 * math.sin(a * 7)), cy + math.sin(a) * (R + 17 + 3 * math.sin(a * 7))) for a in [math.radians(t) for t in range(150, 395, 15)]]
    o.append(f'<path d="{suave(ps1)} L{f(ps2[-1][0])} {f(ps2[-1][1])} {suave(ps2[::-1])[1:]} Z" fill="url(#{p}-x)" stroke-width="1.3"/>')
    # apoC-III: pequeña hélice de realce
    a0 = math.radians(95)
    hel = []
    for t in range(0, 26):
        a = a0 + t * .022
        r = R + 12 + 5 * math.sin(t * 1.3)
        hel.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    o.append(f'<path class="acs" d="{suave(hel)}" stroke-width="3.2"/>')
    a = math.radians(60)
    o.append(f'<circle class="ac" cx="{f(cx + math.cos(a) * (R + 13))}" cy="{f(cy + math.sin(a) * (R + 13))}" r="5" stroke="none"/>')
    return svg(p, "".join(o), "Lipoproteína rica en triglicéridos en corte")


# ---------------------------------------------------------------- III. Neurología
def neuro():
    rng = random.Random(3)
    p = "l-neu"
    o = []
    sx, sy = 168, 178

    def rama(x, y, ang, largo, grosor, nivel):
        ps = [(x, y)]
        a = ang
        for _ in range(4):
            a += rng.uniform(-.28, .28)
            x += math.cos(a) * largo / 4
            y += math.sin(a) * largo / 4
            ps.append((x, y))
        o.append(f'<path d="{suave(ps)}" stroke-width="{f(grosor)}"/>')
        if nivel > 0:
            for d in (-1, 1):
                rama(x, y, a + d * rng.uniform(.3, .6), largo * rng.uniform(.6, .78), max(.5, grosor * .62), nivel - 1)
        else:
            for _ in range(2):
                o.append(f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x + rng.uniform(-4, 4))}" y2="{f(y + rng.uniform(-4, 4))}" stroke-width=".5"/>')

    for ang in (-2.6, -1.9, -1.2, 2.0, 2.7, 3.3, 1.35):
        rama(sx + math.cos(ang) * 24, sy + math.sin(ang) * 24, ang, rng.uniform(36, 48), 3.4, 3)
    # cuerpo celular
    o.append(f'<path d="{blob(sx, sy, 30, rng, 9, .14)}" fill="url(#{p}-f)" stroke-width="1.8"/>')
    o.append(f'<circle cx="{sx - 2}" cy="{sy - 1}" r="12" fill="var(--papel)" stroke-width="1.2"/>')
    o.append(f'<circle class="ac" cx="{sx + 1}" cy="{sy - 3}" r="4" stroke="none"/>')
    o.append(punteado(rng, lambda x, y: 12 ** 2 < (x - sx) ** 2 + (y - sy) ** 2 < 25 ** 2, 70, (sx - 30, sy - 30, sx + 30, sy + 30), (.5, .9)))
    # axón con vainas de mielina
    x, y = sx + 30, sy + 4
    o.append(f'<path d="M{x} {y} C{x + 30} {y + 6} {x + 60} {y - 2} {x + 70} {y}" stroke-width="2.2"/>')
    x += 70
    for i in range(4):
        L = 30
        o.append(f'<rect x="{f(x + 4)}" y="{f(y - 7)}" width="{L}" height="14" rx="7" fill="url(#{p}-h)" stroke-width="1.3"/>')
        o.append(f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(x + 4)}" y2="{f(y)}" stroke-width="2"/>')
        x += L + 8
        y += rng.uniform(-2, 2)
    o.append(f'<line x1="{f(x - 4)}" y1="{f(y)}" x2="{f(x + 10)}" y2="{f(y)}" stroke-width="2"/>')
    # terminales con botones
    for ang in (-.7, -.25, .2, .65):
        ex, ey = x + 10 + math.cos(ang) * 34, y + math.sin(ang) * 34
        o.append(f'<path d="M{f(x + 10)} {f(y)} Q{f(x + 22)} {f(y + math.sin(ang) * 6)} {f(ex)} {f(ey)}" stroke-width="1.1"/>')
        o.append(f'<circle class="ac" cx="{f(ex + 2)}" cy="{f(ey)}" r="4" stroke="none"/>')
    return svg(p, "".join(o), "Neurona con axón mielinizado")


# ---------------------------------------------------------------- IV. Oncohematología
def onco():
    rng = random.Random(5)
    p = "l-onc"
    o = []
    celulas = [(300, 160, 40, "plasma"), (120, 112, 22, "linfo"), (380, 286, 22, "linfo")]
    hematies = []
    intentos = 0
    while len(hematies) < 34 and intentos < 4000:
        intentos += 1
        r = rng.uniform(15, 19)
        x, y = rng.uniform(r + 6, W - r - 6), rng.uniform(r + 6, H - r - 6)
        if all(math.hypot(x - a, y - b) > r + c + 3 for a, b, c, _ in celulas) and all(math.hypot(x - a, y - b) > r + c - 2 for a, b, c in hematies):
            hematies.append((x, y, r))
    for x, y, r in hematies:
        o.append(f'<path d="{blob(x, y, r, rng, 10, .04)}" stroke-width="1.2"/>')
        o.append(f'<path d="{blob(x + 1, y + 1, r * .45, rng, 8, .1)}" stroke-width=".5"/>')
        # sombreado en media luna
        o.append(f'<path d="M{f(x - r * .82)} {f(y + r * .3)} A{f(r * .9)} {f(r * .9)} 0 0 0 {f(x + r * .3)} {f(y + r * .82)}" stroke-width=".5" stroke-dasharray="1.5 1.8"/>')
    for x, y, r, tipo in celulas:
        o.append(f'<path d="{blob(x, y, r, rng, 12, .07)}" fill="url(#{p}-f)" stroke-width="1.6"/>')
        if tipo == "linfo":
            o.append(f'<path d="{blob(x - 1, y, r * .82, rng, 10, .08)}" fill="url(#{p}-x)" stroke-width="1.3"/>')
        else:
            nx, ny = x - 13, y + 6
            o.append(f'<circle cx="{nx + 18}" cy="{ny - 10}" r="11" fill="var(--papel)" stroke-width=".5" stroke-dasharray="1 2"/>')
            o.append(f'<circle cx="{nx}" cy="{ny}" r="19" fill="var(--papel)" stroke-width="1.5"/>')
            for i in range(9):
                a = 2 * math.pi * i / 9
                o.append(f'<circle class="ac" cx="{f(nx + math.cos(a) * 12)}" cy="{f(ny + math.sin(a) * 12)}" r="3" stroke="none"/>')
            o.append(f'<circle class="ac" cx="{nx}" cy="{ny}" r="3.4" stroke="none"/>')
    return svg(p, "".join(o), "Frotis de sangre con una célula plasmática")


# ---------------------------------------------------------------- V. Inmunomediadas (piel)
def gteii():
    rng = random.Random(9)
    p = "l-pie"
    o = []
    def union(x):
        return 168 + 26 * math.sin(x / 34) + 6 * math.sin(x / 11)
    # capa córnea
    for k in range(5):
        ps = [(x, 34 + k * 5 + 1.5 * math.sin(x / 23 + k)) for x in range(0, W + 1, 24)]
        o.append(f'<path d="{suave(ps)}" stroke-width="{1.2 if k == 0 else .6}"/>')
    # queratinocitos en empedrado
    y = 64
    fila = 0
    while y < 200:
        x = -10 + (fila % 2) * 12
        while x < W + 10:
            w, h = rng.uniform(20, 26), rng.uniform(13, 16) - min(4, (200 - y) / 40)
            if y + h / 2 < union(x) - 4:
                o.append(f'<path d="{blob(x, y, w / 2, rng, 8, .1, h / 2)}" stroke-width=".9"/>')
                o.append(f'<circle cx="{f(x + rng.uniform(-2, 2))}" cy="{f(y)}" r="2.2" fill="currentColor" stroke="none"/>')
            x += w + 1.5
        y += 14
        fila += 1
    # membrana basal ondulada
    ps = [(x, union(x)) for x in range(0, W + 1, 8)]
    o.append(f'<path d="{suave(ps)}" stroke-width="2"/>')
    # dermis: fibras de colágeno
    for k in range(13):
        base = 214 + k * 11
        ps = [(x, base + 5 * math.sin(x / (18 + k) + k) + rng.uniform(-1, 1)) for x in range(0, W + 1, 20)]
        o.append(f'<path d="{suave(ps)}" stroke-width=".55"/>')
    # folículo piloso oblicuo
    o.append(f'<path d="M352 40 L340 180 Q330 300 352 318 Q378 312 372 290 L380 182 L368 40" fill="var(--papel)" stroke-width="1.5"/>')
    o.append(f'<path d="M358 20 L356 300" stroke-width="2.6"/>')
    o.append(f'<path d="M346 296 Q360 286 374 296 Q370 316 352 316 Z" fill="url(#{p}-x)" stroke-width="1.2"/>')
    # vaso en corte
    o.append(f'<ellipse cx="120" cy="290" rx="24" ry="15" fill="var(--papel)" stroke-width="1.6"/>')
    o.append(f'<ellipse cx="120" cy="290" rx="16" ry="9" fill="url(#{p}-h)" stroke-width=".8"/>')
    # infiltrado inflamatorio junto a la unión (realce)
    for _ in range(46):
        x = rng.uniform(150, 310)
        yy = union(x) + rng.uniform(6, 50)
        o.append(f'<circle class="ac" cx="{f(x)}" cy="{f(yy)}" r="{f(rng.uniform(2, 3.2))}" stroke="none"/>')
    return svg(p, "".join(o), "Corte de piel con infiltrado inflamatorio")


# ---------------------------------------------------------------- VI. Neuropsiquiatría (sinapsis)
def sinapsis():
    rng = random.Random(21)
    p = "l-sin"
    o = []
    # botón presináptico
    pre = [(120, 0), (90, 60), (96, 140), (150, 196), (240, 208), (330, 196), (384, 140), (390, 60), (360, 0)]
    o.append(f'<path d="{suave(pre)}" stroke-width="2"/>')
    o.append(f'<path d="M150 196 Q240 214 330 196" stroke-width="3.2"/>')
    # mitocondria
    o.append(f'<ellipse cx="300" cy="62" rx="46" ry="20" transform="rotate(-14 300 62)" fill="url(#{p}-f)" stroke-width="1.5"/>')
    for i in range(6):
        x = 268 + i * 12
        o.append(f'<path d="M{x} {f(56 + (x - 300) * .25 + 12)} q4 -12 0 -22" stroke-width=".9" transform="rotate(-14 300 62)"/>')
    # vesículas
    ves = []
    while len(ves) < 30:
        x, y = rng.uniform(120, 360), rng.uniform(70, 182)
        if (x - 300) ** 2 / 60 ** 2 + (y - 62) ** 2 / 34 ** 2 < 1:
            continue
        if all(math.hypot(x - a, y - b) > 19 for a, b in ves):
            ves.append((x, y))
    for x, y in ves:
        o.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="8" stroke-width="1.2"/>')
        o.append(punteado(rng, lambda a, b, x=x, y=y: (a - x) ** 2 + (b - y) ** 2 < 36, 5, (x - 6, y - 6, x + 6, y + 6), (.6, 1)))
    # vesícula fusionándose
    o.append(f'<path d="M218 205 A12 12 0 1 1 246 205" stroke-width="1.4"/>')
    # neurotransmisor en la hendidura (realce)
    for _ in range(36):
        x = rng.uniform(190, 290) + rng.uniform(-30, 30)
        y = rng.uniform(214, 240)
        o.append(f'<circle class="ac" cx="{f(x)}" cy="{f(y)}" r="2.2" stroke="none"/>')
    # membrana postsináptica con receptores
    post = [(40, 360), (60, 290), (130, 252), (240, 246), (350, 252), (420, 290), (440, 360)]
    o.append(f'<path d="{suave(post)}" stroke-width="2"/>')
    for i in range(9):
        x = 150 + i * 22
        y = 249 - 0 * i
        o.append(f'<rect x="{x - 4}" y="{f(y - 7)}" width="8" height="14" rx="2" fill="url(#{p}-x)" stroke-width="1"/>')
    o.append(punteado(rng, lambda x, y: y > 262 + abs(x - 240) * .35 and y < 352, 160, (60, 260, 420, 352), (.5, 1)))
    return svg(p, "".join(o), "Sinapsis química")


# ---------------------------------------------------------------- VII. Respiratorio
def neumo():
    rng = random.Random(13)
    p = "l-neumo"
    o = []
    # silueta pulmonar discontinua
    izq = [(218, 96), (186, 82), (152, 100), (124, 148), (104, 218), (94, 290), (108, 330), (160, 322), (210, 334), (226, 304), (224, 200)]
    der = [(480 - x, y) for x, y in izq]
    for lado in (izq, der):
        o.append(f'<path d="{suave(lado, True)}" stroke-width=".8" stroke-dasharray="3 4"/>')
    # tráquea con anillos de cartílago
    o.append('<path d="M232 8 L232 96 M248 8 L248 96" stroke-width="1.8"/>')
    for y in range(14, 92, 8):
        o.append(f'<path d="M232 {y} Q240 {y + 4} 248 {y}" stroke-width="1.6"/>')

    def dentro(poly, x, y):
        c = False
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i - 1], poly[i]
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                c = not c
        return c

    def rama(x, y, dianas, ancho):
        if len(dianas) <= 2:
            for tx, ty in dianas:
                o.append(f'<path d="M{f(x)} {f(y)} L{f(tx)} {f(ty)}" stroke-width="{f(max(.6, ancho))}"/>')
                for _ in range(3):
                    a = rng.uniform(0, 2 * math.pi)
                    o.append(f'<circle cx="{f(tx + math.cos(a) * 3.4)}" cy="{f(ty + math.sin(a) * 3.4)}" r="{f(rng.uniform(2.1, 2.9))}" stroke-width=".6"/>')
                if rng.random() < .1:
                    o.append(f'<circle class="ac" cx="{f(tx)}" cy="{f(ty)}" r="2.5" stroke="none"/>')
            return
        # divide las dianas por su eje más largo y avanza hacia el centro de cada mitad
        xs = [d[0] for d in dianas]; ys = [d[1] for d in dianas]
        eje = 0 if max(xs) - min(xs) > max(ys) - min(ys) else 1
        dianas = sorted(dianas, key=lambda d: d[eje])
        m = len(dianas) // 2
        for grupo in (dianas[:m], dianas[m:]):
            cx = sum(d[0] for d in grupo) / len(grupo); cy = sum(d[1] for d in grupo) / len(grupo)
            k = .42 if len(grupo) > 4 else .6
            x2, y2 = x + (cx - x) * k, y + (cy - y) * k
            mx, my = (x + x2) / 2 + rng.uniform(-3, 3), (y + y2) / 2 + rng.uniform(-3, 3)
            o.append(f'<path d="M{f(x)} {f(y)} Q{f(mx)} {f(my)} {f(x2)} {f(y2)}" stroke-width="{f(ancho)}"/>')
            rama(x2, y2, grupo, ancho * .74)

    for lado, sx in ((izq, 226), (der, 254)):
        dianas = []
        while len(dianas) < 64:
            x, y = rng.uniform(90, 390), rng.uniform(96, 330)
            if dentro(lado, x, y) and all(math.hypot(x - a, y - b) > 15 for a, b in dianas):
                ok = all(math.hypot(x - lx, y - ly) > 9 for lx, ly in lado)
                if ok:
                    dianas.append((x, y))
        o.append(f'<path d="M240 96 L{sx} 112" stroke-width="4.6"/>')
        rama(sx, 112, dianas, 4.2)
    return svg(p, "".join(o), "Árbol bronquial")


LAMINAS = {
    "vih": (vih, "Virión del VIH en corte: envoltura con sus glicoproteínas, cápside cónica y las dos hebras de ARN."),
    "cardio": (cardio, "Lipoproteína rica en triglicéridos: monocapa de fosfolípidos, núcleo lipídico y apolipoproteínas en la superficie."),
    "geafen": (neuro, "Neurona: cuerpo celular, dendritas y axón con su vaina de mielina."),
    "gedefo": (onco, "Frotis de sangre: hematíes, dos linfocitos y una célula plasmática."),
    "gteii": (gteii, "Corte de piel: epidermis, unión dermoepidérmica y dermis con infiltrado inflamatorio."),
    "neuropsiquiatria": (sinapsis, "Sinapsis química: vesículas, hendidura sináptica y receptores de la membrana postsináptica."),
    "neumo": (neumo, "Árbol bronquial: tráquea, bronquios y racimos de alvéolos."),
}


def todas():
    return {k: {"svg": fn(), "pie": pie} for k, (fn, pie) in LAMINAS.items()}


if __name__ == "__main__":
    import sys, pathlib
    out = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "laminas.html")
    cuerpo = "".join(f'<figure style="margin:0"><div style="color:#1f1b16">{v["svg"]}</div><figcaption>{k}: {v["pie"]}</figcaption></figure>' for k, v in todas().items())
    out.write_text('<!doctype html><meta charset="utf-8"><style>:root{--papel:#f5f0e6;--acento:#9b2318}body{background:#f5f0e6;display:grid;grid-template-columns:repeat(2,1fr);gap:20px;padding:20px;font-family:serif}.ac{fill:var(--acento)}.acs{stroke:var(--acento)}svg{width:100%}</style>' + cuerpo)
