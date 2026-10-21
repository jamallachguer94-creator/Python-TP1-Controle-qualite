from qualite import analyser_ligne, rapport
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
                print(f"Refusé : {err}")
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
