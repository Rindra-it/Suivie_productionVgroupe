import psycopg2
from psycopg2 import Error

def connect_db():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="postgres123",
            host="127.0.0.1",
            port="5432",
            database="v_groupe_db"
        )
        return connection
    except (Exception, Error) as error:
        print("Erreur lors de la connexion à PostgreSQL", error)
        return None

def get_all_workers():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT matricule, nom_complet FROM ouvriers;")
        workers = cursor.fetchall()
        conn.close()
        return workers
    return []
    
def get_workers_list():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT matricule FROM ouvriers;")
        workers = [row[0] for row in cursor.fetchall()]
        conn.close()
        return workers
    return []

def get_styles_list():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code_style FROM styles;")
        styles = [row[0] for row in cursor.fetchall()]
        conn.close()
        return styles
    return []

def get_recent_suggestions(column_name):
    """Récupère les 5 dernières entrées uniques d'une colonne spécifique"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
    
        query = f"SELECT DISTINCT {column_name} FROM productions ORDER BY id DESC LIMIT 5;"
        try:
            cursor.execute(query)
            suggestions = [str(row[0]) for row in cursor.fetchall()]
            conn.close()
            return suggestions
        except:
            conn.close()
            return []
    return []

def save_production(date_prod, mat, sty, et, ca, qy, tk):
    conn = connect_db()
    if not conn: return False
    cursor = conn.cursor()
    
    
    q_manche = qy if ca == "Manche" else 0
    q_collar = qy if ca == "Col" else 0
    q_other = qy if ca not in ["Manche", "Col"] else 0

    try:
        cursor.execute("""
            INSERT INTO productions (date_prod, matricule, code_style, etat, qty_manche, qty_collar, qty_other)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (date_prod, mat, sty, et, q_manche, q_collar, q_other))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur SQL insertion : {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_productions():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT id, date_prod, matricule, code_style, etat, qty_manche, qty_other 
            FROM productions 
            ORDER BY date_prod DESC;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def get_aggregated_production(filter_type="all"):
    conn = connect_db()
    if not conn: return []
    
    
    date_filter = ""
    if filter_type == "day":
        date_filter = "WHERE date_prod = CURRENT_DATE"
    elif filter_type == "week":
        date_filter = "WHERE date_prod >= CURRENT_DATE - INTERVAL '7 days'"
    elif filter_type == "month":
        date_filter = "WHERE date_prod >= CURRENT_DATE - INTERVAL '30 days'"

    query = f"""
        SELECT 
            code_style, 
            SUM(qty_manche) as manche, 
            SUM(qty_collar) as collar, 
            SUM(qty_other) as autres,
            SUM(qty_manche + qty_collar + qty_other) as total
        FROM productions
        {date_filter}
        GROUP BY code_style
        ORDER BY total DESC;
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erreur SQL agrégation : {e}")
        return []
    

def get_worker_stats(filter_type="all"):
    conn = connect_db()
    if not conn: return []
    
    
    date_filter = ""
    if filter_type == "day":
        date_filter = "WHERE date_prod = CURRENT_DATE"
    elif filter_type == "week":
        date_filter = "WHERE date_prod >= CURRENT_DATE - INTERVAL '7 days'"
    elif filter_type == "month":
        date_filter = "WHERE date_prod >= CURRENT_DATE - INTERVAL '30 days'"

    query = f"""
        SELECT 
            matricule, 
            SUM(qty_manche + qty_collar + qty_other) as total_qty,
            COUNT(DISTINCT code_style) as styles_count
        FROM productions
        {date_filter}
        GROUP BY matricule
        ORDER BY total_qty DESC
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"Erreur SQL stats : {e}")
        return []


def save_worker(matricule, nom, prenom):
    """Enregistre ou met à jour un ouvrier (sans atelier)"""
    conn = connect_db()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ouvriers (matricule, nom, prenom)
            VALUES (%s, %s, %s)
            ON CONFLICT (matricule) 
            DO UPDATE SET nom = EXCLUDED.nom, prenom = EXCLUDED.prenom;
        """, (matricule, nom, prenom))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur SQL save_worker : {e}")
        return False
    finally:
        conn.close()

def get_all_workers():
    """Récupère la liste propre pour le tableau (3 colonnes)"""
    conn = connect_db()
    if not conn: return []
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT matricule, nom, prenom FROM ouvriers ORDER BY matricule ASC")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erreur SQL get_all_workers : {e}")
        return []
    finally:
        conn.close()

def get_dashboard_data():
    conn = connect_db()
    if not conn: return None
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT (productions.qty_manche + productions.qty_collar + productions.qty_other) FROM productions WHERE date_prod = CURRENT_DATE")
        total = cursor.fetchone()[0] or 0
        cursor.execute("SELECT COUNT(DISTINCT matricule) FROM productions WHERE date_prod = CURRENT_DATE")
        effectif = cursor.fetchone()[0] or 0
        
        
        cursor.execute("""
            SELECT matricule, SUM(productions.qty_manche + productions.qty_collar + productions.qty_other) as total FROM productions
            WHERE date_prod = CURRENT_DATE 
            GROUP BY matricule ORDER BY total DESC LIMIT 5
        """)
        top_5 = cursor.fetchall()

    
        cursor.execute("""
            SELECT matricule, code_style, (productions.qty_manche + productions.qty_collar + productions.qty_other), etat FROM productions
            ORDER BY id DESC LIMIT 10
        """)
        recent_entries = cursor.fetchall()

    
        cursor.execute("""
            SELECT date_prod, SUM(productions.qty_manche + productions.qty_collar + productions.qty_other) FROM productions 
            GROUP BY date_prod ORDER BY date_prod DESC LIMIT 7
        """)
        graph_data = cursor.fetchall()

        return {
            "total": total,
            "effectif": effectif,
            "top_5": top_5,
            "recent": recent_entries,
            "graph": graph_data
        }
    finally:
        conn.close()













def setup_database():
    """Crée les tables si elles n'existent pas encore"""
    conn = connect_db()
    if not conn: return
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ouvriers (
                matricule VARCHAR(50) PRIMARY KEY,
                nom VARCHAR(100) NOT NULL,
                prenom VARCHAR(100)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS production (
                id SERIAL PRIMARY KEY,
                date_production DATE DEFAULT CURRENT_DATE,
                matricule VARCHAR(50) REFERENCES ouvriers(matricule),
                code_style VARCHAR(100),
                etat VARCHAR(50),
                categorie VARCHAR(100),
                quantite INTEGER,
                ticket VARCHAR(100)
            )
        """)
        conn.commit()
        print("Connexion à la base de données")
    except Exception as e:
        print(f"Erreur lors du setup de la DB : {e}")
    finally:
        conn.close()

def get_all_styles():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT code_style FROM styles ORDER BY code_style ASC")
    res = cursor.fetchall()
    conn.close()
    return res

def add_style_to_repo(code):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO styles (code_style) VALUES (%s) ON CONFLICT DO NOTHING", (code.upper(),))
        conn.commit()
        return True
    except: return False
    finally: conn.close()


def delete_style(code_style):
    conn = connect_db()
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM styles WHERE code_style = ?", (code_style))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def update_style_code(old_code, new_code):
    conn = connect_db()
    
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE styles SET code_style = ? WHERE code_style = ?", (new_code, old_code))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()
