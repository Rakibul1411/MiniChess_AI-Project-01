# app_logic.py
import pygame
import sys
from button_navigation import create_button, select_difficulty_with_navigation
from board import Board
from pieces import load_piece_images
from launch_screen import create_launch_screen
import constants as const

def initialize_game():
    """Initialize pygame and create the game window"""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("Mini Chess - Human vs AI")
    return screen, pygame.time.Clock()

def handle_game_events():
    """Handle pygame events and return the action"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
    return None

def draw_game_screen(screen, board, piece_images):
    """Draw all game elements on the screen"""
    screen.fill(const.BLACK)
    board.draw(screen)
    board.draw_pieces(screen, piece_images)

def play_game_round(screen, clock, images, difficulty):
    """Handle a single game round"""
    board = Board(const.BOARD_WIDTH, const.BOARD_HEIGHT, const.SQUARE_SIZE)
    
    while True:
        action = handle_game_events()
        if action:
            return action
        
        draw_game_screen(screen, board, images)
        pygame.display.flip()
        clock.tick(const.FPS)

def handle_main_menu(screen):
    """Display and handle the main menu screen"""
    while True:
        choice = create_launch_screen(screen, const.WIDTH, const.HEIGHT)
        if choice != "PLAY":
            return False  # Quit application
        
        # Handle difficulty selection
        difficulty_choice = select_difficulty_with_navigation(screen, const.WIDTH, const.HEIGHT)
        if difficulty_choice == "QUIT" or difficulty_choice is None:
            return False  # Quit application
        
        # Start game with selected difficulty
        game_result = play_game_round(screen, pygame.time.Clock(), load_piece_images(const.SQUARE_SIZE), difficulty_choice)
        
        if game_result == "QUIT":
            return False  # Quit application
        elif game_result == "MENU":
            continue  # Return to main menu

def run_game_application():
    """Main function to initialize and run the game application"""
    try:
        screen, clock = initialize_game()
        piece_images = load_piece_images(const.SQUARE_SIZE)
        
        while handle_main_menu(screen):
            pass  # Continue running until user quits
            
    finally:
        pygame.quit()
        sys.exit()