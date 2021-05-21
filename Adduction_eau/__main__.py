#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Démonstration du module.
"""

from Adduction_eau import Probleme
from Adduction_eau import ressort_table_apres_travaux, transforme_table, visualisation_graphe_flots_maximaux, recupere_ville_flot_maximal_faible

probleme = Probleme.par_str(
    """
source / A / 15
source / B / 15
source / C / 15
source / D / 10
C / A / 5
C / F / 5 
A / E / 7
B / F / 10
B / G / 7
D / G / 10
D / F / 4
E / F / 5
E / H / 4
E / I / 15
F / G / 5
F / I / 15
G / I / 15
H / J / 7
I / K / 30
I / L / 4
K / J / 10
J / puit / 15
K / puit / 20
L / puit / 15
"""
)

probleme.affiche()
recupere_ville_flot_maximal_faible(probleme)
debut = probleme.table_depart()
visualisation_graphe_flots_maximaux(debut)

solution = ressort_table_apres_travaux(probleme)
visualisation_graphe_flots_maximaux(solution)

solution_finale = Probleme(transforme_table(solution))
recupere_ville_flot_maximal_faible(solution_finale)
solution_finale.affiche()