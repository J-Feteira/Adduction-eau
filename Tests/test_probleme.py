#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Tests de la classe Probleme.
"""

import pytest
import pandas as pd
import numpy as np
from Adduction_eau import Probleme


@pytest.fixture
def Reseau():
    """Réseau pour tous les tests."""
    canalisation_0 = ("source", "A", 10)
    canalisation_1 = ("A", "C", 5)
    canalisation_2 = ("B", "D", 4)
    canalisation_3 = ("C", "D", 2)
    canalisation_4 = ("D", "puit", 10)
    return [canalisation_0, canalisation_1, canalisation_2, canalisation_3, canalisation_4]


def test_verification_capacite():
    """La capacité doit être positive."""
    with pytest.raises(ValueError):
        Probleme([("A", "B", -1), ("C", "D", 2)])


def test_instanciation(Reseau):
    """Création."""
    probleme = Probleme(reseau=Reseau)
    assert isinstance(probleme, Probleme)
    assert probleme._reseau == Reseau
        

def test_egalite(Reseau):
    """Doit être différent de l'identité."""
    probleme1 = Probleme(Reseau)
    probleme2 = Probleme(Reseau)
    assert probleme1 == probleme2
    
    
def test_validation_doublon(Reseau):
    """Vérifie la détection de deux canalisations similaires."""
    s, a, b, c, p = Reseau
    d = ("A", "C", 5)
    with pytest.raises(ValueError):
        Probleme([s, a, b, c, d, p])
        

def test_repr():
    """Teste le repr."""
    probleme = Probleme(reseau=[('A', 'B', 2)])
    assert (
        repr(probleme)
        == "Probleme(reseau=[('A', 'B', 2)])"
    )

    
def test_encode():
    """Teste l'encodage d'une ligne."""
    correspondance = {
        "A / B / 1": ("A", "B", 1),
        "C / D / 8": ("C", "D", 8)
    }
    for entree, attendu in correspondance.items():
        assert attendu == Probleme._encode(entree)


def test_constructeur(Reseau):
    """Constructeur alternatif."""
    entree = """
source / A / 10
A / C / 5
B / D / 4
C / D / 2
D / puit / 10
"""
    probleme = Probleme.par_str(entree)
    assert probleme == Probleme(Reseau)
    
    
def test_table_depart(Reseau):
    """Test l'instance table_depart."""
    a,b,c,d = "ABCD"
    probleme = Probleme(reseau=Reseau)
    test = pd.DataFrame(
        data=np.zeros((5, 5)),
        index=["source",a,c,b,d], 
        columns=[a,c,b,d,"puit"]
    )
    test.loc["source", "A"] = 10
    test.loc["A", "C"] = 5
    test.loc["B", "D"] = 4
    test.loc["C", "D"] = 2
    test.loc["D", "puit"] = 10
    assert probleme.table_depart().equals(test)

    
def test_recupere_noeuds_capacite_insuffisante_toutes_suffisantes():
    """Test l'instance _recupere_noeuds_capacite_insuffisante lorsque toutes les capacités sont suffisantes."""
    entree = """
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
"""
    probleme = Probleme.par_str(entree)
    assert probleme._recupere_noeuds_capacite_insuffisante() == list()

        
def test_recupere_noeuds_capacite_insuffisante_certaines_insuffisantes():
    """Test la méthode _recupere_noeuds_capacite_insuffisante lorsque plusieurs capacités sont insuffisantes."""
    entree = """
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
E / F / 2
E / H / 2
E / I / 2
F / G / 4
F / I / 4
G / I / 20
H / J / 20
I / K / 2
I / L / 2
K / J / 20
J / puit / 15
K / puit / 20
L / puit / 15
"""
    probleme = Probleme.par_str(entree)
    liste = [('E', 'H'), ('I', 'K'), ('I', 'L')]
    assert probleme._recupere_noeuds_capacite_insuffisante() == liste
    
    
    def test_recupere_noeud_non_alimente_par_source(Reseau):
        """Teste la méthode statique _recupere_noeud_non_alimente_par_source lorsque tous les sommets ne sont pas alimentés par la source."""
        probleme = Probleme(reseau=Reseau)
        test = Probleme._recupere_noeud_non_alimente_par_source(probleme.table_depart())
        resultat = [1, 2, 3, 4]
        assert test == resultat
    
    
    def test_recupere_noeud_non_alimente_par_source_tout_alimente():
        """Teste la méthode statique _recupere_noeud_non_alimente_par_source lorsque tous les sommets sont alimentés par la source."""
        a,b,c,d = "ABCD"
        table = pd.DataFrame(
            data=np.zeros([
                [5, 5, 5, 5, 2],
                [5, 5, 5, 5, 0],
                [5, 5, 5, 5, 0],
                [5, 5, 5, 5, 0],
                [5, 5, 5, 5, 0],
            ]
            ),
            index=["source",a,c,b,d], 
            columns=[a,c,b,d,"puit"]
        )
        test = Probleme._recupere_noeud_non_alimente_par_source(table)
        assert test == []