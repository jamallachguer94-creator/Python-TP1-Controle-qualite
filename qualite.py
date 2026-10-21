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


def moyenne(*valeurs):
    if not valeurs:
        raise ValueError("Aucune valeur fournie")
    return sum(valeurs) / len(valeurs)

def ecart_type(*valeurs):
    if len(valeurs) < 2:
        raise ValueError("Au moins 2 valeurs requises")
    m = moyenne(*valeurs)
    somme_ecarts = sum((x - m) ** 2 for x in valeurs)
    return math.sqrt(somme_ecarts / (len(valeurs) - 1))

def capabilite(mesures, *, nominal=NOMINAL, tolerance=TOLERANCE):
    s = ecart_type(*mesures)
    if s == 0:
        raise ValueError("Écart-type nul")
    m = moyenne(*mesures)
    t_min = nominal - tolerance
    t_max = nominal + tolerance
    cp = (t_max - t_min) / (6 * s)
    cpk = min(t_max - m, m - t_min) / (3 * s)
    return round(cp, 2), round(cpk, 2)


def entete(nominal=NOMINAL, tolerance=TOLERANCE):
    return f"Contrôle des axes\n{nominal:.2f} ± {tolerance:.2f} mm"

def rapport(lignes, *, nominal=NOMINAL, tolerance=TOLERANCE):
    resultats, erreurs = analyser_lot(lignes, nominal=nominal, tolerance=tolerance)
    sortie = [entete(nominal, tolerance)]
    sortie.append(f"{'Code':<10} {'Mesure':>8} {'Écart':>9}   Verdict")
    
    for code, mesure, v in resultats:
        e = ecart(mesure, nominal)
        sortie.append(f"{code:<10} {mesure:>8.3f} {e:>+9.3f}   {v}")
        
    c, a, r = compter_verdicts(resultats)
    total = c + a + r
    taux = (c / total) if total else 0.0
    sortie.append(f"Pièces {total} | conformes: {c} ({taux:.1%})  à reprendre {a} rebuts: {r}")
    
    valides = [m for _, m, _ in resultats]
    if len(valides) >= 2:
        try:
            cp, cpk = capabilite(valides, nominal=nominal, tolerance=tolerance)
            etat = "procédé capable" if cpk >= 1.33 else "procédé NON capable"
            sortie.append(f"Cp = {cp:.2f} | Cpk = {cpk:.2f} -> {etat}")
        except ValueError:
            pass
            
    if erreurs:
        sortie.append(f"Lignes rejetées: {len(erreurs)}")
        for err in erreurs:
            sortie.append(f"  {err}")
            
    return "\n".join(sortie)
