import pygame
import random
import constants as const

class Board:
    """
    Enhanced chess board class with professional visuals and game logic,
    organized into smaller, focused methods.
    """
    
    def __init__(self, width, height, square_size):
        self.width = width
        self.height = height
        self.square_size = square_size
        self.board = self._init_starting_position()
        self._init_decorative_elements()
    
    def _init_starting_position(self):
        """Initialize the chess board with pieces in starting positions"""
        board = [[None]*self.width for _ in range(self.height)]
        # Set up black pieces
        board[0] = ['brook','bknight','bbishop','bqueen','bking','bbishop','bknight','brook']
        board[1] = ['bpawn'] * self.width
        # Set up white pieces
        board[-2] = ['wpawn'] * self.width
        board[-1] = ['wrook','wknight','wbishop','wqueen','wking','wbishop','wknight','wrook']
        return board
    
    def _init_decorative_elements(self):
        """Initialize visual decorative elements for the board"""
        self._create_wood_texture()
        self._create_coordinate_markers()
        self._create_board_shadow()
    
    def _create_wood_texture(self):
        """Create refined wood texture for board borders"""
        self.border_texture = pygame.Surface(
            (self.width * self.square_size + 20, self.height * self.square_size + 20), 
            pygame.SRCALPHA
        )
        for i in range(0, self.border_texture.get_height(), 2):
            shade = random.randint(80, 100)
            grain_color = (
                shade,
                max(0, shade - 20),
                max(0, shade - 40)
            )
            pygame.draw.line(
                self.border_texture, 
                grain_color, 
                (0, i), 
                (self.border_texture.get_width(), i)
            )
    
    def _create_coordinate_markers(self):
        """Create modern coordinate markers for board edges"""
        self.coord_font = pygame.font.SysFont("Helvetica", 16, bold=True)
        self.rank_labels = [
            self.coord_font.render(str(i+1), True, const.TEXT_COLOR) 
            for i in range(self.height)
        ]
        self.file_labels = [
            self.coord_font.render(chr(97+i), True, const.TEXT_COLOR) 
            for i in range(self.width)
        ]
    
    def _create_board_shadow(self):
        """Create subtle shadow for the entire board"""
        self.shadow_surface = pygame.Surface(
            (self.width * self.square_size + 30, self.height * self.square_size + 30),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.shadow_surface, const.SHADOW_COLOR,
            (0, 0, self.shadow_surface.get_width(), self.shadow_surface.get_height()),
            border_radius=12
        )
    
    # Board drawing methods
    def draw(self, screen, y_offset=0):
        """Draw the chess board with all visual elements"""
        self._draw_board_shadow(screen, y_offset)
        self._draw_board_border(screen, y_offset)
        self._draw_chess_squares(screen, y_offset)
        self._draw_coordinates(screen, y_offset)
    
    def _draw_board_shadow(self, screen, y_offset):
        """Draw the board's shadow for depth"""
        screen.blit(self.shadow_surface, (-15, y_offset - 15))
    
    def _draw_board_border(self, screen, y_offset):
        """Draw the refined wooden border around the chess board"""
        border_rect = pygame.Rect(
            -10, y_offset-10, 
            self.width*self.square_size+20, 
            self.height*self.square_size+20
        )
        pygame.draw.rect(screen, const.BOARD_BORDER, border_rect, border_radius=12)
        screen.blit(self.border_texture, (-10, y_offset-10))
    
    def _draw_chess_squares(self, screen, y_offset):
        """Draw all chess squares with enhanced textures"""
        for r in range(self.height):
            for c in range(self.width):
                self._draw_single_square(screen, r, c, y_offset)
    
    def _draw_single_square(self, screen, row, col, y_offset):
        """Draw a single chess square with professional visual effects"""
        base_color = const.LIGHT_SQUARE if (row + col) % 2 == 0 else const.DARK_SQUARE
        square_surf = pygame.Surface((self.square_size, self.square_size))
        
        self._apply_square_texture(square_surf, base_color, row, col)
        self._apply_square_border(square_surf, base_color)
        
        screen.blit(
            square_surf, 
            (col*self.square_size, row*self.square_size + y_offset)
        )
    
    def _apply_square_texture(self, surface, base_color, row, col):
        """Apply smooth wood grain texture to a square"""
        surface.fill(base_color)
        for i in range(0, self.square_size, 3):
            shade = random.randint(-10, 10)
            adjusted_color = (
                min(255, max(0, base_color[0] + shade)),
                min(255, max(0, base_color[1] + shade)),
                min(255, max(0, base_color[2] + shade))
            )
            pygame.draw.line(
                surface, adjusted_color, 
                (0, i), 
                (self.square_size, i),
                1
            )
    
    def _apply_square_border(self, surface, base_color):
        """Apply subtle 3D border effect to a square"""
        border_color = (
            min(255, base_color[0] + 20), 
            min(255, base_color[1] + 20), 
            min(255, base_color[2] + 20)
        )
        pygame.draw.rect(
            surface, border_color, 
            (0, 0, self.square_size, self.square_size), 
            1
        )
    
    def _draw_coordinates(self, screen, y_offset):
        """Draw modern rank and file coordinates"""
        for i in range(self.height):
            screen.blit(
                self.rank_labels[i], 
                (-5, y_offset + i*self.square_size + 10)
            )
        for i in range(self.width):
            screen.blit(
                self.file_labels[i], 
                (i*self.square_size + self.square_size - 20, 
                 y_offset + self.height*self.square_size + 5)
            )

    # Piece drawing methods
    def draw_pieces(self, screen, images, y_offset=0):
        """Draw all chess pieces with enhanced visual effects"""
        for r in range(self.height):
            for c in range(self.width):
                piece = self.board[r][c]
                if piece:
                    self._draw_single_piece(screen, images, r, c, piece, y_offset)
    
    def _draw_single_piece(self, screen, images, row, col, piece, y_offset):
        """Draw a single chess piece with refined effects"""
        center_x, center_y = self._get_square_center(col, row, y_offset)
        
        self._draw_piece_shadow(screen, center_x, center_y)
        if 'king' in piece:
            self._draw_king_glow(screen, center_x, center_y, piece[0])
        
        piece_img = images[piece]
        piece_rect = piece_img.get_rect(center=(center_x, center_y))
        screen.blit(piece_img, piece_rect)
    
    def _get_square_center(self, col, row, y_offset):
        """Calculate the exact center of a square"""
        return (
            col * self.square_size + self.square_size // 2,
            row * self.square_size + self.square_size // 2 + y_offset
        )
    
    def _draw_piece_shadow(self, screen, center_x, center_y):
        """Draw refined shadow under a chess piece"""
        shadow_surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        shadow_radius = self.square_size // 3
        pygame.draw.circle(
            shadow_surf, (0, 0, 0, 60), 
            (self.square_size//2, self.square_size//2 + 3), 
            shadow_radius
        )
        shadow_rect = shadow_surf.get_rect(center=(center_x, center_y))
        screen.blit(shadow_surf, shadow_rect)
    
    def _draw_king_glow(self, screen, center_x, center_y, color):
        """Draw elegant glow effect for kings"""
        glow = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        glow_color = (189, 162, 102, 60) if color == 'w' else (150, 150, 200, 60)
        pygame.draw.circle(
            glow, glow_color, 
            (self.square_size//2, self.square_size//2), 
            self.square_size//2
        )
        glow_rect = glow.get_rect(center=(center_x, center_y))
        screen.blit(glow, glow_rect)

    # Highlighting methods
    def highlight_square(self, screen, row, col, color, y_offset=0):
        """Highlight a square with professional visual effects"""
        center_x, center_y = self._get_square_center(col, row, y_offset)
        highlight_surf = self._create_highlight_surface(color)
        highlight_rect = highlight_surf.get_rect(center=(center_x, center_y))
        screen.blit(highlight_surf, highlight_rect)
    
    def _create_highlight_surface(self, color):
        """Create refined highlight effect based on type"""
        s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        if color == const.HIGHLIGHT_COLOR:  # Selected piece
            self._draw_selection_highlight(s)
        elif color == const.MOVE_COLOR:    # Valid move
            self._draw_move_highlight(s)
        elif color == const.LAST_MOVE_COLOR:  # Last move
            self._draw_last_move_highlight(s)
        elif color == const.CHECK_COLOR:  # King in check
            self._draw_check_highlight(s)
        
        return s
    
    def _draw_selection_highlight(self, surface):
        """Draw elegant golden halo for selected piece"""
        highlight_radius = self.square_size // 2 - 5
        pygame.draw.circle(
            surface, const.HIGHLIGHT_COLOR, 
            (self.square_size//2, self.square_size//2), 
            highlight_radius
        )
        inner_radius = self.square_size // 3
        pygame.draw.circle(
            surface, (255, 255, 255, 100), 
            (self.square_size//2, self.square_size//2), 
            inner_radius
        )
    
    def _draw_move_highlight(self, surface):
        """Draw smooth pulsating green circle for valid moves"""
        pulse = abs(pygame.time.get_ticks() % 1200 - 600) / 600
        radius = int(self.square_size // 3 * (0.7 + 0.3 * pulse))
        pygame.draw.circle(
            surface, const.MOVE_COLOR, 
            (self.square_size//2, self.square_size//2), 
            radius
        )
    
    def _draw_last_move_highlight(self, surface):
        """Draw refined blue glow for last move"""
        glow_radius = self.square_size // 2 - 5
        pygame.draw.circle(
            surface, const.LAST_MOVE_COLOR, 
            (self.square_size//2, self.square_size//2), 
            glow_radius
        )
        inner_radius = self.square_size // 3
        pygame.draw.circle(
            surface, (255, 255, 255, 80), 
            (self.square_size//2, self.square_size//2), 
            inner_radius
        )
    
    def _draw_check_highlight(self, surface):
        """Draw red pulsing effect for king in check"""
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        radius = int(self.square_size // 2 * (0.8 + 0.2 * pulse))
        pygame.draw.circle(
            surface, const.CHECK_COLOR, 
            (self.square_size//2, self.square_size//2), 
            radius
        )
        pygame.draw.circle(
            surface, (255, 255, 255, 80), 
            (self.square_size//2, self.square_size//2), 
            radius // 2
        )

    # Game logic methods
    def get_piece(self, row, col):
        """Get the piece at a specific position"""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.board[row][col]
        return None
    
    def make_move(self, start, end):
        """Move a piece from start to end position and handle pawn promotion"""
        sr, sc = start
        er, ec = end
        moving_piece = self.board[sr][sc]
        captured_piece = self.board[er][ec]  # Store the captured piece
        was_promoted = False  # Track if promotion occurred
        original_piece = moving_piece  # Store the original piece before promotion

        # Move the piece
        self.board[er][ec] = moving_piece
        self.board[sr][sc] = None

        # Check for pawn promotion
        if moving_piece and 'pawn' in moving_piece:
            color = moving_piece[0]
            # White pawn reached top row (row 0) or black pawn reached bottom row (row board.height-1)
            if (color == 'w' and er == 0) or (color == 'b' and er == self.height - 1):
                # Promote to queen
                self.board[er][ec] = f"{color}queen"
                was_promoted = True

        return captured_piece, was_promoted, original_piece  # Return additional info for undo
    
    def undo_move(self, start, end, captured_piece, was_promoted, original_piece):
        """Undo a move by restoring original positions, handling pawn promotion"""
        sr, sc = start
        er, ec = end
        # If the move involved a promotion, restore the original piece (pawn)
        if was_promoted:
            self.board[sr][sc] = original_piece  # Restore the original pawn
        else:
            self.board[sr][sc] = self.board[er][ec]  # Otherwise, move the piece back as usual
        self.board[er][ec] = captured_piece  # Restore the captured piece (or None)
    
    # Move generation methods
    def get_valid_moves(self, row, col):
        """Get all valid moves for the piece at given position"""
        piece = self.get_piece(row, col)
        if not piece:
            return []
        
        typ = piece[1:]  # Piece type (e.g., 'pawn', 'rook')
        color = piece[0] # Piece color ('w' or 'b')
        
        if typ == 'pawn':
            return self._get_pawn_moves(row, col, color)
        elif typ in ('rook', 'bishop', 'queen'):
            return self._get_sliding_moves(row, col, color, typ)
        elif typ == 'knight':
            return self._get_knight_moves(row, col, color)
        elif typ == 'king':
            return self._get_king_moves(row, col, color)
        
        return []
    
    def _get_pawn_moves(self, row, col, color):
        """Calculate valid moves for a pawn"""
        moves = []
        direction = -1 if color == 'w' else 1
        start_row = self.height-2 if color == 'w' else 1
        
        # Forward moves
        if self._is_valid_position(row + direction, col) and not self.board[row + direction][col]:
            moves.append((row + direction, col))
            if row == start_row and self._is_valid_position(row + 2*direction, col) and not self.board[row + 2*direction][col]:
                moves.append((row + 2*direction, col))
        
        # Capture moves
        for dc in (-1, 1):
            if self._is_valid_position(row + direction, col + dc):
                target = self.board[row + direction][col + dc]
                if target and target[0] != color:
                    moves.append((row + direction, col + dc))
        
        return moves
    
    def _get_sliding_moves(self, row, col, color, piece_type):
        """Calculate moves for rook, bishop, or queen"""
        moves = []
        directions = []
        
        if piece_type in ('rook', 'queen'):
            directions.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])  # Rook directions
        if piece_type in ('bishop', 'queen'):
            directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])  # Bishop directions
        
        for dr, dc in directions:
            for i in range(1, max(self.width, self.height)):
                nr, nc = row + dr*i, col + dc*i
                if not self._is_valid_position(nr, nc):
                    break
                
                if not self.board[nr][nc]:
                    moves.append((nr, nc))
                else:
                    if self.board[nr][nc][0] != color:
                        moves.append((nr, nc))
                    break
        
        return moves
    
    def _get_knight_moves(self, row, col, color):
        """Calculate valid moves for a knight"""
        moves = []
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            nr, nc = row + dr, col + dc
            if self._is_valid_position(nr, nc):
                target = self.board[nr][nc]
                if not target or target[0] != color:
                    moves.append((nr, nc))
        
        return moves
    
    def _get_king_moves(self, row, col, color):
        """Calculate valid moves for a king"""
        moves = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if self._is_valid_position(nr, nc):
                    target = self.board[nr][nc]
                    if not target or target[0] != color:
                        moves.append((nr, nc))
        return moves
    
    def _is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.height and 0 <= col < self.width
    
    def get_all_moves(self, color):
        """Get all possible moves for pieces of given color"""
        all_moves = []
        for r in range(self.height):
            for c in range(self.width):
                piece = self.board[r][c]
                if piece and piece[0] == color:
                    valid_moves = self.get_valid_moves(r, c)
                    for move in valid_moves:
                        all_moves.append(((r, c), move))
        return all_moves
    
    # Evaluation methods
    def get_piece_value(self, piece_type):
        """Get the value of a chess piece"""
        values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 100
        }
        return values.get(piece_type[1:], 0)
    
    def evaluate_board(self, color):
        """Evaluate the board position for the given color"""
        score = 0
        for r in range(self.height):
            for c in range(self.width):
                piece = self.board[r][c]
                if piece:
                    value = self.get_piece_value(piece)
                    if piece[0] == color:
                        score += value
                    else:
                        score -= value
        return score