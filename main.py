#!/usr/bin/env python3
# python main.py
# Auteur: Matthew Wright, CPA, PSM, ACA - pythonfin@proton.me
# Version: 1.0.0

# importations standard

# importations de tiers
import pandas as pd

# importations d'applications locales
from base.base_quantitatif import QuantitatifBeta


if __name__ == '__main__':

    # paramètres du programme initial
    tickers = ["SCGLY", "BNPQY", "RNLSY", "LRLCY", "SBGSY", "VEOEY"]
    calculs = QuantitatifBeta(tickers)

    index = "^GSPC"
    commence = '2020-01-01'
    intervalle_dates = pd.date_range('2021-01-31', periods=24, freq='M')

    # charger les valeurs des données de base
    calculs.charger_donnees(index=index, start=commence, end=intervalle_dates[-1], interval='1d')

    # effectuer des calculs
    calculs.preparer_beta_calculs(index=index, date_range=intervalle_dates, commencer=commence)

    # résultats de sortie
    calculs.plot_betas()
