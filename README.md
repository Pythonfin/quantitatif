Quantitative calculations

Auteur: Matthew Wright, CPA, PSM, ACA

Ce logiciel crée des calculs quantitatifs avec des résultats de séries chronologiques dans un format de sortie graphique.

Pour exécuter ce programme :

#1) Rendez poetry opérationnelle pour votre environnement
pip install poetry
python -m poetry lock --no-update
python -m poetry install

#2) Programme en cours
Pour l'argument index, les options actuelles sont :
S&P 500 Index: "^GSPC"
Dow Jones Industrial Average: "^DJI"
Nasdaq Composite: "^IXIC"
Russell 2000 Index: "^RUT"
MSCI Emerging Markets Index: "^EEM"
CBOE Volatility Index (VIX): "^VIX"

Pour les tickers, créez une liste du NYSE.

commence: YYYY-MM-DD format

intervalle_dates = YYYY-MM-DD format de la fin de la première période
periods= # Nombre de périodes de comparaison
freq = Intervalles de fréquence valides :
[1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
Exemples de résultats:

tickers = ["SCGLY", "BNPQY", "RNLSY", "LRLCY", "SBGSY", "VEOEY"]
index = "^GSPC"
commence = '2020-01-01'
intervalle_dates = pd.date_range('2021-01-31', periods=24, freq='M')
