# Automatisation de gestion des candidatures d'alternance — n8n

## Objectif

Cette V2 vient enrichir la brique fonctionnelle de base posée en V1. L'objectif est désormais d'automatiser l'ensemble du cycle : de la réception d'une offre brute jusqu'à la génération d'une candidature personnalisée (CV ajusté + lettre de motivation), en passant par un stockage structuré permettant le suivi et l'analyse des candidatures.

---

## Stack

* **Orchestration :** n8n
* **IA / LLM :** Claude (Opus 5 pour l'extraction, Sonnet 4.6 pour la génération) via Anthropic API
* **Stockage candidatures :** API HTTP locale (`127.0.0.1:5000/candidature`) — backend Flask/similaire
* **Données CV :** fichier `cv_structure.json` local, lu depuis le disque
* **Envoi email :** Resend
* **Format d'échange :** JSON
* **Versionning :** Git / GitHub (branche `v2`)

---

## Architecture du workflow (v2.0)

Formulaire (nom_entreprise, intitule_poste, description_offre)
        ¦
        v
Basic LLM Chain (Claude Opus 5)
-> Extraction structurée : entreprise, poste, domaine,
  lien_offre, date_candidature, localisation, statut
        ¦
        +-----------------------------+
	¦                             ¦
        v                             v
Code JS (parse JSON)          Read/Write Files from Disk
        ¦                       (lecture cv_structure.json)
	¦                             ¦
        v                             v
HTTP Request                  Extract from File (JSON)
(POST -> API candidature)             ¦
        ¦                             ¦
        +---------------+-------------+
                        v
                     Merge (combine)
                        ¦
                        v
        Basic LLM Chain1 (Claude Sonnet 4.6)
         Analyse CV + offre :
          - points forts matchant l'offre
          - suggestions d'ajustement CV
          - lettre de motivation complète
                        ¦
                        v
                Code JS (parse JSON)
                        ¦
                        v
            Send a new email (Resend)
        (récapitulatif + suggestions + lettre)



---

## Ce que fait la V2

* Réception d'une offre d'alternance via formulaire n8n (entreprise, poste, description libre).
* Extraction automatique et structuration des informations clés de l'offre via LLM (Claude Opus 5), avec classification par domaine (IA, Data Science, UX/UI, Développement, Autre).
* Enregistrement de la candidature via appel HTTP vers une API locale (backend séparé, responsable du stockage en base).
* Lecture en parallèle du CV structuré (`cv_structure.json`) depuis le disque.
* Fusion (`Merge`) des données de l'offre et du CV pour alimenter une seconde chaîne LLM.
* Génération via Claude Sonnet 4.6 :
  * identification des points forts du CV pertinents pour l'offre,
  * suggestions concrètes d'ajustement du CV,
  * rédaction d'une lettre de motivation complète et personnalisée (250-350 mots).
* Envoi automatique d'un email récapitulatif (via Resend) contenant l'offre, les suggestions et la lettre générée.

---

## Pourquoi une base de données (et pas un simple fichier plat) ?

* **Découplage** : le workflow n8n ne gère pas directement la logique de persistance (dédoublonnage, schéma de la base), déléguée à un service dédié.
* **Évolutivité** : permet de faire évoluer le stockage (SQLite ? autre SGBD) sans toucher au workflow n8n.
* **Réutilisabilité** : l'API `/candidature` peut être appelée par d'autres sources que ce workflow.

---

## Points de vigilance actuels (limites connues de la v2.0)

- Le nœud `HTTP Request` n'a pas de branche de sortie connectée (`"main": [[]]`) — la réponse de l'API n'est pas exploitée actuellement dans le workflow.
- Deux blocs de parsing JSON identiques (`Code in JavaScript` / `Code in JavaScript1`) — factorisation possible.
- Dépendance à un chemin de fichier local en dur (`C:\Users\loise\...`) pour le CV — non portable en l'état.

---

## Évolutions prévues (Roadmap)

- [ ] Exploiter la réponse de l'API HTTP (confirmation d'enregistrement, gestion des doublons visible dans n8n).
- [ ] Dashboard de visualisation de l'état des candidatures.
- [ ] Rendre le chemin du CV configurable (variable d'environnement plutôt que chemin en dur).
- [ ] Notifications de suivi (relance après X jours sans réponse).
- [ ] Amélioration du scoring de matching offre/CV.

---

## Versionning

Cette version est maintenue sur la branche `v2`, séparée de la branche `main` (V1), pour permettre une comparaison claire entre les deux itérations :

```bash
git checkout main   # V1 — brique de base
git checkout v2     # V2 — pipeline complet avec IA + stockage
git diff main v2    # comparer les différences
