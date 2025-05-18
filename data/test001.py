from stockfish import Stockfish

stockfish = Stockfish(path = "./stockfish/stockfish-ubuntu-x86-64-avx2" , depth=15)

stockfish.set_position("r1bk1b1r/pp1pn1R1/2n5/1Np3Bp/2B5/5N2/PP3PPP/R5K1 w - - 1 16")

print("eval", stockfish.get_evaluation())
print("Best move", stockfish.get_best_move())