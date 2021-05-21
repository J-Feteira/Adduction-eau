#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests du module algorithme qui permet de résoudre le problème d'adduction d'eau.
"""

import pytest
from Adduction_eau import Probleme, ressort_table_apres_travaux, transforme_table, recupere_ville_flot_maximal_faible
from Adduction_eau.algorithme import _modifie_reseau, _recupere_sommets, _recupere_flots_maximaux
import numpy as np
import pandas as pd
import networkx as nx


@pytest.fixture
def Reseau():
    """Réseau pour tous les tests."""
    canalisation_0 = ("source", "D", 30.)
    canalisation_1 = ("D", "E", 32.)
    canalisation_2 = ("E", "F", 21.)
    canalisation_3 = ("F", "G", 22.)
    canalisation_4 = ("G", "H", 23.)
    canalisation_5 = ("H", "I", 12.)
    canalisation_6 = ("I", "J", 35.)
    canalisation_7 = ("J", "K", 30.)
    canalisation_8 = ("K", "L", 2.)
    canalisation_9 = ("J", "puit", 30.)
    canalisation_10 = ("K", "puit", 10.)
    canalisation_11 = ("L", "puit", 10.)
    return [
        canalisation_0, canalisation_1, canalisation_2, canalisation_3, canalisation_4, canalisation_5,
        canalisation_6, canalisation_7, canalisation_8, canalisation_9, canalisation_10, canalisation_11
    ]


def test_modifie_reseau(Reseau):
    """Teste la modification du réseau."""
    probleme = Probleme(reseau=Reseau)
    d,e,f,g,h,i,j,k,l = "DEFGHIJKL"
    resultat = pd.DataFrame(
        data=np.array(
            [
                [30., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 32., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 21., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 22., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 23., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 12., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 35., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0., 30., 0., 30.],
                [0., 0., 0., 0., 0., 0., 0., 0., 52., 10.],
                [0., 0., 0., 0., 0., 0., 0., 0., 0., 10.]
            ]
        ),
        index=["source",d,e,f,g,h,i,j,k,l], 
        columns=[d,e,f,g,h,i,j,k,l,"puit"]
    )
    assert _modifie_reseau(probleme).equals(resultat)

    
def test_ressort_table_apres_travaux(Reseau):
    """Teste la fonction ressort_table_apres_travaux."""
    probleme = Probleme(reseau=Reseau)
    d,e,f,g,h,i,j,k,l = "DEFGHIJKL"
    test = pd.DataFrame(
        data=np.array(
            [
                [30., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 32., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 21., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 22., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 23., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 12., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 35., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0., 30., 0., 30.],
                [0., 0., 0., 0., 0., 0., 0., 0., 0., 10.],
                [0., 0., 0., 0., 0., 0., 0., 0., 0., 10.]
            ]
        ),
        index=["source",d,e,f,g,h,i,j,k,l], 
        columns=[d,e,f,g,h,i,j,k,l,"puit"]
    )
    assert ressort_table_apres_travaux(probleme).equals(test)
    
    
def test_transforme_table(Reseau):
    """Teste la fonction transforme table pour transformer une table en liste de tuples."""
    d,e,f,g,h,i,j,k,l = "DEFGHIJKL"
    resultat = pd.DataFrame(
        data=np.array(
            [
                [30., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 32., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 21., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 22., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 23., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 12., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 35., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0., 30., 0., 30.],
                [0., 0., 0., 0., 0., 0., 0., 0., 2., 10.],
                [0., 0., 0., 0., 0., 0., 0., 0., 0., 10.]
            ]
        ),
        index=["source",d,e,f,g,h,i,j,k,l], 
        columns=[d,e,f,g,h,i,j,k,l,"puit"]
    )
    for arrete in transforme_table(resultat):
        if arrete not in Reseau:
            raise AssertionError
    
    
def test_recupere_sommets(Reseau):
    """Teste la fonction _recupere_sommets."""
    d,e,f,g,h,i,j,k,l = "DEFGHIJKL"
    resultat = ["source",d,e,f,g,h,i,j,k,"puit",l]
    test = pd.DataFrame(
        data=np.array(
            [
                [30., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 32., 0., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 21., 0., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 22., 0., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 23., 0., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 20., 0., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 35., 0., 0., 0.],
                [0., 0., 0., 0., 0., 0., 0., 30., 0., 30.],
                [0., 0., 0., 0., 0., 0., 0., 0., 20., 10.],
                [0., 0., 0., 0., 0., 0., 0., 0., 0., 10.]
            ]
        ),
        index=["source",d,e,f,g,h,i,j,k,l], 
        columns=[d,e,f,g,h,i,j,k,l,"puit"]
    )
    assert list(_recupere_sommets(test)) == resultat
    

def test_recupere_flots_maximaux(Reseau):
    """Teste la fonction _recupere_flots_maximaux."""
    probleme = Probleme(reseau=Reseau)
    test = _recupere_flots_maximaux(probleme.table_depart())
    resultat = {
        ("source", "D"): 12.0,
        ("D", "E"): 12.0,
        ("E", "F"): 12.0,
        ("F", "G"): 12.0,
        ("G", "H"): 12.0,
        ("H", "I"): 12.0,
        ("I", "J"): 12.0,
        ("J", "K"): 0,
        ("J", "puit"): 12.0,
        ("K", "L"): 0,
        ("K", "puit"): 0,
        ("L", "puit"): 0
    }
    assert test == resultat
    
    
def villes_non_alimentees(Reseau):
    """Test que les villes ne sont pas alimentées correctement."""
    probleme = Probleme(reseau=Reseau)
    depart = probleme.table_depart()
    assert recupere_ville_flot_maximal_faible(probleme) == [("K", 20), ("L", 15)]


def villes_alimentees():
    """Teste lorsque toutes les villes sont alimentées correctement."""
    reseau = Probleme.par_str("""
source / A / 15
source / B / 15
source / C / 15
source / D / 10
C / A / 20
C / F / 20
A / E / 20
B / F / 20
B / G / 20
D / G / 20
D / F / 20
E / F / 20
E / H / 20
E / I / 20
F / G / 20
F / I / 20
G / I / 20
H / J / 20
I / K / 20
I / L / 20
K / J / 20
J / puit / 15
K / puit / 20
L / puit / 15
""")
    assert recupere_ville_flot_maximal_faible(reseau) == []



