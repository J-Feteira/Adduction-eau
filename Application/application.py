#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Description.

Contient l'application de résolution de l'exercice d'adduction d'eau.
"""

from ipywidgets.widgets.interaction import show_inline_matplotlib_plots
import ipywidgets as ipw
from IPython.display import display
import matplotlib.pyplot as plt
from Adduction_eau import Probleme
from Adduction_eau import ressort_table_apres_travaux, visualisation_graphe_flots_maximaux, recupere_ville_flot_maximal_faible, transforme_table


class Application:
    def __init__(self):
        """Crée l'application de la résolution du problème d'adduction."""
        self.caption = ipw.Label(value="Résolution du problème d'adduction d'eau :")
        self.bouton = ipw.Button(description="Résoudre")
        reseau = """
source / D / 30.
D / E / 32.
E / F / 21.
F / G / 22.
G / H / 23.
H / I / 12.
I / J / 35.
J / K / 30.
K / L / 2.
J / puit / 30.
K / puit / 10.
L / puit / 10.
"""
        self.zone_entree = ipw.Textarea(value=reseau, layout=ipw.Layout(height="425px", width="200px"))
        self.choix_graphique = ipw.ToggleButtons(
            options=["Début", "Fin"],
            value="Début",
            description="Graphique : ",
            disabled=False
        )
        self.aide = ipw.Button(description="AIDE", layout=ipw.Layout(width="auto"), button_style="danger")
        self.zone_probleme = ipw.Output()
        self.zone_solution = ipw.Output()
        self.etapes = ipw.Output()
        self.graphique = ipw.Output()
        self.erreur = ipw.Output()
        self.total = ipw.VBox([
            ipw.HBox([self.caption, self.aide]),
            ipw.HBox(
                [
                    ipw.VBox([self.bouton, self.zone_entree]),
                    ipw.VBox([ipw.Label(value="Départ :"), self.erreur, self.zone_probleme]),
                    ipw.VBox([ipw.Label(value="Résultat :"), self.zone_solution]),
                    ipw.VBox([ipw.Label(value="Étapes :"), self.etapes])
                ]
            ),
            ipw.HBox([self.choix_graphique, self.graphique])
        ])
        self._sur_clique(self.bouton)
        self.bouton.on_click(self._sur_clique)
        self._choix_graphique(self.choix_graphique)
        self.choix_graphique.observe(self._choix_graphique, "value")
        self._clique_aide(self.aide)
        self.aide.on_click(self._clique_aide)
        
        
    def affichage(self):
        """Affiche l'application pour l'utilisateur."""
        display(self.total)
        
    
    def _sur_clique(self, b):
        """Lorsque l'utilisateur appuie sur le bouton résoudre."""
        try:
            self.zone_probleme.clear_output()
            self.zone_solution.clear_output()
            self.erreur.clear_output()
            self.etapes.clear_output()
            self.graphique.clear_output()
            self.choix_graphique.value = "Début"
            probleme = Probleme.par_str(self.zone_entree.value)
            solution = ressort_table_apres_travaux(probleme)
            with self.zone_probleme:
                probleme.affiche()
            with self.zone_solution:
                solution_arretes = transforme_table(probleme.table_depart())
                solution_finale = Probleme(solution_arretes)
                solution_finale.affiche()
            with self.etapes:
                self._capacites_insuffisantes(probleme)
            with self.graphique:
                visualisation_graphe_flots_maximaux(probleme.table_depart())
                show_inline_matplotlib_plots()
        except ValueError:
            with self.erreur:
                display(
                    ipw.HTML(
                        f"""
<p style="color:red; border:2px solid yellow;"> <B><U> Veuillez respecter la syntaxe : </U> </B><br>
DEPART / ARRIVEE / CAPACITE MAXIMALE <br>
<B> Le problème est à la ligne {self._est_valide()} </B>
</p>

<p style="color:red; border:2px solid yellow;">  <B><U> Exemple : </U> </B><br>
source / Tours / 150 <br>
Tours / Joue-les-Tours / 50 <br>
Joue-les-Tours / puit / 40</p>

<p style="color:red; border:2px solid yellow;">  <B><U> Remarque : </U> </B><br>
L'entrée doit comprendre une source et un puit. Pour plus d'informations, cliquez sur <B> AIDE </B>
</p>
"""
                    )
                )
            
    
    def _choix_graphique(self, change):
        """Permet à l'utilisateur de voir le graphique qu'il souhaite."""
        self.graphique.clear_output()
        plt.rcParams["figure.figsize"] = (12, 9)
        
        probleme = Probleme.par_str(self.zone_entree.value)
        solution = ressort_table_apres_travaux(probleme)
        if self.choix_graphique.value == "Début":
            with self.graphique:
                visualisation_graphe_flots_maximaux(probleme.table_depart())
                show_inline_matplotlib_plots()
        else:
            with self.graphique:
                visualisation_graphe_flots_maximaux(solution)
                show_inline_matplotlib_plots()
    
    
    def _capacites_insuffisantes(self, probleme: Probleme):
        """Annonce les capacités insuffisantes pour l'utilisateur."""
        longueur_villes_non_alimentees = len(recupere_ville_flot_maximal_faible(probleme))
        if longueur_villes_non_alimentees != 0:
            if longueur_villes_non_alimentees == 1:
                print(f"La ville {recupere_ville_flot_maximal_faible(probleme)[0][0]} n'est pas assez alimentée.")
            else:
                print(f"Les villes qui ne sont pas assez alimentées en eau sont : ")
                for canalisation in recupere_ville_flot_maximal_faible(probleme):
                    print("- ", canalisation[0])
            capacites_insuffisantes = probleme._recupere_noeuds_capacite_insuffisante()
            if len(capacites_insuffisantes) > 0:
                table = probleme.table_depart()
                print("Les capacités à modifier sont : ")
                for valeur in capacites_insuffisantes:
                    print(f"{valeur[0]} --> {valeur[1]} : {table.loc[valeur[0], valeur[1]]}")
        else:
            print("Aucun travail n'est nécessaire.")
    
    
    def _est_valide(self):
        """Vérifie que la ligne est valide sinon ressort message d'erreur."""
        reseau = list()
        i = 0
        for ligne in self.zone_entree.value.strip().splitlines():
            i += 1
            try:
                initial, arrivee, capacite = ligne.split("/")
            except ValueError:
                return i
    
    
    def _clique_aide(self, b):
        """Permet à l'utilisateur d'obtenir une aide pour l'application."""
        self.zone_probleme.clear_output()
        self.zone_solution.clear_output()
        self.erreur.clear_output()
        self.etapes.clear_output()
        with self.erreur:
            display(
                    ipw.HTML(
                        """
<p style="color:red; border:2px solid yellow;"> <B><U> Application : </U> </B><br>
1) Rentrer le réseau sous la forme : DEPART / ARRIVEE / CAPACITE MAXIMALE. <br>
<B> Attention : </B> Chaque réseau doit comprendre <B>UNE</B> source et <B>UN</B> puit annoté respectivement `source` et `puit`. <br>
2) Appuyer sur le bouton `Résoudre`. <br>
3) La table `Départ` vous permettra de vérifier que votre saisie est juste. <br>
4) La table `Résultat` vous permettra de voir la sortie avec les capacités modifiés. <br>
5) La zone `étape` vous permettra de voir les villes qui n'étaient pas assez alimentées en eau, ainsi que les canalisations qui doivent recevoir des travaux. <br>
6) Pour une compréhension plus facile, le réseau se retrouve sous forme de graphique avec les capacités et flots maximaux pour chaque canalisation. <br>
<B> Remarque : </B> Le bouton `Début` ressort le réseau initial et le bouton `Fin` ressort le réseau final.
</p>

<p style="border:2px solid yellow;"> <B> Remarque : </B> Si la capacité est un décimal, veuillez mettre un point (.) plutôt qu'une virgule (,). </p>

<p style="color:red; border:2px solid yellow;">  <B><U> Exemple de réseau : </U> </B><br>
source / TOURS / 150 <br>
TOURS / JOUE-LES-TOURS / 50 <br>
JOUE-LES-TOURS / puit / 40
</p>
<p style= "border:2px solid yellow;"> <B> Pour quitter l'aide appuyez sur Résoudre </B> </p>
"""
                    )
                )