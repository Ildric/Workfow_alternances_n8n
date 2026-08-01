from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "candidatures.db")


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


@app.route("/candidature", methods=["POST"])
def ajouter_candidature(force=True, silent=True)
    print("DEBUG - Content-Type reçu :", request.content_type)
    print("DEBUG - Body brut :", request.data)
    print("DEBUG - Data parsée :", data)
    data = request.get_json()

    if not data:
        return jsonify({"error": "Aucune donnée JSON reçue"}), 400

    entreprise = data.get("entreprise") or "Non renseigné"
    poste = data.get("poste") or "Non renseigné"
    domaine = data.get("domaine") or "Non renseigné"
    lien_offre = data.get("lien_offre")
    statut = data.get("statut") or "à postuler"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO candidatures (entreprise, poste, domaine, statut, lien_offre)
            VALUES (?, ?, ?, ?, ?)
            """,
            (entreprise, poste, domaine, statut, lien_offre)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Candidature enregistrée", "entreprise": entreprise}), 201


@app.route("/candidatures", methods=["GET"])
def lister_candidatures():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidatures")
    rows = cursor.fetchall()
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)