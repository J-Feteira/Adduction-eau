#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Classe Probleme permettant de décrire le problème d'adduction d'eau.
"""

from typing import Tuple, List, Any
from rich.table import Table
import numpy as np
import pandas as pd


class Probleme:
    """Crée un graphe pour l'adduction d'eau."""
    def __init__(self, reseau):
        self._reseau = reseau
        self._enleve_doublons()
        self._est_valide()
        
    
    def __repr__(self) -> str:
        """Renvoie la liste de construction."""
        return f"Probleme(reseau={list(self._reseau) !r})"
    
    
    def __str__(self) -> List[Tuple[str, str, int]]:
        """Affiche les canalisations par ligne."""
        return "\n".join(repr(debit) for debit in self._reseau)
    
    
    @staticmethod
    def _encode(ligne: str) -> Tuple[str, str, int]:
        """Encode une ligne de débit.
        
        Exemple :
>>> from Adduction_eau import Probleme
>>> Probleme._encode('''l / a / 12''')
('l', 'a', 12)
        """
        initial, arrivee, capacite = ligne.split("/")
        try:
            capacite_valide = int(capacite.strip())
        except ValueError:
            capacite_valide = float(capacite.strip())
        return (initial.replace(" ", ""), arrivee.replace(" ", ""), capacite_valide)
        
    
    
    @classmethod
    def par_str(cls, message: str) -> "Probleme":
        """Constructeur alternatif par chaine de caractères.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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

Probleme(reseau=[('source', 'A', 15), ('source', 'B', 15), ('source', 'C', 15), ('source', 'D', 10), ('C', 'A', 5), ('C', 'F', 5), ('A', 'E', 7), ('B', 'F', 10), ('B', 'G', 7), ('D', 'G', 10), ('E', 'F', 5), ('E', 'H', 4), ('E', 'I', 15), ('F', 'G', 5), ('F', 'I', 15), ('G', 'I', 15), ('H', 'J', 7), ('I', 'K', 30), ('I', 'L', 4), ('K', 'J', 10), ('J', 'puit', 15), ('K', 'puit', 20), ('L', 'puit', 15)])
        """
        reseau = list()
        for ligne in message.strip().splitlines():
            reseau.append(cls._encode(ligne))
        return cls(reseau)
    
    
    def __eq__(self, autre: Any) -> bool:
        """Teste l'égalité de 2 réseaux."""
        if type(autre) != type(self):
            return False
        return self._reseau == autre._reseau
    
    
    def _est_valide(self) -> None:
        """Vérifie que la capacite est positive."""
        for debit in self._reseau:
            if debit[2] < 0:
                raise ValueError("Toutes les capacités doivent être positives.")
                
    
    def _enleve_doublons(self) -> None:
        """Empêche de mettre des doublons."""
        deja_passer = list()
        for canalisation in self._reseau:
            if canalisation in deja_passer:
                raise ValueError(f"La canalisation {canalisation} est présente deux fois!")
            else:
                 deja_passer.append(canalisation)
    
    
    def recupere_sommets(self) -> List:
        """Récupère tous les sommets rentrés."""
        liste_sommets = list()
        for initial, arrivee, _ in self._reseau:
            if initial not in liste_sommets:
                liste_sommets.append(initial)
            if arrivee not in liste_sommets:
                liste_sommets.append(arrivee)
        return liste_sommets
        
    
    def _genere_table(self) -> Table:
        """Renvoie un résumé du réseau rich.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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

>>> probleme._genere_table()

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
        """
        resultat = Table(title="Problème d'adduction d'eau")
        resultat.add_column("Initial")
        resultat.add_column("Arrivée")
        resultat.add_column("Capacité")
        for debit in self._reseau:
            resultat.add_row(
                debit[0], str(debit[1]), str(debit[2])
            )
        return resultat
    
    
    def affiche(self) -> str:
        """Affiche le résumé directement.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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
        """
        from rich import print
        print(self._genere_table())
        
    
    def table_depart(self) -> pd.DataFrame:
        """Ressort la table de départ des noeuds et arrêtes sous forme de dataframe.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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

>>> probleme.table_depart()
|      | A  | B  | C  | D  | E  | F  | G  | H  | I  | J  | K  | L  |puit|
|------|----|----|----|----|----|----|----|----|----|----|----|----|----|
|source|15.0|15.0|15.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| A    | 0.0| 0.0| 0.0| 0.0| 7.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| B    | 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 7.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| C    | 5.0| 0.0| 0.0| 0.0| 0.0| 5.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| D    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|
| E    | 0.0| 0.0| 0.0| 0.0| 0.0| 5.0| 0.0| 4.0|15.0| 0.0| 0.0| 0.0| 0.0|
| F    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 5.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| G    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0| 0.0| 0.0| 0.0| 0.0|
| H    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 7.0| 0.0| 0.0| 0.0|
| I    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|30.0| 4.0| 0.0|
| J    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
| K    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|10.0| 0.0| 0.0|20.0|
| L    | 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0| 0.0|15.0|
        """
        ligne = self.recupere_sommets()
        ligne.remove("puit")
        colonne = self.recupere_sommets()
        colonne.remove("source")
        tableau = pd.DataFrame(
            data=np.zeros((len(ligne), len(colonne))),
            index=ligne,
            columns=colonne
        )
        for depart, arrivee, flot_max in self._reseau:
            tableau.loc[depart, arrivee] = flot_max
        tableau = tableau.fillna(0);
        return tableau
    
    
    @staticmethod
    def _recupere_noeud_non_alimente_par_source(table: pd.DataFrame) -> List[int]:
        """Récupère le numéro de ligne des sommets qui ne sont pas alimentés par la source.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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

>>> Probleme._recupere_noeud_non_alimente_par_source(probleme.table_depart())
[4, 5, 6, 7, 8, 9, 10, 11, 12]
        """
        non_nul = list()
        i = 0
        for capacite in table.loc["source",:]:
            if capacite == 0.0:
                non_nul.append(i)
            i += 1
        return non_nul
    

    def _recupere_noeuds_capacite_insuffisante(self) -> List[Tuple[str, str]]:
        """Vérifie que la capacité d'un noeud d'arrivée est suffisante.
        
        Exemple :
>>> from Adduction_eau import Probleme

>>> Probleme.par_str(
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

>>> probleme._recupere_noeuds_capacite_insuffisante()
[('A', 'E'), ('E', 'H'), ('I', 'L')]
        """
        capacites_insuffisantes = list()
        table = self.table_depart()
        non_nulle = self._recupere_noeud_non_alimente_par_source(table)
        sommets = self.recupere_sommets()
        sommets.remove("source")
        liste_sommets = list()
        for valeur in non_nulle:
            liste_sommets.append(sommets[valeur])
        sommets.remove("puit")
        flot_minimal_ville = min(i for i in table.loc[:,"puit"] if i > 0)
        for arrivee in liste_sommets:
            if sum(table.loc[:, arrivee]) < flot_minimal_ville:
                for depart in sommets:
                    if table.loc[depart, arrivee] != 0:
                        capacites_insuffisantes.append((depart, arrivee))
        return capacites_insuffisantes
    