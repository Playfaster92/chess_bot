import zstandard as zstd
import io
import chess.pgn
import pandas as pd

# 2. Extraire les données d'une partie PGN
def extract_game_data(game):
    board = game.board()
    moves = list(game.mainline_moves())
    first_move = board.san(moves[0]) if moves else None

    return {
        "White": game.headers.get("White", ""),
        "Black": game.headers.get("Black", ""),
        "Result": game.headers.get("Result", ""),
        "WhiteElo": int(game.headers.get("WhiteElo", 0)),
        "BlackElo": int(game.headers.get("BlackElo", 0)),
        "Opening": game.headers.get("Opening", ""),
        "ECO": game.headers.get("ECO", ""),
        "FirstMove": first_move,
        "NumMoves": len(moves)
    }

# 3. Lire toutes les parties du fichier et les transformer en DataFrame
def pgn_zst_to_dataframe(zst_path, max_games=None):
    games = []
    count = 0

    with open(zst_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(compressed_file)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')

        while True:
            game = chess.pgn.read_game(text_stream)
            if game is None:
                break
            try:
                games.append(extract_game_data(game))
            except Exception as e:
                print(f"Erreur à la partie {count} : {e}")
            count += 1
            if max_games and count >= max_games:
                break

    df = pd.DataFrame(games)
    return df


# 4. Exemple d’utilisation
df = pgn_zst_to_dataframe("lichess_db_standard_rated_2017-02.pgn.zst", max_games=10000)  # remplace par ton vrai fichier

print(df.head())