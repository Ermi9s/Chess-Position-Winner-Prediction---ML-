from stockfish import Stockfish
import pandas as pd

stockfish = Stockfish(path="./stockfish/stockfish-ubuntu-x86-64-avx2", depth=15)


df = pd.read_csv("balanced_positions.fen", header=None, names=["fen"])

FENS = [df["fen"][i] for i in range(12000)] 

def cat(ev):
    if ev >= 100:
        return "White Winning"
    elif ev <= -100:
        return "Black Winning"
    else:
        return "Draw"



# print(FENS)
data = []
for fen in FENS:
    stockfish.set_fen_position(fen)
    evaluation = stockfish.get_evaluation()
    
    print(evaluation)
    if evaluation is None or evaluation.get("type") != "cp":
        label = "Error"
    else:
        label = cat(evaluation["value"])
    
    data.append({"fen": fen, "label": label})

# print(data)


df = pd.DataFrame(data)
df = df[df["label"] != "Error"]
df.to_csv("labeled_chess_positions.csv", index=False)
