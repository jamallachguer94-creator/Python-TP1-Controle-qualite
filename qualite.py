import math

NOMINAL = 25.0
TOLERANCE = 0.05

def lire_mesure(texte):
    try:
        t_propre = texte.strip().lower().removesuffix("mm").strip().replace(",", ".")
        valeur = float(t_propre)
        if valeur <= 0 or not math.isfinite(valeur):
            raise ValueError()
        return valeur
    except ValueError:
        raise ValueError(f"mesure invalide: {texte.strip()!r}")

def valider_code(code):
    return (len(code) == 8 and 
            code[:3].isalpha() and code[:3].isupper() and code[:3].isascii() and 
            code[3] == "-" and 
            code[4:].isdigit())


def ecart(mesure, nominal=NOMINAL):
    return round(mesure - nominal, 3)

def verdict(mesure, nominal=NOMINAL, tolerance=TOLERANCE):
    if tolerance <= 0:
        raise ValueError("Tolérance invalide")
    e = ecart(mesure, nominal)
    if abs(e) <= tolerance:
        return "conforme"
    elif e > tolerance:
        return "à reprendre"
    else:
        return "rebut"


def analyser_ligne(ligne, *, nominal=NOMINAL, tolerance=TOLERANCE):
    champs = ligne.split(";")
    if len(champs) != 2:
        raise ValueError(f"2 champs attendus, {len(champs)} trouvé(s)")
    
    code = champs[0].strip().upper()
    if not valider_code(code):
        raise ValueError(f"code invalide: {code!r}")
        
    mesure = lire_mesure(champs[1])
    v = verdict(mesure, nominal, tolerance)
    return (code, mesure, v)


def analyser_lot(lignes, **reglages):
    resultats = []
    erreurs = []
    for i, ligne in enumerate(lignes, start=1):
        if not ligne.strip() or ligne.lstrip().startswith("#"):
            continue
        try:
            resultats.append(analyser_ligne(ligne, **reglages))
        except ValueError as err:
            erreurs.append(f"ligne {i} {err}")
    return resultats, erreurs

def compter_verdicts(resultats):
    c = a = r = 0
    for _, _, v in resultats:
        if v == "conforme":
            c += 1
        elif v == "à reprendre":
            a += 1
        elif v == "rebut":
            r += 1
    return c, a, r
