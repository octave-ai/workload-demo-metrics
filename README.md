# Workload demo — Metrics

Application Flask autonome pour démontrer plusieurs sources Git dans un même
espace de déploiement. **Toutes les données sont fictives** : aucune base,
aucun secret, aucune donnée d'entreprise et aucun appel à un service externe.

Cette application se distingue de sa compagne
[`workload-demo-events`](https://github.com/octave-ai/workload-demo-events)
par son identifiant, son contenu et sa couleur. Chacune peut être synchronisée,
déployée ou arrêtée indépendamment.

## Lancer en local

Python **3.10 ou plus récent** :

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
gunicorn --bind 127.0.0.1:8080 --workers 1 --access-logfile - app:app
```

Ouvrir `http://127.0.0.1:8080/`. L'endpoint `/healthz` retourne l'identifiant
`metrics`, la version et le caractère fictif des données. Aucun endpoint d'écriture
n'est exposé. Les liens et assets utilisent le préfixe WSGI (`SCRIPT_NAME`)
transmis par l'hébergement, sans chemin absolu codé en dur.

## Ajouter comme source Git

Dans l'interface d'administration, créer une **nouvelle** source :

- ID de source suggéré : `demo-metrics`.
- URL : `https://github.com/octave-ai/workload-demo-metrics.git`.
- Branche de configuration : `main`.
- Fichier de workloads : `production.yml`.
- Authentification Git : aucune, ce dépôt est public.

Ne pas modifier ni remplacer la source `default`. Le workload `demo-metrics` et
son sous-chemin sont distincts de ceux de l'autre dépôt pour éviter les conflits.
Le runtime Gunicorn doit écouter le port fourni par l'hébergement (`PORT`).
Les dépendances sont installées depuis `requirements.txt` : le runtime doit donc
pouvoir récupérer ces paquets via son registre Python.

## Scénario de démonstration

1. Ajouter et synchroniser ce dépôt ainsi que le dépôt compagnon.
2. Constater que les deux workloads portent des identifiants de source distincts.
3. Déployer en environnement **test** : la référence `preprod` suit `main`.
4. Ouvrir les deux pages ; constater les contenus, sources et couleurs différents.
5. Consulter les logs HTTP puis arrêter un seul workload, sans arrêter l'autre.
6. Facultatif : déployer la version stable `v1.0.1` en environnement production.

Le tag `v1.0.1` est la référence stable de l'exemple ; `main` reste la référence de
préproduction. Pour montrer une mise à jour, modifier une donnée ou la version
sur `main`, synchroniser cette source puis redéployer son environnement test.
Ne pas déplacer le tag stable pour simuler une mise à jour.

La création du dépôt ne l'enregistre pas automatiquement dans un cluster et ne
déploie aucun workload. Ajouter/synchroniser/déployer sont des actions séparées.

## Licence

MIT — voir [LICENSE](LICENSE).
