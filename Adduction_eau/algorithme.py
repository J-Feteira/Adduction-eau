#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Contient la fonction de résolution de l'exercice d'adduction d'eau ainsi qu'une fonction de visualisation du graphe et de ses flots.

Fonctions principales :
- ressort_table_apres_travaux
- visualisation_graphe_flots_maximaux
- transforme_table
- recupere_ville_flot_maximal_faible

Fonctions secondaires :
- _modifie_reseau
- _recupere_sommets
- _recupere_flots_maximaux
"""

from typing import List, Dict, Tuple
from Adduction_eau import Probleme
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
import pandas as pd


def _modifie_reseau(probleme: Probleme) -> pd.DataFrame:
    """
    Modifie les capacités des arrêtes de façon à voir quel capacité mettre selon le flot maximal.
    
    Exemple :
>>> from Adduction_eau.algorithme import _modifie_reseau
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> _modifie_reseau(probleme)
|      | A  | B  | C  | D  | F  | E  | G  | H  | I  | J  | K  | L  |puit|
|------|----|----|----|----|----|----|----|----|----|----|----|----|----|
|source|15.0|15.0|15.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| A    | 0.0| 0.0| 0.0| 0.0| 0.0|57.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| B    | 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 7.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| C    | 5.0| 0.0| 0.0| 0.0| 5.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| D    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| F    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 5.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| E    | 0.0| 0.0| 0.0| 0.0| 5.0| 0.0| 0.0|54.0|15.0| 0.0| 0.0| 0.0| 0.0|
| G    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| H    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 7.0| 0.0| 0.0| 0.0|
| I    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|30.0|54.0| 0.0|
| J    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
| K    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0|20.0|
| L    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
    """
    table = probleme.table_depart()
    for depart, arrivee in probleme._recupere_noeuds_capacite_insuffisante():
        table.loc[depart, arrivee] += 50
    return table


def ressort_table_apres_travaux(probleme: Probleme) -> pd.DataFrame:
    """Ressort la table lorsque les travaux sont finis.
    
    Exemple :
>>> from Adduction_eau import ressort_table_apres_travaux
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> ressort_table_apres_travaux(probleme)
|      | A  | B  | C  | D  | F  | E  | G  | H  | I  | J  | K  | L  |puit|
|------|----|----|----|----|----|----|----|----|----|----|----|----|----|
|source|15.0|15.0|15.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| A    | 0.0| 0.0| 0.0| 0.0| 0.0|20.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| B    | 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 7.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| C    | 5.0| 0.0| 0.0| 0.0| 5.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| D    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| F    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 5.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| E    | 0.0| 0.0| 0.0| 0.0| 5.0| 0.0| 0.0| 7.0|15.0| 0.0| 0.0| 0.0| 0.0|
| G    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| H    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 7.0| 0.0| 0.0| 0.0|
| I    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|30.0|15.0| 0.0|
| J    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
| K    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0|20.0|
| L    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
    """
    table = _modifie_reseau(probleme)
    flots_maximaux = _recupere_flots_maximaux(table)
    for depart, arrivee in probleme._recupere_noeuds_capacite_insuffisante():
        for arrete, capacite in flots_maximaux.items():
            if (depart, arrivee) == arrete:
                table.loc[depart, arrivee] = capacite
                break
    return table


def transforme_table(table: pd.DataFrame) -> List[Tuple[str, str, float]]:
    """Transforme la table en liste de tuples.
    
    Exemple :
>>> from Adduction_eau import transforme_table
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> transforme_table(probleme.table_depart())
[('source', 'A', 15.0),
 ('source', 'B', 15.0),
 ('source', 'C', 15.0),
 ('source', 'D', 10.0),
 ('A', 'E', 7.0),
 ('B', 'F', 10.0),
 ('B', 'G', 7.0),
 ('C', 'A', 5.0),
 ('C', 'F', 5.0),
 ('D', 'G', 10.0),
 ('E', 'F', 5.0),
 ('E', 'H', 4.0),
 ('E', 'I', 15.0),
 ('F', 'G', 5.0),
 ('F', 'I', 15.0),
 ('G', 'I', 15.0),
 ('H', 'J', 7.0),
 ('I', 'K', 30.0),
 ('I', 'L', 4.0),
 ('J', 'puit', 15.0),
 ('K', 'J', 10.0),
 ('K', 'puit', 20.0),
 ('L', 'puit', 15.0)]
    """
    colonnes = list(table.loc[:])
    lignes = list(table.index)
    liste_tuple = list()
    for ligne in lignes:
        for colonne in colonnes:
            if table.loc[ligne, colonne] != 0:
                liste_tuple.append((ligne, colonne, table.loc[ligne, colonne]))
    return liste_tuple


def _recupere_sommets(table: pd.DataFrame) -> nx.DiGraph:
    """Récupère les sommets afin de dessiner le graphe.
    
    Exemple :
>>> from Adduction_eau.algorithme import _recupere_sommets
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> _recupere_sommets(probleme.table_depart())
<networkx.classes.digraph.DiGraph at 0x24f5c8a7f70>

>>> list(_recupere_sommets(probleme.table_depart()))
['source', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'puit']
    """
    reseau = nx.DiGraph()
    reseau.add_weighted_edges_from(transforme_table(table), weight="capacite")
    return reseau


def _recupere_flots_maximaux(table: pd.DataFrame) -> Dict[Tuple[str, str], float]:
    """Fonction qui récupère les flots maximaux du graphe.
    
    Exemple :
>>> from Adduction_eau.algorithme import _recupere_flots_maximaux
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> _recupere_flots_maximaux(probleme.table_depart())
{('source', 'A'): 2.0,
 ('source', 'B'): 15.0,
 ('source', 'C'): 10.0,
 ('source', 'D'): 10.0,
 ('A', 'E'): 7.0,
 ('B', 'F'): 10.0,
 ('B', 'G'): 5.0,
 ('C', 'A'): 5.0,
 ('C', 'F'): 5.0,
 ('D', 'G'): 10.0,
 ('E', 'F'): 0,
 ('E', 'H'): 4.0,
 ('E', 'I'): 3.0,
 ('F', 'G'): 0,
 ('F', 'I'): 15.0,
 ('G', 'I'): 15.0,
 ('H', 'J'): 4.0,
 ('I', 'K'): 30.0,
 ('I', 'L'): 3.0,
 ('J', 'puit'): 14.0,
 ('K', 'J'): 10.0,
 ('K', 'puit'): 20.0,
 ('L', 'puit'): 3.0}
    """
    _, repartition_flot = nx.maximum_flow(
        flowG=_recupere_sommets(table),
        _s="source",
        _t="puit", 
        capacity="capacite"
    )
    liste_flots = {}
    for cle, items in repartition_flot.items():
        for item_1, poids_item_1 in items.items():
            liste_flots[(cle, item_1)] = poids_item_1
    return liste_flots


def recupere_ville_flot_maximal_faible(probleme: Probleme) -> List[Tuple[str, int]]:
    """Récupère les villes dont le flot d'arrivée d'eau n'est pas maximal.
    
    Exemple :
>>> from Adduction_eau.algorithme import recupere_ville_flot_maximal_faible
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> recupere_ville_flot_maximal_faible(probleme)
[('J', 15), ('L', 15)]
    """
    villes_non_alimentees = list()
    reseau_flots = _recupere_flots_maximaux(probleme.table_depart())
    arretes = dict()
    for initial, arrivee, capacite in probleme._reseau:
        if arrivee == "puit":
            arretes[(initial, arrivee)] = capacite
            
    for canalisation_arrivee in arretes:
        if arretes.get(canalisation_arrivee) != reseau_flots.get(canalisation_arrivee):
            villes_non_alimentees.append(
                (canalisation_arrivee[0], arretes.get(canalisation_arrivee))
            )
    return villes_non_alimentees


def visualisation_graphe_flots_maximaux(table: pd.DataFrame) -> plt.plot:
    """Fonction afin de créer le graphe et visualiser les flots maximaux de ce dernier.
    
    Exemple :
>>> from Adduction_eau import visualisation_graphe_flots_maximaux
>>> from Adduction_eau import Probleme

>>> probleme = Probleme.par_str(
...    '''
... source / A / 15
... source / B / 15
... source / C / 15
... source / D / 10
... C / A / 5
... C / F / 5 
... A / E / 7
... B / F / 10
... B / G / 7
... D / G / 10
... E / F / 5
... E / H / 4
... E / I / 15
... F / G / 5
... F / I / 15
... G / I / 15
... H / J / 7
... I / K / 30
... I / L / 4
... K / J / 10
... J / puit / 15
... K / puit / 20
... L / puit / 15
... '''
... )

>>> visualisation_graphe_flots_maximaux(probleme.table_depart())

    """
    figure, repere = plt.subplots()
    point_rouge = mpatches.Patch(color="red")
    point_bleu = mpatches.Patch(color="blue")
    arretes = _recupere_sommets(table)
    positions = nx.circular_layout(G=arretes)
    nx.draw_networkx(G=arretes, pos=positions, ax=repere)
    capacites = nx.get_edge_attributes(G=arretes, name="capacite")
    liste_flots = _recupere_flots_maximaux(table)
    nx.draw_networkx_edge_labels(G=arretes, pos=positions, edge_labels=capacites,
                                verticalalignment="top", horizontalalignment="right",
                                font_color="blue")
    nx.draw_networkx_edge_labels(G=arretes, pos=positions, edge_labels=liste_flots,
                                font_color = "red", verticalalignment="bottom",
                                horizontalalignment="left")
    repere.legend((point_rouge, point_bleu), ("Flots", "Capacités"), fontsize="x-large")
    repere.set_title("Graphe orienté avec capacités et flots", color="yellow");