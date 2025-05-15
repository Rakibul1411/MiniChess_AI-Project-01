import random
from app_game_move import get_legal_moves, find_king, is_in_check, is_game_over

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