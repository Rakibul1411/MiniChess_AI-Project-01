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
        return False  
    
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
    
    captured_piece, was_promoted, original_piece = board.make_move(start, end)
    
    
    result = is_in_check(board, color)
    
    
    board.undo_move(start, end, captured_piece, was_promoted, original_piece)
    
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
    """Check if the game is over (checkmate, stalemate, or insufficient material)"""
    # First, check for insufficient material (only kings remaining)
    only_kings_remain = True
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and 'king' not in piece:  
                only_kings_remain = False
                break
        if not only_kings_remain:
            break
    
    if only_kings_remain:
        return "insufficient_material"  
    
    # Continue with the original logic for checkmate and stalemate
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
            return "checkmate"  
        else:
            return "stalemate"  
    
    return None