Overview

MiniChess is a high-performance, minimalist chess implementation built with Python and Pygame. Designed for rapid gameplay and clean visuals, this engine maintains the strategic depth of classical chess while optimizing for speed and accessibility.


🎮 Features


🧠 Difficulty Selection: Choose between Easy, Medium, and Hard AI

🖼️ Modern UI: Includes launch screen, animated chess pieces, and glowing titles

🔊 Sound Effects: Click, hover, and ambient background sounds

♟️ AI vs Human, Human vs Human Gameplay: The AI makes strategic decisions based on selected difficulty

📦 Modular Codebase: Organized into board.py, app_logic.py, launch_screen.py, etc.


🗂️ Project Structure
<pre>
MiniChess/
├── assets/                 # All images, sounds, and fonts
├── app_logic.py            # Main game loop and logic
├── board.py                # Board rendering and piece movement
├── pieces.py               # Piece image loading and placeholder rendering
├── constants.py            # Configuration for sizes, colors, FPS
├── launch_screen.py        # Intro screen with animated effects
├── difficulty_screen.py    # Difficulty level selection screen
├── button_navigation.py    # Manages screen transitions
├── main.py                 # Entry point of the game
└── README.md               # Project documentation (this file)
</pre>



▶️ How to Run


Requirements<br/>
<pre>
Python 3.10+
Pygame 
</pre>

Setup
<pre>
pip install pygame
python main.py  
</pre>




🧠 Educational Use

This project is ideal for:

Practicing game development with Python

Understanding 2D grid-based movement

Learning turn-based game loops
