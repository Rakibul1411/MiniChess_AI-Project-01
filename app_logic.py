# app_logic.py
import pygame
import os
import sys
import random
import time
from button_navigation import create_button, select_difficulty_with_navigation
from board import Board
from pieces import load_piece_images
from launch_screen import create_launch_screen
import constants as const
from difficulty_screen import create_difficulty_screen


from ai import get_ai_move
from app_game_move import get_legal_moves, is_game_over, is_in_check

def initialize_game():
    """Initialize pygame and create the game window"""
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
    pygame.display.set_caption("Mini Chess")
    return screen, pygame.time.Clock()

def handle_game_events():
    """Handle pygame events and return the action"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "MENU"
    return None

def draw_game_screen(screen, board, piece_images, selected=None, valid_moves=None, last_move=None):
    """Draw all game elements on the screen"""
    screen.fill(const.BLACK)
    board.draw(screen)
    
    # Draw highlights for last move
    if last_move:
        start, end = last_move
        board.highlight_square(screen, start[0], start[1], const.LAST_MOVE_COLOR)
        board.highlight_square(screen, end[0], end[1], const.LAST_MOVE_COLOR)
    
    # Draw highlights for valid moves
    if valid_moves:
        for move in valid_moves:
            board.highlight_square(screen, move[0], move[1], const.MOVE_COLOR)
    
    # Draw highlight for selected piece
    if selected:
        board.highlight_square(screen, selected[0], selected[1], const.HIGHLIGHT_COLOR)
    
    board.draw_pieces(screen, piece_images)

def draw_game_ui(screen, turn, game_state, ai_thinking=False, in_check=False, difficulty=None):
    """Draw UI elements like turn indicator, difficulty, and game state"""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    button_font_path = os.path.join(assets_dir, 'Rosemary.ttf')
    font = pygame.font.Font(button_font_path, 25) if os.path.exists(button_font_path) else \
                pygame.font.SysFont("Georgia", 25, bold=True)
                
    color_text = "White" if turn == 'w' else "Black"
    bar_height = const.UI_HEIGHT
    y = const.HEIGHT - bar_height

    # Draw bar at the bottom
    pygame.draw.rect(screen, (33, 150, 243), (0, y, const.WIDTH, bar_height))

    # Turn (left)
    turn_text = font.render(f"Turn: {color_text}", True, const.WHITE)
    turn_pos = (20, y + (bar_height - turn_text.get_height()) // 2)
    screen.blit(turn_text, turn_pos)

    # Difficulty (right)
    if difficulty:
        diff_text = font.render(f"Difficulty: {difficulty.title()}", True, const.WHITE)
        diff_pos = (const.WIDTH - diff_text.get_width() - 20, y + (bar_height - diff_text.get_height()) // 2)
        screen.blit(diff_text, diff_pos)
    else:
        diff_text = None

    # King in Check! (centered)
    if in_check:
        check_text = font.render("King in Check!", True, (255, 50, 50))
        check_x = (const.WIDTH - check_text.get_width()) // 2
        check_y = y + (bar_height - check_text.get_height()) // 2
        screen.blit(check_text, (check_x, check_y))

    # Draw game state if game is over
    if game_state in ["checkmate", "stalemate", "insufficient_material"]:
        if game_state == "checkmate":
            state_text = "Checkmate!"
            winner = "White wins!" if turn == 'b' else "Black wins!"
        elif game_state == "stalemate":
            state_text = "Stalemate!"
            winner = "Draw!"
        else:  # insufficient_material
            state_text = "Only Kings Remain!"
            winner = "Draw!"
            
        state_font = pygame.font.SysFont("Arial", 36)
        state_surf = state_font.render(state_text, True, const.WHITE)
        winner_surf = state_font.render(winner, True, const.WHITE)
        state_rect = state_surf.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 - 30))
        winner_rect = winner_surf.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 + 30))
        bg_surf = pygame.Surface((const.WIDTH, 120), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        screen.blit(bg_surf, (0, const.HEIGHT//2 - 60))
        screen.blit(state_surf, state_rect)
        screen.blit(winner_surf, winner_rect)

    # AI thinking indicator
    if ai_thinking:
        thinking_font = pygame.font.SysFont("Arial", 24)
        thinking_text = thinking_font.render("AI is thinking...", True, const.WHITE)
        screen.blit(thinking_text, (20, 20))

def play_game_round(screen, clock, images, difficulty, opponent):
    """Handle a complete game round with player and AI/human interaction"""
    board = Board(const.BOARD_WIDTH, const.BOARD_HEIGHT, const.SQUARE_SIZE)
    turn = 'w'  # White starts
    selected = None
    valid_moves = []
    last_move = None
    game_state = None
    ai_thinking = False
    in_check = False
    
    # Determine player and AI colors based on opponent
    if opponent == "OPPONENT_AI":
        player_color = 'w'  # Player is white
        ai_color = 'b'      # AI is black
    else:  # OPPONENT_HUMAN
        player_color = None  # Both colors are controlled by players
        ai_color = None      # No AI
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
            
            # Handle game over events when the game is over
            if game_state:
                result = handle_game_over_events(event)
                if result:
                    return result
            
            # Handle player input for their turn
            if not game_state:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // const.SQUARE_SIZE
                    row = pos[1] // const.SQUARE_SIZE
                    
                    if 0 <= row < const.BOARD_HEIGHT and 0 <= col < const.BOARD_WIDTH:
                        piece = board.get_piece(row, col)
                        
                        # If a piece is already selected
                        if selected:
                            # Check if clicked on a valid move
                            if (row, col) in valid_moves:
                                # Make the move
                                board.make_move(selected, (row, col))
                                last_move = (selected, (row, col))
                                selected = None
                                valid_moves = []
                                turn = 'b' if turn == 'w' else 'w'  # Switch turns
                                
                                # Check if the opponent is now in check
                                opponent_color = 'b' if turn == 'w' else 'w'
                                in_check = is_in_check(board, opponent_color)
                            else:
                                # Select a different piece or deselect
                                if piece and piece[0] == turn:
                                    selected = (row, col)
                                    valid_moves = get_legal_moves(board, row, col)
                                else:
                                    selected = None
                                    valid_moves = []
                        # If no piece is selected yet
                        else:
                            if piece and piece[0] == turn:
                                selected = (row, col)
                                valid_moves = get_legal_moves(board, row, col)
        
        # AI's turn (only if opponent is AI)
        if opponent == "OPPONENT_AI" and turn == ai_color and not game_state:
            ai_thinking = True
            # Draw the current state while AI is "thinking"
            draw_game_screen(screen, board, images, selected, valid_moves, last_move)
            draw_game_ui(screen, turn, game_state, ai_thinking, in_check, difficulty)
            pygame.display.flip()
            
            # Add a small delay to make it look like the AI is thinking
            time.sleep(0.5 + random.random() * 0.5)
            
            # Get AI move
            ai_move = get_ai_move(board, ai_color, difficulty)
            
            if ai_move:
                start, end = ai_move
                board.make_move(start, end)
                last_move = (start, end)
                turn = player_color  # Switch to player's turn
                in_check = is_in_check(board, player_color)
            
            ai_thinking = False
        
        # Check if game is over
        if not game_state:
            game_state = is_game_over(board, turn)
        
        # Draw game screen
        draw_game_screen(screen, board, images, selected, valid_moves, last_move)
        draw_game_ui(screen, turn, game_state, ai_thinking, in_check, difficulty)
        
        # Handle game over state with navigation buttons
        if game_state:
            draw_game_over_screen(screen, game_state, turn)
        
        pygame.display.flip()
        clock.tick(const.FPS)

def handle_main_menu(screen):
    """Display and handle the main menu screen"""
    while True:
        choice = create_launch_screen(screen, const.WIDTH, const.HEIGHT)
        if choice != "PLAY":
            return False  # Quit application
        
        difficulty_selected = True
        while difficulty_selected:
            # Handle difficulty and opponent selection
            result = select_difficulty_with_navigation(screen, const.WIDTH, const.HEIGHT)
            if result == "QUIT" or result is None:
                return False  # Quit application
            
            difficulty, opponent = result  # Unpack difficulty and opponent
            
            # Start game with selected difficulty and opponent
            game_result = play_game_round(screen, pygame.time.Clock(), load_piece_images(const.SQUARE_SIZE), difficulty, opponent)
            
            if game_result == "QUIT":
                return False  # Quit application
            elif game_result == "MENU":
                difficulty_selected = False  # Return to main menu
            elif game_result == "DIFFICULTY":
                # Continue to difficulty selection (next loop iteration)
                pass
            else:
                difficulty_selected = False  # Default behavior - return to main menu

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