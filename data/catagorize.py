import chess
import chess.pgn
from stockfish import Stockfish
import random
import pandas as pd


engine = Stockfish(path="./stockfish/stockfish-ubuntu-x86-64-avx2", depth=15)


TARGET_COUNT = 3

white_wins = []
black_wins = []
draws = []


WHITE_WIN_THRESHOLD = 200
BLACK_WIN_THRESHOLD = -200
DRAW_THRESHOLD = (-50, 50)


puzzle_file = "lichess_db_puzzle.csv"
if puzzle_file:
    puzzles = pd.read_csv(puzzle_file)
    for index, row in puzzles.iterrows():
        fen = row["FEN"]
        try:
            board = chess.Board(fen)
            engine.set_position(fen)
            eval_info = engine.get_evaluation()
            score = eval_info["value"] if eval_info["type"] == "cp" else (10000 if eval_info["value"] > 0 else -10000)

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
            print(f"Error processing puzzle {index}: {e}")
            continue


pgn_file = "lichess_db_puzzle.csv"

if (
    len(white_wins) < TARGET_COUNT
    or len(black_wins) < TARGET_COUNT
    or len(draws) < TARGET_COUNT
):
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

                engine.set_position(fen)
                eval_info = engine.get_evaluation()
                score = eval_info["value"] if eval_info["type"] == "cp" else (10000 if eval_info["value"] > 0 else -10000)

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

data = []

for w in white_wins:
    data.append({"fen" : w, "label" : "White inning"})

for b in black_wins:
    data.append({"fen" : b, "label" : "Black Winning"})
    
for d in draws:
    data.append({"fen" : d, "label" : "Draw"})



df = pd.DataFrame(data)
df = df[df["label"] != "Error"]
df.to_csv("labeled_chess_positions.csv", index=False)
