# Description du Code

Ce projet est une API FastAPI qui fournit divers endpoints pour accéder et analyser des données immobilières stockées dans une base de données SQLite. Chaque endpoint répond à une user story spécifique, permettant aux utilisateurs d'obtenir des informations telles que le revenu fiscal moyen des foyers, les transactions immobilières récentes, le nombre d'acquisitions, etc.

## Structure du Code

Le code est organisé de la manière suivante :

- **Importations :** Les modules nécessaires sont importés, y compris FastAPI, SQLite3, et Query de FastAPI pour gérer les paramètres de requête.

- **Création de l'Application :** Une instance de l'application FastAPI est créée.

- **Endpoints :** Chaque endpoint correspond à une user story spécifique et utilise la syntaxe de FastAPI pour définir les paramètres de requête, se connecter à la base de données SQLite, exécuter des requêtes SQL, et gérer les erreurs.

- **Exécution de l'Application :** L'application est exécutée avec uvicorn.

"""bash
Explication du code point par point

@app.get("/revenu_fiscal_moyen/", description="1. Obtenir le revenu fiscal moyen des foyers d'une ville pour une année donnée.")
 Dans le code FastAPI, @app.get est utilisé pour définir un endpoint dans une application FastAPI.
 On indique ensuite l'url cible(relatif) et une description

 async def revenu_fiscal_moyen(year: int = Query(...), city: str = Query(...)):
 pour rappel def permet de dire qu'on va crée une fonction. Pour async: Il est utilisé pour définir des fonctions asynchrones. 
Les fonctions asynchrones, également appelées coroutines, permettent l'exécution de plusieurs tâches de manière 
concurrente sans bloquer le programme principal. En gros par exemple une tache qu'on veut exacuté sois même apres execution du programme
via un click sur un bouton


  try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE date = {year} AND ville = '{city}'")
            result = res.fetchone()

On crée une condition pour testé si on trouve la donnée via notre requette.
on dit avec quoi on se connecte et a quoi
on crée le curseur 
et on l'utilise pour faire la requette avec les ptite variable précédement faite
on met le resultat dans result

petite explication pour fetchone() ou all()
fetchone() renvoie un seul tuple représentant la première ligne de résultats.
fetchall() renvoie une liste de tuples représentant toutes les lignes de résultats.
Si la requête ne renvoie aucun résultat, fetchone() renvoie None, et fetchall() renvoie une liste vide ([]).
L'utilisation de fetchall() peut être inefficace pour de grandes quantités de données car elle récupère toutes les lignes en mémoire.
En général, pour des résultats potentiels importants, il est préférable d'utiliser fetchone() et de parcourir les résultats au fur et à mesure 
pour éviter une utilisation excessive de la mémoire. 

Pour faire plus simple c'est pour dire si on veut une liste ou pas....


 if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
si il y a pas de resultat car pas de donnée trouvé on affiche pas de résultat trouvé

else:
                return {"revenu_fiscal_moyen": result[0]}
et si non on affiche le resultat

petite précision:

si la requête SQL renvoie plusieurs colonnes, result[0], result[1], etc., font référence aux valeurs de chaque colonne 
pour la première ligne de résultats.
Si il n'y a qu'une colone on met 0

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
Dans le contexte du code FastAPI, le bloc except Exception as e: est utilisé pour capturer toute exception
 qui pourrait se produire lors de l'exécution du code à l'intérieur du bloc try. Ensuite, il utilise FastAPI 
 pour lever une exception HTTP (HTTPException) avec un code d'état 500 (Erreur interne du serveur) 
 et le détail de l'exception en tant que message.
"""

# Utilisation de l'API

## Installation

```bash
pip install -r requirements.txt
uvicorn main:app --reload

```
Readme by ChatGPT
