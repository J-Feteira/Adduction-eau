#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.
Exemple:

>>> from Adduction_eau import Probleme
>>> from Adduction_eau import ressort_table_apres_travaux, transforme_table, visualisation_graphe_flots_maximaux, recupere_ville_flot_maximal_faible

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
... D / F / 4
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

>>> probleme.affiche()
   Problème d'adduction d'eau   
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ Initial ┃ Arrivée ┃ Capacité ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ source  │ A       │ 15       │
│ source  │ B       │ 15       │
│ source  │ C       │ 15       │
│ source  │ D       │ 10       │
│ C       │ A       │ 5        │
│ C       │ F       │ 5        │
│ A       │ E       │ 7        │
│ B       │ F       │ 10       │
│ B       │ G       │ 7        │
│ D       │ G       │ 10       │
│ D       │ F       │ 4        │
│ E       │ F       │ 5        │
│ E       │ H       │ 4        │
│ E       │ I       │ 15       │
│ F       │ G       │ 5        │
│ F       │ I       │ 15       │
│ G       │ I       │ 15       │
│ H       │ J       │ 7        │
│ I       │ K       │ 30       │
│ I       │ L       │ 4        │
│ K       │ J       │ 10       │
│ J       │ puit    │ 15       │
│ K       │ puit    │ 20       │
│ L       │ puit    │ 15       │
└─────────┴─────────┴──────────┘


>>> debut = probleme.table_depart()
>>> visualisation_graphe_flots_maximaux(debut)

>>> recupere_ville_flot_maximal_faible(probleme)
[('J', 15), ('L', 15)]

>>> solution = ressort_table_apres_travaux(probleme)
>>> solution_finale = Probleme(transforme_table(solution))
>>> recupere_ville_flot_maximal_faible(solution_finale)
[]

>>> solution_finale.affiche()
   Problème d'adduction d'eau   
┏━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┓
┃ Initial ┃ Arrivée ┃ Capacité ┃
┡━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━┩
│ source  │ A       │ 15.0     │
│ source  │ B       │ 15.0     │
│ source  │ C       │ 15.0     │
│ source  │ D       │ 10.0     │
│ A       │ E       │ 20.0     │
│ B       │ F       │ 10.0     │
│ B       │ G       │ 7.0      │
│ C       │ A       │ 5.0      │
│ C       │ F       │ 5.0      │
│ D       │ F       │ 4.0      │
│ D       │ G       │ 10.0     │
│ E       │ F       │ 5.0      │
│ E       │ H       │ 7.0      │
│ E       │ I       │ 15.0     │
│ F       │ G       │ 5.0      │
│ F       │ I       │ 15.0     │
│ G       │ I       │ 15.0     │
│ H       │ J       │ 7.0      │
│ I       │ K       │ 30.0     │
│ I       │ L       │ 15.0     │
│ J       │ puit    │ 15.0     │
│ K       │ J       │ 10.0     │
│ K       │ puit    │ 20.0     │
│ L       │ puit    │ 15.0     │
└─────────┴─────────┴──────────┘

>>> visualisation_graphe_flots_maximaux(solution);
"""



from .probleme import Probleme
from .algorithme import ressort_table_apres_travaux, transforme_table, visualisation_graphe_flots_maximaux, recupere_ville_flot_maximal_faible

__all__ = [
    "Probleme", "ressort_table_apres_travaux", "transforme_table", 
    "visualisation_graphe_flots_maximaux", "recupere_ville_flot_maximal_faible"
]