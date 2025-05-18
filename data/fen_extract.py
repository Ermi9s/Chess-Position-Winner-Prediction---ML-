import pandas as pd


df = pd.read_csv("lichess_db_puzzle.csv")
fens = df["FEN"]
fens.to_csv("fens_only.csv", index=False, header=["fen"])

# print(len(fens))
