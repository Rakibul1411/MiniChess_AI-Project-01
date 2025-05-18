import random
import time
from app_game_move import get_legal_moves, find_king, is_in_check, is_game_over


pruning_stats = {'cuts': 0}


def get_all_pieces_with_moves(board, color):
    pieces_with_moves = []
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == color:
                legal_moves = get_legal_moves(board, r, c)
                if legal_moves:
                    pieces_with_moves.append(((r, c), legal_moves))
    return pieces_with_moves


def get_sorted_moves(board, color, all_pieces_with_moves):
    sorted_moves = []
    for (r, c), moves in all_pieces_with_moves:
        for move in moves:
            captured = board.get_piece(move[0], move[1])
            board.make_move((r, c), move)
            score = board.evaluate_board(color)  
            board.undo_move((r, c), move, captured)
            sorted_moves.append(((r, c), move, score))
    
    sorted_moves.sort(key=lambda x: x[2], reverse=True)
    ordered_moves = [(start, end) for start, end, _ in sorted_moves]
    return ordered_moves


def get_ai_move(board, color, difficulty):
    
    start_time=time.time()
    current_color=color
    all_pieces_with_moves=get_all_pieces_with_moves(board, color)

    if not all_pieces_with_moves:
        return None

    depth=-1
    if difficulty == "EASY":
        depth=2
    elif difficulty == "MEDIUM":
        depth=3
    elif difficulty == "HARD":
        depth=4
    elif difficulty == "":
        depth=4

    total_pieces = sum(1 for r in range(board.height) 
                     for c in range(board.width) 
                     if board.get_piece(r, c))
    
    if total_pieces <= 11: 
        depth+=1  
        print(f"Endgame detected ({total_pieces} pieces), increasing depth to {depth}")
    elif total_pieces <= 7:  
        depth+=1
        print(f"Late endgame detected ({total_pieces} pieces), increasing depth to {depth}")

    ordered_moves=get_sorted_moves(board, color, all_pieces_with_moves)
        
    best_score = float('-inf')
    best_move = None
        
    timeout = 4.0  
    last_valid_move = best_move
    last_valid_score = best_score
    
    for start, end in ordered_moves:
        if time.time() - start_time > timeout:
            print(f"Timeout! Returning best move found after {time.time()-start_time:.2f}s")
            return last_valid_move
        
        captured = board.get_piece(end[0], end[1])
        board.make_move(start, end)
        
        try:
            score = minimax(board, depth-1, -float('inf'), float('inf'), 
                          False, color, 'b' if color == 'w' else 'w')
        except TimeoutError:
            board.undo_move(start, end, captured)
            print(f"Timeout during evaluation! Returning best move so far")
            return last_valid_move
        
        board.undo_move(start, end, captured)
        
        if score > best_score:
            best_score = score
            best_move = (start, end)
            last_valid_move = best_move
            last_valid_score = best_score
            
            if best_score >= 1000:  
                break
    
    elapsed = time.time() - start_time
    print(f"Move found in {elapsed:.2f}s | Score: {best_score}")
    return best_move

    

def minimax(board, depth, alpha, beta, is_maximizing, player_color, current_color):

    game_state = is_game_over(board, current_color)
    opponent_color = 'b' if current_color == 'w' else 'w'

    if depth == 0 or game_state:
        return heuristic_function(board, player_color, opponent_color, game_state)
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
                pruning_stats['cuts'] += 1
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
                pruning_stats['cuts'] += 1
                break
        return min_eval


def count_controlled_squares(board, color):
    
    controlled = set()  
    for r in range(board.height):
        for c in range(board.width):
            piece = board.get_piece(r, c)
            if piece and piece[0] == color:
                for move in board.get_valid_moves(r, c):
                    controlled.add(move) 
    
    return len(controlled)


def evaluate_space_control(board, color):
    opponent_color = 'b' if color == 'w' else 'w'
    player_control = count_controlled_squares(board, color)
    opponent_control = count_controlled_squares(board, opponent_color)
    return (player_control - opponent_control) * 0.1


def heuristic_function(board, player_color, opponent_color, game_state):
    if game_state == "checkmate":
        return 1000 if opponent_color == player_color else -1000
    elif game_state in ["stalemate", "insufficient_material"]:
        return 0  # Draw situations return 0

    score=board.evaluate_board(player_color)

    WINNING_THRESHOLD=3  
    WINNING_BONUS=0.1   
    winning_prob_bonus=0

    if score>WINNING_THRESHOLD:
        player_moves=len(get_all_pieces_with_moves(board,player_color))
        opponent_moves=len(get_all_pieces_with_moves(board,opponent_color))
        
        winning_prob_bonus=(player_moves-opponent_moves)*WINNING_BONUS

    space_advantage=evaluate_space_control(board, player_color)
    space_bonus=0.2*space_advantage

    return score+winning_prob_bonus+space_bonus