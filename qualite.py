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
