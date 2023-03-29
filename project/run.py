from src import main
import sys

if __name__ == '__main__':
    n = len(sys.argv)
    if n == 2:
        path = sys.argv[1]
        print(f"INFO : Using config path : {path}")
        main.run(f"configPresets/{path}")
    else:
        print("INFO : Using default config path")
        main.run()
