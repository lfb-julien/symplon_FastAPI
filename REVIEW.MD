# Modifications to FastAPI Code

## Mitigation of SQL Injection

To enhance security and prevent SQL injection, queries have been updated to use parameterized queries instead of string formatting. This change is applied to all endpoints.

**Example Modification:** :

Before :
```python
res = cur.execute(f"SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE date = {year} AND ville = '{city}'")
```

After :
```python
res = cur.execute("SELECT revenu_fiscal_moyen FROM foyers_fiscaux WHERE date = ? AND ville = ?", (year, city))
```

## Correction of Missing SELECT Clause

The endpoint for "Top 10 cities with the lowest average price per square meter for apartments" was corrected to include the missing SELECT clause in the SQL query.

**Modification made** :

before :
```python
    res = cur.execute("""
        FROM transactions_sample 
        WHERE type_batiment = 'appartement' 
        GROUP BY ville 
        ORDER BY prix_m2_moyen ASC 
        LIMIT 10
    """)
```

after :
```python
    res = cur.execute("""
        SELECT FROM transactions_sample 
        WHERE type_batiment = 'appartement' 
        GROUP BY ville 
        ORDER BY prix_m2_moyen ASC 
        LIMIT 10
    """)
```

