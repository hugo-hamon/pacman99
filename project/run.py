from src import main
import sys

if __name__ == '__main__':
    n = len(sys.argv)
    if n == 2:
        main.run(sys.argv[1])
    else:
        print("INFO : Using default config path")
        main.run()
