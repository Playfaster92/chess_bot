import chess
import chess.svg
import torch
from model import EvaluationNet
from dataset import ChessDataset
from IPython.display import SVG, display


def afficher_plateau(board, fichier="echiquier.html"):
    svg = chess.svg.board(board=board, size=400)
    with open(fichier, "w") as f:
        f.write(svg)
    print(f"Échiquier sauvegardé dans {fichier}. Ouvre-le dans un navigateur.")



def bot_move(model, board):
    best_move = None
    best_eval = -float("inf")

    for move in board.legal_moves:
        board.push(move)
        tensor = ChessDataset.encode_board(board).unsqueeze(0)
        with torch.no_grad():
            evaluation = model(tensor).item()
        if evaluation > best_eval:
            best_eval = evaluation
            best_move = move
        board.pop()

    return best_move


def main():
    print("Bienvenue ! Vous jouez les pièces noires. Le bot commence.")
    
    board = chess.Board()
    model = EvaluationNet()
    model.load_state_dict(torch.load("evaluation_model.pth"))
    model.eval()

    while not board.is_game_over():
        afficher_plateau(board)  # Affichage graphique
        print("\n")

        if board.turn == chess.WHITE:
            move = bot_move(model, board)
            print(f"Bot joue : {move.uci()}")
            board.push(move)
        else:
            user_move = input("Votre coup (format uci, ex : e7e5) : ")
            try:
                move = chess.Move.from_uci(user_move)
                if move in board.legal_moves:
                    board.push(move)
                else:
                    print("Coup illégal. Réessayez.")
            except:
                print("Format invalide. Réessayez.")

    afficher_plateau(board)
    print("\nPartie terminée :", board.result())
    print("FEN finale :", board.fen())


# À exécuter seulement dans un notebook ou un environnement IPython/Jupyter
if __name__ == "__main__":
    main()
