import zstandard as zstd
from io import TextIOWrapper

input_path = "lichess_db_standard_rated_2025-05.pgn.zst"
output_path = "filtered_1000_1200.pgn"

with open(input_path, "rb") as fh:
    dctx = zstd.ZstdDecompressor()
    with dctx.stream_reader(fh) as reader:
        # On transforme le flux binaire en flux texte
        text_stream = TextIOWrapper(reader, encoding="utf-8")
        
        with open(output_path, "w", encoding="utf-8") as out_f:
            buffer = ""
            for line in text_stream:
                if line.strip() == "":
                    if "WhiteElo" in buffer and "BlackElo" in buffer:
                        try:
                            white_elo = int(buffer.split("[WhiteElo \"")[1].split("\"]")[0])
                            black_elo = int(buffer.split("[BlackElo \"")[1].split("\"]")[0])
                            average_elo = (white_elo + black_elo) / 2
                            if 1000 <= average_elo <= 1200:
                                out_f.write(buffer + "\n\n")
                        except:
                            pass
                    buffer = ""
                else:
                    buffer += line
