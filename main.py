# main.py
import sys
# It's good practice to ensure the current directory is in sys.path
# if modules are in the same folder, but often not strictly necessary.
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_logic import run_game_application

if __name__ == "__main__":
    run_game_application()