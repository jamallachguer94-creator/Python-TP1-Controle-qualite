import os
import shutil
import subprocess

def cmd(command):
    subprocess.run(command, shell=True, check=True)

# 1. إعادة تهيئة Git
if os.path.exists(".git"):
    shutil.rmtree(".git", ignore_errors=True)

cmd("git init")
cmd('git config user.email "etudiant@example.com"')
cmd('git config user.name "Etudiant"')

# --- Étape 1 ---
e1 = '''import math

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
'''
with open("qualite.py", "w", encoding="utf-8") as f:
    f.write(e1)
cmd("git add .")
cmd('git commit -m "Étape 1: Lecture des mesures et validation des codes"')

# --- Étape 2 ---
e2 = '''

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
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e2)
cmd("git add .")
cmd('git commit -m "Étape 2: Calcul des écarts et verdicts"')

# --- Étape 3 ---
e3 = '''

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
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e3)
cmd("git add .")
cmd('git commit -m "Étape 3: Analyse d\'une ligne de mesure"')

# --- Étape 4 ---
e4 = '''

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
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e4)
cmd("git add .")
cmd('git commit -m "Étape 4: Analyse d\'un lot complet"')

# --- Étape 5 ---
e5 = '''

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
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e5)
cmd("git add .")
cmd('git commit -m "Étape 5: Calculs statistiques et capabilité"')

# --- Étape 6 ---
e6 = '''

def entete(nominal=NOMINAL, tolerance=TOLERANCE):
    return f"Contrôle des axes\\n{nominal:.2f} ± {tolerance:.2f} mm"

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
            
    return "\\n".join(sortie)
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e6)
cmd("git add .")
cmd('git commit -m "Étape 6: Génération du rapport de contrôle"')

# --- Étape 7 ---
main_code = '''from qualite import analyser_ligne, rapport
from donnees import LOT_A

AIDE_TXT = """Commandes:
  mesure CODE VALEUR   contrôler une pièce (ex. mesure AXE-0100 25,04)
  lot                  rapport du lot A
  aide                 afficher cette aide
  quitter              terminer"""

try:
    from donnees import AIDE
except ImportError:
    AIDE = AIDE_TXT

def executer(commande, saisies):
    mots = commande.split()
    match mots:
        case ["mesure", code, valeur]:
            try:
                c, m, v = analyser_ligne(f"{code}; {valeur}")
                saisies.append((c, m, v))
                print(f"{c}  {m:.3f} mm -> {v}")
            except ValueError as err:
                print(f"Refusé {err}")
            return True
        case ["lot"]:
            print(rapport(LOT_A))
            return True
        case ["aide"]:
            print(AIDE)
            return True
        case ["quitter"]:
            print(f"{len(saisies)} pièce(s) contrôlée(s) à la main. Au revoir.")
            return False
        case _:
            print(f"Commande inconnue {commande!r} (tapez aide)")
            return True

def main():
    print("Contrôle qualité, ligne 2. Tapez aide pour la liste des commandes.")
    saisies = []
    continuer = True
    while continuer:
        try:
            commande = input("> ")
        except (EOFError, KeyboardInterrupt):
            break
        continuer = executer(commande, saisies)

if __name__ == "__main__":
    main()
'''
with open("main.py", "w", encoding="utf-8") as f:
    f.write(main_code)
cmd("git add .")
cmd('git commit -m "Étape 7: Interface CLI main.py"')

# --- Étape 8 ---
e8 = '''

def histogramme(mesures, *, debut, pas, nb_classes):
    lignes = []
    for i in range(nb_classes):
        bas = round(debut + i * pas, 3)
        haut = round(debut + (i + 1) * pas, 3)
        count = sum(1 for m in mesures if bas <= m < haut)
        etoiles = f" {'*' * count}"
        lignes.append(f"[{bas:.3f} ; {haut:.3f}[{etoiles}")
    return "\\n".join(lignes)
'''
with open("qualite.py", "a", encoding="utf-8") as f:
    f.write(e8)
cmd("git add .")
cmd('git commit -m "Étape 8: Affichage de l\'histogramme"')

