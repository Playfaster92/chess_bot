# ChessBot1400 – Apprentissage d’un bot d’échecs agressif (ELO < 1400)

Ce projet a pour objectif de développer un bot d'échecs jouant de manière agressive en s’appuyant sur un jeu de parties disputées par des joueurs classés sous les 1400 ELO. Il repose sur l’extraction de parties agressives, l’analyse de métadonnées, l’évaluation de positions à partir de FEN, et l’entraînement d’un réseau de neurones pour simuler ce style de jeu.


## 1. `read_metadata/` — Analyse et extraction des parties agressives

### `extract.ipynb`

Ce notebook extrait les parties considérées comme agressives selon plusieurs critères :
- Parties courtes
- Absence de match nul
- Ouvertures tranchantes
- Nombre élevé de captures
- Poussées de pions agressives

L’extraction est restreinte aux parties entre joueurs classés sous les 1400 ELO. Le résultat est stocké dans un fichier `aggressives_games_1400.pgn`.

### `reading_meta.ipynb`

Ce notebook permet de :
- Charger les données du fichier `game_data_2013_01.pgn` sous forme de DataFrame.
- Réaliser des statistiques descriptives.
- Identifier les caractéristiques pertinentes à extraire en vue de l'entraînement du modèle.

## 2. `evaluation_position/` — Évaluation des positions à partir d'une FEN

### `evaluation.ipynb`

Ce notebook permet d’évaluer une position d’échecs donnée sous forme de chaîne FEN. Il crée un modèle de régression linéaire qui évalue une position donnée en utilisant différents critères sur la position.

## 3. `model/` — Entraînement du modèle de réseau de neurones

### `model.ipynb`

Ce notebook contient l’architecture et l'entraînement d’un réseau de neurones basé sur les parties extraites (`aggressives_games_1400.pgn`). L’objectif est de modéliser un style de jeu agressif à partir de ce dataset, afin de simuler un bot d’échecs reproduisant ce comportement.

## Prérequis

Avant d’exécuter les notebooks, il est nécessaire d’installer les modules suivants :

```bash
pip install tensorflow python-chess



