import pandas as pd

def afficher_liste_regions():
    chemin_fichier = '../data/clean/2018-data.csv'
    
    try:
        df = pd.read_csv(chemin_fichier, sep=";")
        
        if 'REGION' in df.columns:
            regions_uniques = df['REGION'].dropna().unique()    
            regions_uniques.sort() 
            
            print("-" * 40)
            print(f"[DEBUG] Nombre total de régions : {len(regions_uniques)}")
            print("[DEBUG] Liste détaillée :")
            print("-" * 40)
            
            for region in regions_uniques:
                print(region)
                
            print("-" * 40)
            
        else:
            print("[ERREUR] La colonne 'REGION' n'existe pas.")

    except FileNotFoundError:
        print(f"[ERREUR] Le fichier '{chemin_fichier}' est introuvable.")
    except Exception as e:
        print(f"[ERREUR] : {e}")

if __name__ == "__main__":
    afficher_liste_regions()