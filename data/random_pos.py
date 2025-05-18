import chess
import chess.pgn
from stockfish import Stockfish
import random
import os

engine = Stockfish(path="./stockfish/stockfish-ubuntu-x86-64-avx2", depth=15)

TARGET_COUNT = 4000


white_wins = []
black_wins = []
draws = []

WHITE_WIN_THRESHOLD = 200 
BLACK_WIN_THRESHOLD = -200 
DRAW_THRESHOLD = (-50, 50)  


pgn_file = "lichess_db_standard_rated_2016-03.pgn"


with open(pgn_file, encoding="utf-8", errors="ignore") as pgn:
    game_count = 0
    while True:
        try:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            game_count += 1
            if game_count % 100 == 0:
                print(f"Processed {game_count} games...")


            moves = list(game.mainline())
            if len(moves) < 10:
                continue

           
            random_index = random.randint(5, len(moves) - 2)
            node = moves[random_index]
            board = node.board()
            fen = board.fen()

       
            engine.set_fen_position(fen)

            eval_info = engine.get_evaluation()
            if eval_info["type"] == "cp":
                score = eval_info["value"]  
            elif eval_info["type"] == "mate":
                score = 10000 if eval_info["value"] > 0 else -10000
   
         
            if score >= WHITE_WIN_THRESHOLD and len(white_wins) < TARGET_COUNT:
                white_wins.append(fen)
            elif score <= BLACK_WIN_THRESHOLD and len(black_wins) < TARGET_COUNT:
                black_wins.append(fen)
            elif DRAW_THRESHOLD[0] <= score <= DRAW_THRESHOLD[1] and len(draws) < TARGET_COUNT:
                draws.append(fen)

    
            if (
                len(white_wins) >= TARGET_COUNT
                and len(black_wins) >= TARGET_COUNT
                and len(draws) >= TARGET_COUNT
            ):
                break

        except Exception as e:
            print(f"Error processing game {game_count}: {e}")
            continue


all_fens = white_wins + black_wins + draws
random.shuffle(all_fens)

output_file = "balanced_positions.fen"
with open(output_file, "w") as f:
    for fen in all_fens:
        f.write(fen + "\n")


print(f"Saved {len(all_fens)} FENs to {output_file}")
print(f"White wins: {len(white_wins)}")
print(f"Black wins: {len(black_wins)}")
print(f"Draws: {len(draws)}")