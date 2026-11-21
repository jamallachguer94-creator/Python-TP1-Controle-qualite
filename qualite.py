import math

NOMINAL = 25.0
TOLERANCE = 0.05

def lire_mesure(texte):
    texte_nettoye = (
        texte.strip()
        .lower()
        .removesuffix("mm")
        .strip()
        .replace(",", ".")
    )

    try:
        mesure = float(texte_nettoye)
    except ValueError:
        raise ValueError(
            f"mesure invalide : {texte.strip()!r}"
        )

    if not math.isfinite(mesure) or mesure <= 0:
        raise ValueError(
            f"mesure invalide : {texte.strip()!r}"
        )

    return mesure

def valider_code(code):
    return (
        len(code) == 8
        and code.isascii()
        and code[:3].isalpha()
        and code[:3].isupper()
        and code[3] == "-"
        and code[4:].isdigit()
    )


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
        raise ValueError(f"code invalide : '{code}'")
        
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
            erreurs.append(f"ligne {i} : {err}")
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
    resultats, erreurs = analyser_lot(
        lignes,
        nominal=nominal,
        tolerance=tolerance
    )

    conformes, a_reprendre, rebuts = compter_verdicts(resultats)

    sortie = []

    # En-tête
    sortie.append(
        f"Contrôle des axes : {nominal:.2f} ± {tolerance:.2f} mm"
    )

    # En-tête du tableau
    sortie.append(
        f"{'Code':<10}{'Mesure':>8}{'Écart':>9}   Verdict"
    )

    # Détails des pièces
    for code, mesure, v in resultats:
        e = ecart(mesure, nominal)

        sortie.append(
            f"{code:<10}{mesure:>8.3f}{e:>+9.3f}   {v}"
        )

    # Bilan
    total = len(resultats)
    taux = conformes / total if total > 0 else 0.0

    sortie.append(
        f"Pièces : {total} | conformes : {conformes} "
        f"({taux:.1%}) | à reprendre : {a_reprendre} | rebuts : {rebuts}"
    )

    # Capabilité : uniquement avec au moins deux pièces
    if total >= 2:
        mesures = [mesure for code, mesure, v in resultats]

        cp, cpk = capabilite(
            mesures,
            nominal=nominal,
            tolerance=tolerance
        )

        conclusion = (
            "procédé capable"
            if cpk >= 1.33
            else "procédé NON capable"
        )

        sortie.append(
            f"Cp = {cp:.2f} | Cpk = {cpk:.2f} -> {conclusion}"
        )

    # Lignes rejetées
    if erreurs:
        sortie.append(f"Lignes rejetées : {len(erreurs)}")

        for erreur in erreurs:
            sortie.append(f"  {erreur}")

    return "\n".join(sortie)


def histogramme(mesures, *, debut, pas, nb_classes):
    lignes = []
    for i in range(nb_classes):
        bas = round(debut + i * pas, 3)
        haut = round(debut + (i + 1) * pas, 3)
        count = sum(1 for m in mesures if bas <= m < haut)
        etoiles = f" {'*' * count}"
        lignes.append(f"[{bas:.3f} ; {haut:.3f}[{etoiles}")
    return "\n".join(lignes)
