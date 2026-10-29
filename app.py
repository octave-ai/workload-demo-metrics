"""Standalone demo: fixed sample data, no persistence or external services."""
from flask import Flask, jsonify, render_template

app = Flask(__name__)
SOURCE = "metrics"
VERSION = "1.0.0"


@app.get("/healthz")
def health():
    """Identify this demo without exposing host, environment, or credentials."""
    return jsonify(status="ok", source=SOURCE, version=VERSION, synthetic=True)

ROWS = [
    {
        "label": "Messages traités",
        "value": "128",
        "detail": "Jeu de données fictif"
    },
    {
        "label": "Qualité des données",
        "value": "99,2 %",
        "detail": "Valeur de démonstration"
    },
    {
        "label": "Temps de traitement",
        "value": "42 ms",
        "detail": "Pas une mesure réelle"
    }
]


@app.get("/")
def home():
    """Render a visibly distinct demo for this Git source."""
    return render_template(
        "index.html", title="Demo Metrics", source=SOURCE,
        version=VERSION, accent="#72d5ff", description='Un petit tableau de bord, fourni par un premier dépôt Git.', rows=ROWS,
    )
