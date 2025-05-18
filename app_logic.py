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
    
# In the draw_game_ui function in app_logic.py, replace the current implementation with:

def draw_game_ui(screen, turn, game_state, ai_thinking=False, in_check=False, difficulty=None):
    """Draw UI elements like turn indicator, difficulty, and game state"""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    buttom_font_path = os.path.join(assets_dir, 'Rosemary.ttf')
    font = pygame.font.Font(buttom_font_path, 25) if os.path.exists(buttom_font_path) else \
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

    # Draw game state if game is over (unchanged)
    if game_state in ["checkmate", "stalemate"]:
        state_text = "Checkmate!" if game_state == "checkmate" else "Stalemate!"
        winner = "White wins!" if turn == 'b' else "Black wins!" if game_state == "checkmate" else "Draw!"
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

    # AI thinking indicator (unchanged)
    if ai_thinking:
        thinking_font = pygame.font.SysFont("Arial", 24)
        thinking_text = thinking_font.render("AI is thinking...", True, const.WHITE)
        screen.blit(thinking_text, (20, 20))


'''
def find_king(board, color):
    """Find the position of the king with the given color"""
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == color and 'king' in piece:
                return (r, c)
    return None

def is_in_check(board, color):
    """Check if the king of the given color is in check"""
    # Find the king's position
    king_pos = find_king(board, color)
    if not king_pos:
        return False  # No king found (shouldn't happen in a normal game)
    
    # Check if any opponent piece can capture the king
    opponent_color = 'b' if color == 'w' else 'w'
    
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == opponent_color:
                moves = board.get_valid_moves(r, c)
                if king_pos in moves:
                    return True
    
    return False

def would_be_in_check_after_move(board, start, end, color):
    """Check if making a move would leave the king in check"""
    # Save the current state
    sr, sc = start
    er, ec = end
    moved_piece = board.get_piece(sr, sc)
    captured_piece = board.get_piece(er, ec)
    
    # Make the move
    board.make_move(start, end)
    
    # Check if the king is in check after the move
    result = is_in_check(board, color)
    
    # Restore the original position
    board.undo_move(start, end, captured_piece)
    
    return result

def get_legal_moves(board, row, col):
    """Get all legal moves for a piece (moves that don't leave the king in check)"""
    piece = board.get_piece(row, col)
    if not piece:
        return []
    
    color = piece[0]
    potential_moves = board.get_valid_moves(row, col)
    legal_moves = []
    
    for move in potential_moves:
        # Check if the move would leave the king in check
        if not would_be_in_check_after_move(board, (row, col), move, color):
            legal_moves.append(move)
    
    return legal_moves

def is_game_over(board, color):
    """Check if the game is over (checkmate or stalemate)"""
    # Check if the king is in check
    check = is_in_check(board, color)
    
    # Check if there are any legal moves
    has_legal_moves = False
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == color:
                legal_moves = get_legal_moves(board, r, c)
                if legal_moves:
                    has_legal_moves = True
                    break
        if has_legal_moves:
            break
    
    if not has_legal_moves:
        if check:
            return "checkmate"  # No legal moves and king is in check
        else:
            return "stalemate"  # No legal moves but king is not in check
    
    return None
'''
'''
def get_ai_move(board, color, difficulty):
    """Generate an AI move based on difficulty level"""
    # Get all pieces and their legal moves
    all_pieces_with_moves = []
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == color:
                legal_moves = get_legal_moves(board, r, c)
                if legal_moves:
                    all_pieces_with_moves.append(((r, c), legal_moves))
    
    if not all_pieces_with_moves:
        return None
    
    if difficulty == "EASY":
        # Random move selection
        piece_pos, moves = random.choice(all_pieces_with_moves)
        move = random.choice(moves)
        return (piece_pos, move)
    
    elif difficulty == "MEDIUM":
        # Prioritize captures, checks, and protecting the king
        check_moves = []  # Moves that put opponent in check
        capture_moves = []  # Moves that capture a piece
        king_safety_moves = []  # Moves that get king out of danger or block checks
        regular_moves = []  # All other legal moves
        
        opponent_color = 'b' if color == 'w' else 'w'
        king_pos = find_king(board, color)
        opponent_king_pos = find_king(board, opponent_color)
        
        for piece_pos, moves in all_pieces_with_moves:
            for move in moves:
                # Make the move temporarily
                captured_piece = board.get_piece(move[0], move[1])
                board.make_move(piece_pos, move)
                
                # Check if this move puts the opponent's king in check
                if is_in_check(board, opponent_color):
                    check_moves.append((piece_pos, move))
                # Check if this move captures a piece
                elif captured_piece:
                    capture_value = board.get_piece_value(captured_piece)
                    capture_moves.append((piece_pos, move, capture_value))
                # Check if this improves king safety (king move out of danger)
                elif 'king' in board.get_piece(move[0], move[1]):
                    king_safety_moves.append((piece_pos, move))
                else:
                    regular_moves.append((piece_pos, move))
                
                # Undo the move
                board.undo_move(piece_pos, move, captured_piece)
        
        # Prioritize moves
        if check_moves:
            return random.choice(check_moves)
        elif capture_moves:
            # Sort captures by value and pick from top half
            capture_moves.sort(key=lambda x: x[2], reverse=True)
            best_half = capture_moves[:max(1, len(capture_moves)//2)]
            return random.choice(best_half)[:2]  # Return just the position and move
        elif king_safety_moves:
            return random.choice(king_safety_moves)
        else:
            return random.choice(regular_moves)
    
    elif difficulty == "HARD":
        # Simple minimax
        best_score = float('-inf')
        best_move = None
        
        for piece_pos, moves in all_pieces_with_moves:
            for move in moves:
                # Make move
                captured_piece = board.get_piece(move[0], move[1])
                board.make_move(piece_pos, move)
                
                # Evaluate position (minimax depth 2)
                opponent_color = 'b' if color == 'w' else 'w'
                score = minimax(board, 2, float('-inf'), float('inf'), False, color, opponent_color)
                
                # Undo move
                board.undo_move(piece_pos, move, captured_piece)
                
                if score > best_score:
                    best_score = score
                    best_move = (piece_pos, move)
        
        return best_move
    
    # Default fallback
    piece_pos, moves = random.choice(all_pieces_with_moves)
    return (piece_pos, random.choice(moves))

def minimax(board, depth, alpha, beta, is_maximizing, player_color, current_color):
    """Minimax algorithm with alpha-beta pruning"""
    # Check terminal conditions
    if depth == 0:
        return board.evaluate_board(player_color)
    
    opponent_color = 'b' if current_color == 'w' else 'w'
    
    # Check for checkmate/stalemate
    game_state = is_game_over(board, current_color)
    if game_state == "checkmate":
        return 1000 if opponent_color == player_color else -1000
    elif game_state == "stalemate":
        return 0
    
    # Find all legal moves
    all_moves = []
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == current_color:
                legal_moves = get_legal_moves(board, r, c)
                for move in legal_moves:
                    all_moves.append(((r, c), move))
    
    if is_maximizing:
        max_eval = float('-inf')
        for start, end in all_moves:
            captured_piece = board.get_piece(end[0], end[1])
            board.make_move(start, end)
            
            eval = minimax(board, depth - 1, alpha, beta, False, player_color, opponent_color)
            
            board.undo_move(start, end, captured_piece)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for start, end in all_moves:
            captured_piece = board.get_piece(end[0], end[1])
            board.make_move(start, end)
            
            eval = minimax(board, depth - 1, alpha, beta, True, player_color, opponent_color)
            
            board.undo_move(start, end, captured_piece)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
'''

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
                turn = player_color  # Switch turns
                
                # Check if the player is now in check
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