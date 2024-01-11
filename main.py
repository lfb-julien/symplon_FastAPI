from fastapi import FastAPI, HTTPException, Query
import sqlite3

app = FastAPI()

# 1. En tant qu'Agent je veux pouvoir consulter le revenu fiscal moyen des foyers de ma ville (Montpellier)
@app.get("/revenu_fiscal_moyen/", description="1. Obtenir le revenu fiscal moyen des foyers d'une ville pour une année donnée.")
async def revenu_fiscal_moyen(year: int = Query(...), city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            query = "SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE date = ? AND ville = ?"
            res = cur.execute(query, (year, city))
            result = res.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"revenu_fiscal_moyen": result[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 2. En tant qu'Agent je veux consulter les 10 dernières transactions dans ma ville (Lyon)
@app.get("/top10_transaction/", description="2. Obtenir les 10 dernières transactions dans une ville.")
async def top_transaction_10(city: str = Query(...)):
    try:
        with sqlite3.connect(r"chinook.db") as con:
            cur = con.cursor()
            query = "SELECT id_transaction FROM transactions_sample WHERE ville = ? ORDER BY date_transaction DESC LIMIT 10"
            res = cur.execute(query, (city,))
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
            query = "SELECT COUNT(id_transaction) FROM transactions_sample WHERE ville = ? AND date_transaction LIKE ?"
            res = cur.execute(query, (city, f"{year}%"))
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
            query = "SELECT n_pieces, COUNT(*) AS nombre_appartements FROM transactions_sample WHERE ville = ? AND date_transaction LIKE ? AND type_batiment = 'appartement' GROUP BY n_pieces"
            res = cur.execute(query, (city, f"{year}%"))
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
            query = "SELECT COUNT(*) AS nombre_acquisitions_studios FROM transactions_sample WHERE ville = ? AND date_transaction LIKE ? AND type_batiment = 'studio'"
            res = cur.execute(query, (city, f"{year}%"))
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
            query = "SELECT AVG(prix / surface_habitable) AS prix_m2_moyen FROM transactions_sample WHERE ville = ? AND date_transaction LIKE ? AND type_batiment = 'maison'"
            res = cur.execute(query, (city, f"{year}%"))
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
            query = "SELECT departement, COUNT(*) AS nombre_transactions FROM transactions_sample GROUP BY departement ORDER BY nombre_transactions DESC"
            res = cur.execute(query)
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
            query = "SELECT ville, COUNT(*) as nombre_transactions FROM transactions_sample GROUP BY ville ORDER BY nombre_transactions DESC LIMIT 10"
            res = cur.execute(query)
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
            query = """
                SELECT COUNT(*) as nombre_ventes_appart_2022
                FROM transactions_sample t
                JOIN foyers_fiscaux f ON t.ville = f.ville
                WHERE t.type_batiment = 'appartement' AND t.date_transaction LIKE '2022%' AND f.revenu_fiscal_moyen > 70000
            """
            res = cur.execute(query)
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
            query = """
                SELECT ville, AVG(prix / surface_habitable) AS prix_m2_moyen
                FROM transactions_sample
                WHERE type_batiment = 'appartement'
                GROUP BY ville
                ORDER BY prix_m2_moyen ASC
                LIMIT 10
            """
            res = cur.execute(query)
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
            query = """
                SELECT ville, AVG(prix / surface_habitable) AS prix_m2_moyen
                FROM transactions_sample
                WHERE type_batiment = 'maison'
                GROUP BY ville
                ORDER BY prix_m2_moyen DESC
                LIMIT 10
            """
            res = cur.execute(query)
            results = res.fetchall()
            if not results:
                raise HTTPException(status_code=404, detail="Pas de résultat trouvé")
            else:
                return {"top_10_villes_prix_m2_haut": [{"ville": result[0], "prix_m2_moyen": result[1]} for result in results]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Exécuter l'application avec uvicorn (uniquement si ce n'est pas chargé en tant que module)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1
