# app_logic.py
import pygame
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
    pygame.display.set_caption("Mini Chess - Human vs AI")
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
    
def draw_game_ui(screen, turn, game_state, ai_thinking=False, in_check=False):
    """Draw UI elements like turn indicator and game state"""
    # Draw turn indicator
    font = pygame.font.SysFont("Arial", 24)
    color_text = "White" if turn == 'w' else "Black"
    turn_text = font.render(f"Turn: {color_text}", True, const.WHITE)
    screen.blit(turn_text, (const.WIDTH - 150, 20))
    
    # Draw check indicator
    if in_check:
        check_text = font.render(f"{color_text} is in CHECK!", True, (255, 50, 50))
        screen.blit(check_text, (const.WIDTH - 200, 50))
    
    # Draw game state if game is over
    if game_state in ["checkmate", "stalemate"]:
        state_text = "Checkmate!" if game_state == "checkmate" else "Stalemate!"
        winner = "White wins!" if turn == 'b' else "Black wins!" if game_state == "checkmate" else "Draw!"
        
        state_font = pygame.font.SysFont("Arial", 36)
        state_surf = state_font.render(state_text, True, const.WHITE)
        winner_surf = state_font.render(winner, True, const.WHITE)
        
        state_rect = state_surf.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 - 30))
        winner_rect = winner_surf.get_rect(center=(const.WIDTH//2, const.HEIGHT//2 + 30))
        
        # Draw semi-transparent background
        bg_surf = pygame.Surface((const.WIDTH, 120), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 180))
        screen.blit(bg_surf, (0, const.HEIGHT//2 - 60))
        
        screen.blit(state_surf, state_rect)
        screen.blit(winner_surf, winner_rect)
    
    # Draw AI thinking indicator
    if ai_thinking:
        thinking_font = pygame.font.SysFont("Arial", 24)
        thinking_text = thinking_font.render("AI is thinking...", True, const.WHITE)
        screen.blit(thinking_text, (50, 20))



def play_game_round(screen, clock, images, difficulty):
    """Handle a complete game round with player and AI interaction"""
    board = Board(const.BOARD_WIDTH, const.BOARD_HEIGHT, const.SQUARE_SIZE)
    turn = 'w'  # White starts
    selected = None
    valid_moves = []
    last_move = None
    game_state = None
    ai_thinking = False
    in_check = False
    
    # Player is white, AI is black
    player_color = 'w'
    ai_color = 'b'
    
    while True:
        # Handle events
        action = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"
            
            # Handle player input when it's their turn and game is not over
            if turn == player_color and not game_state:
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
                                turn = ai_color  # Switch turns
                                
                                # Check if the opponent is now in check
                                in_check = is_in_check(board, ai_color)
                            else:
                                # Select a different piece or deselect
                                if piece and piece[0] == player_color:
                                    selected = (row, col)
                                    valid_moves = get_legal_moves(board, row, col)
                                else:
                                    selected = None
                                    valid_moves = []
                        # If no piece is selected yet
                        else:
                            if piece and piece[0] == player_color:
                                selected = (row, col)
                                valid_moves = get_legal_moves(board, row, col)
                                
            # Handle game over buttons
            if game_state and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                
                # Check if Play Again button is clicked
                play_again_rect = pygame.Rect(const.WIDTH // 4 - 100, const.HEIGHT - 70, 200, 60)
                if play_again_rect.collidepoint(pos):
                    return "DIFFICULTY"  # Go to difficulty selection
                
                # Check if Main Menu button is clicked
                menu_rect = pygame.Rect(const.WIDTH * 3 // 4 - 100, const.HEIGHT - 70, 200, 60)
                if menu_rect.collidepoint(pos):
                    return "MENU"  # Go to main menu
        
        # AI's turn
        if turn == ai_color and not game_state:
            ai_thinking = True
            # Draw the current state while AI is "thinking"
            draw_game_screen(screen, board, images, selected, valid_moves, last_move)
            draw_game_ui(screen, turn, game_state, ai_thinking, in_check)
            pygame.display.flip()
            
            # Add a small delay to make it look like the AI is thinking
            time.sleep(0.5 + random.random() * 0.5)
            
            # Get AI move
            ai_move = get_ai_move(board, ai_color, difficulty)
            
            if ai_move:
                start, end = ai_move
                board.make_move(start, end)
                last_move = (start, end)
                turn = player_color  # Switch turns
                
                # Check if the player is now in check
                in_check = is_in_check(board, player_color)
            
            ai_thinking = False
        
        # Check if game is over
        if not game_state:
            game_state = is_game_over(board, turn)
        
        # Draw game screen
        draw_game_screen(screen, board, images, selected, valid_moves, last_move)
        draw_game_ui(screen, turn, game_state, ai_thinking, in_check)
        
        # Handle game over state with navigation buttons
        if game_state:
            # Draw semi-transparent background for buttons
            button_bg = pygame.Surface((const.WIDTH, 100), pygame.SRCALPHA)
            button_bg.fill((0, 0, 0, 200))
            screen.blit(button_bg, (0, const.HEIGHT - 120))
            
            # Create buttons
            font = pygame.font.SysFont("Arial", 32)
            play_again_rect = pygame.Rect(const.WIDTH // 4 - 100, const.HEIGHT - 70, 200, 60)
            menu_rect = pygame.Rect(const.WIDTH * 3 // 4 - 100, const.HEIGHT - 70, 200, 60)
            
            # Handle mouse hover for buttons
            mouse_pos = pygame.mouse.get_pos()
            
            # Play Again button
            if play_again_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, const.BRIGHT_GREEN, play_again_rect, border_radius=5)
                text_color = const.BLACK
            else:
                pygame.draw.rect(screen, const.GREEN, play_again_rect, border_radius=5)
                text_color = const.WHITE
            text = font.render("Play Again", True, text_color)
            text_rect = text.get_rect(center=play_again_rect.center)
            screen.blit(text, text_rect)
            
            # Menu button
            if menu_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, const.BRIGHT_RED, menu_rect, border_radius=5)
                text_color = const.BLACK
            else:
                pygame.draw.rect(screen, const.RED, menu_rect, border_radius=5)
                text_color = const.WHITE
            text = font.render("Main Menu", True, text_color)
            text_rect = text.get_rect(center=menu_rect.center)
            screen.blit(text, text_rect)
        
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
            # Handle difficulty selection
            difficulty_choice = select_difficulty_with_navigation(screen, const.WIDTH, const.HEIGHT)
            if difficulty_choice == "QUIT" or difficulty_choice is None:
                return False  # Quit application
            
            # Start game with selected difficulty
            game_result = play_game_round(screen, pygame.time.Clock(), load_piece_images(const.SQUARE_SIZE), difficulty_choice)
            
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