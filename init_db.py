import sqlite3

def initialiser_base_de_donnees():
    conn = sqlite3.connect('candidatures.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entreprise TEXT NOT NULL,
            poste TEXT NOT NULL,
            domaine TEXT,
            statut TEXT DEFAULT 'À postuler',
            date_candidature DATE DEFAULT CURRENT_DATE,
            lien_offre TEXT
        )
    ''')

    cursor.execute('''
        INSERT INTO candidatures (entreprise, poste, domaine, statut, lien_offre)
        VALUES (?, ?, ?, ?, ?)
    ''', ('Mistral AI', 'Alternant Data & IA', 'IA', 'Postulé', 'https://mistral.ai/jobs'))

    conn.commit()
    conn.close()
    
    print("✅ La base de données 'candidatures.db' a été initialisée avec succès !")

if __name__ == "__main__":
    initialiser_base_de_donnees()