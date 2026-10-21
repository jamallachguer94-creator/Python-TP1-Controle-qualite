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
