from fastapi import FastAPI, HTTPException, Query
import sqlite3

app = FastAPI()

# 1. En tant qu'Agent je veux pouvoir consulter le revenu fiscal moyen des foyers de ma ville (Montpellier)
@app.get("/revenu_fiscal_moyen/", description="1. Obtenir le revenu fiscal moyen des foyers d'une ville pour une année donnée.")
async def revenu_fiscal_moyen(year: int = Query(...), city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE date = {year} AND ville = '{city}'")
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"revenu_fiscal_moyen": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""
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
# 2. En tant qu'Agent je veux consulter les 10 dernières transactions dans ma ville (Lyon)
@app.get("/top10_transaction/", description="2. Obtenir les 10 dernières transactions dans une ville.")
async def top_transaction_10(city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT id_transaction FROM transactions_sample WHERE ville = '{city}' ORDER BY date_transaction DESC LIMIT 10")
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"top_transactions": [result[0] for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 3. En tant qu'Agent je souhaite connaitre le nombre d'acquisitions dans ma ville (Paris) durant l'année 2022
@app.get("/nb_acquisitions_city/", description="3. Obtenir le nombre d'acquisitions dans une ville pour une année donnée.")
async def nb_acquisitions_city(city: str = Query(...), year: int = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT COUNT(id_transaction) FROM transactions_sample WHERE ville = '{city}' AND date_transaction LIKE '{year}%'")
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"nombre_acquisitions": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 4. En tant qu'Agent je souhaite connaitre la répartition des appartements vendus (à Marseille) durant l'année 2022 en fonction du nombre de pièces
@app.get("/repartition_appart/", description="4. Obtenir la répartition des appartements vendus dans une ville pour une année donnée en fonction du nombre de pièces.")
async def repartition_appartement(year: int = Query(...), city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT n_pieces, COUNT(*) AS nombre_appartements FROM transactions_sample WHERE ville = '{city}' AND date_transaction LIKE '{year}%' AND type_batiment = 'appartement' GROUP BY n_pieces")
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"repartition_appartements": [{"n_pieces": result[0], "nombre_appartements": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. En tant qu'Agent je souhaite connaitre le nombre d'acquisitions de studios dans ma ville (Rennes) durant l'année 2022
@app.get("/acquisitions_studio/", description="5. Obtenir le nombre d'acquisitions de studios dans une ville pour une année donnée.")
async def acquisitions_studio(year: int = Query(...), city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT COUNT(*) AS nombre_acquisitions_studios FROM transactions_sample WHERE ville = '{city}' AND date_transaction LIKE '{year}%' AND type_batiment = 'studio'")
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"nombre_acquisitions_studios": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 6. En tant qu'Agent je souhaite connaitre le prix au m2 moyen pour les maisons vendues à Avignon l'année 2022
@app.get("/prix_m2_moyen_maison/", description="6. Obtenir le prix au m2 moyen pour les maisons vendues dans une ville pour une année donnée.")
async def prix_m2_moyen_maison(city: str = Query(...), year: int = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT AVG(prix / surface_habitable) AS prix_m2_moyen FROM transactions_sample WHERE ville = '{city}' AND date_transaction LIKE '{year}%' AND type_batiment = 'maison'")
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"prix_m2_moyen_maison": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 7. En tant que CEO, je veux consulter le nombre de transactions (tout type confondu) par département, ordonnées par ordre décroissant
@app.get("/nb_transactions_departement/", description="7. Obtenir le nombre de transactions par département, ordonnées par ordre décroissant.")
async def nb_transactions_departement():
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT departement, COUNT(*) AS nombre_transactions FROM transactions_sample GROUP BY departement ORDER BY nombre_transactions DESC")
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"nb_transactions_departement": [{"departement": result[0], "nombre_transactions": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 8. En tant que CEO, je veux consulter le top 10 des villes les plus dynamiques en termes de transactions immobilières
@app.get("/top_10_villes/", description="8. Obtenir le top 10 des villes les plus dynamiques en termes de transactions immobilières.")
async def top_10_villes():
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute(f"SELECT ville, COUNT(*) as nombre_transactions FROM transactions_sample GROUP BY ville ORDER BY nombre_transactions DESC LIMIT 10")
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"top_10_villes": [{"ville": result[0], "nombre_transactions": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 9. En tant que CEO je souhaite connaitre le nombre total de vente d'appartements en 2022 dans toutes les villes où le revenu fiscal moyen en 2018 est supérieur à 70k
@app.get("/nb_ventes_appart_2022/", description="9. Obtenir le nombre total de ventes d'appartements en 2022 dans toutes les villes où le revenu fiscal moyen en 2018 est supérieur à 70k.")
async def nb_ventes_appart_2022():
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute("""
                SELECT COUNT(*) as nombre_ventes_appart_2022
                FROM transactions_sample t
                JOIN foyers_fiscaux f ON t.ville = f.ville
                WHERE t.type_batiment = 'appartement' AND t.date_transaction LIKE '2022%' AND f.revenu_fiscal_moyen > 70000
            """)
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"nombre_ventes_appart_2022": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 10. En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus bas pour les appartements
@app.get("/top_10_villes_prix_m2_bas/", description="10. Obtenir le top 10 des villes avec un prix au m2 moyen le plus bas pour les appartements.")
async def top_10_villes_prix_m2_bas():
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute("""
                FROM transactions_sample 
                WHERE type_batiment = 'appartement' 
                GROUP BY ville 
                ORDER BY prix_m2_moyen ASC 
                LIMIT 10
            """)
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"top_10_villes_prix_m2_bas": [{"ville": result[0], "prix_m2_moyen": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 11. En tant que CEO, je veux accéder aux 10 villes avec un prix au m2 moyen le plus haut pour les maisons
@app.get("/top_10_villes_prix_m2_haut/", description="11. Obtenir le top 10 des villes avec un prix au m2 moyen le plus haut pour les maisons.")
async def top_10_villes_prix_m2_haut():
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            res = cur.execute("""
                SELECT ville, AVG(prix / surface_habitable) AS prix_m2_moyen 
                FROM transactions_sample 
                WHERE type_batiment = 'maison' 
                GROUP BY ville 
                ORDER BY prix_m2_moyen DESC 
                LIMIT 10
            """)
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"top_10_villes_prix_m2_haut": [{"ville": result[0], "prix_m2_moyen": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Exécuter l'application avec uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)