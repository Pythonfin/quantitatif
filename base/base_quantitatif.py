#!/usr/bin/env python3
# python base_quantitatif.py
# Auteur: Matthew Wright, CPA, PSM, ACA - pythonfin@proton.me
# Version: 1.0

# importations standard
from typing import Tuple, Any
from datetime import datetime

# importations de tiers
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# importations d'applications locales


class QuantitatifCalculs:
    """
    Classe de base

    Paramètres
    ----------
    self.yf_data : tuple
        Tuple[pd.DataFrame] contenant les données yf.download stock ticker de l'indice de temps
    self.tickers : list
        les symboles boursiers à utiliser dans les calculs
    """

    def __init__(self, tickers):
        self.yf_data = tuple()
        self.tickers = tickers

    def charger_donnees(self, index: str, **kwargs: Any):
        """
        Récupère les données historiques pour les tickers et ^GSPC en un seul appel.
        yf.download s'appuie sur une chaîne de tickers séparés par un espace, par exemple 'SCGLY PFE'.

        Args:
            :param index: indice comparatif à utiliser pour le calcul du bêta
            :type index: "str"

            :param kwargs: Arguments facultatifs à passer à la fonction yf.download.

            :Arguments de mots-clés:
                start (str): La date de début au format YYYY-MM-DD
                end (str): La date de fin au format YYYY-MM-DD
                group_by (str): spécifie comment regrouper les données téléchargées
                    (par exemple "ticker" pour le regroupement par symbole de téléscripteur,
                    "column" pour le regroupement par colonne de données)
                interval = '1d' : La période d'intervalle de temps à utiliser dans les calculs bêta.
                    Intervalles valides: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
                auto_adjust (bool): ajuster automatiquement les calculs (la valeur par défaut est True)
                prepost (bool): inclure les données de négociation avant et après le marché (par défaut, False)
                threads (int): spécifiant le nombre de threads à utiliser pour le téléchargement (1 par défaut)

        Retours:
            None: Ceci charge juste les données df dans self.yf_data

        Raises:
            ValueError: Si ticker n'est pas trouvé, ou s'il y a une erreur dans la récupération des données.

        Exemple :
            >>> self.charger_donnees("^GSPC", start='2020-01-01', end='2020-12-31', interval='1d')
        """
        try:
            stock_str = " ".join(self.tickers)

            data: Tuple[pd.DataFrame] = yf.download(stock_str + " " + index, **kwargs, group_by='ticker')

            # Vérifier si les données ne sont pas vides
            if data.empty:
                raise ValueError("yf.download ne s'est pas terminé correctement pour la liste de téléscripteurs")

            # Vérifier si les données d'index sont disponibles
            if index not in data:
                raise KeyError(f"Données pour le {index} n'était pas chargé")

            self.yf_data = data

        except (KeyError, ValueError) as e:
            print("Error:", e)
            return None

        except Exception as e:
            print("Unknown error:", e)
            return None


class QuantitatifBeta(QuantitatifCalculs):
    """ Commencez par les questions de l'analyse quantitative de base"""
    def __init__(self, tickers):
        super().__init__(tickers)
        self.betas = []

    def preparer_beta_calculs(self, index: str, date_range: pd.DatetimeIndex, commencer: str):
        """
        effectuer toutes les préparations du calcul du bêta

        Args:
            :param index: indice comparatif à utiliser pour le calcul du bêta
            :type index: "str"

            :param commencer: date de début pour ce segment des calculs bêta
            :type commencer: "str"

            :param date_range: Pandas df de l'intégralité de l'index date-heure sur lequel il faut itérer
            :type date_range: "pd.DatetimeIndex"

        Retourne:
            dict: Les valeurs bêta des tickers, avec deux décimales.

        Raises:
            ValueError: Si le téléscripteur n'est pas trouvé,
                        ou s'il y a une erreur dans la récupération des données.
            KeyError: Si le téléscripteur n'a pas été chargé dans le fichier yf.download
        """
        try:
            df_betas = []

            # Vérifiez que la plage de dates n'est pas vide.
            if date_range.empty:
                raise ValueError("pas de plage de dates - vide DateTimeIndex")

            for end_date in date_range:
                betas = self._calculs_beta(index=index, commencer=commencer, fin=end_date)

                df = pd.DataFrame(betas, index=[end_date])
                df_betas.append(df)

                print(f'\nla date du jour est {end_date}')
                for ticker, beta_val in betas.items():
                    print(f'Ticker: {ticker} - avec le bêta de {beta_val}')

            self.betas = pd.concat(df_betas)

        except ValueError as e:
            print(f"Erreur: {e}")

        except Exception as e:
            print("Erreur inconnue:", e)
            return None

    def _calculs_beta(self, index: str, commencer: str, fin: str) -> dict[str, float] | None:
        """
        Bêta : mesure de la volatilité d'une action par rapport à l'ensemble du marché
        (métrique typique SP500)
        Calculez le bêta pour un symbole boursier donné.

        Args:
            :param index: indice comparatif à utiliser pour le calcul du bêta
            :type index: "str"

            :param commencer: date de début pour ce segment des calculs bêta
            :type commencer: "str"

            :param fin: date de fin pour ce segment des calculs bêta
            :type fin: "str"

        Retourne:
            dict: les valeurs bêta des tickers, en deux décimales

        Raises:
            ValueError: Si le téléscripteur n'est pas trouvé,
                        ou s'il y a une erreur dans la récupération des données.
            KeyError: Si le téléscripteur n'a pas été chargé dans le fichier yf.download
        """

        try:
            betas_dict = {}

            # boolean mask filtre par jour
            mask = (self.yf_data.index >= commencer) & (self.yf_data.index <= fin)
            df_yf_data = self.yf_data.loc[mask]

            # Effectuer des contrôles d'erreurs
            if df_yf_data.empty:
                err_str = "yf.download ne s'est pas terminé correctement pour la liste de téléscripteurs"
                raise ValueError(err_str)

            if index not in df_yf_data:
                raise KeyError(f"Données pour le {index} n'était pas chargé")

            # Calculer les rendements des indices en utilisant des opérations vectorielles
            sp500_returns = df_yf_data[index]['Adj Close'] \
                .values[1:] / df_yf_data[index]['Adj Close'].values[:-1] - 1

            for ticker in self.tickers:
                if ticker not in df_yf_data:
                    raise KeyError(f"data for {ticker} wasn't loaded")

                # Calculer les rendements quotidiens en utilisant des opérations vectorielles
                stock_returns = df_yf_data[ticker]['Adj Close'] \
                    .values[1:] / df_yf_data[ticker]['Adj Close'].values[:-1] - 1

                # Vérifiez que les données de retour sont suffisantes pour effectuer les calculs de bêta.
                if len(stock_returns) < 2 or len(sp500_returns) < 2:
                    raise ValueError(
                        f"peut pas calculer le bêta pour {ticker} - manque de données suffisantes")

                # Calculez le bêta de l'action
                beta = np.cov(stock_returns, sp500_returns)[0, 1] / np.var(sp500_returns)

                betas_dict[ticker] = round(beta, 2)

            return betas_dict

        except (KeyError, ValueError) as e:
            print("Error:", e)
            return None

        except Exception as e:
            print("Unknown error:", e)
            return None

    def plot_betas(self):
        """
        En utilisant les valeurs de bêta actuelles, crée un graphique de résultats
        des bêta en utilisant matplotlib et trace les valeurs de self.tickers.
        """

        try:
            if not isinstance(self.betas, pd.DataFrame):
                print("Erreur : calculate_beta.betas n'est pas un DataFrame")
                return None

            plt.plot(self.betas.index, self.betas)

            plt.title('Bêta des actions au fil du temps')
            plt.xlabel('Date')
            plt.ylabel('Bêta')

            plt.legend(self.tickers, loc='lower left')

            # Créez un timbre horodateur au format "YYYY-MM-DD_HHM-MM-SS"
            # et sauvegardez-le .png des résultats de bêta.
            now = datetime.now()
            datetime_stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            save_str = 'resultat/beta_' + datetime_stamp + '.png'

            plt.savefig(save_str)

        except Exception as e:
            print(f'Error: {e}')
            return None
