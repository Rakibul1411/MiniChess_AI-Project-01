import pygame
import random
import constants as const

class Board:
    """
    Enhanced chess board class with beautiful visuals and game logic,
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
    
    def _create_wood_texture(self):
        """Create wood texture for board borders"""
        self.border_texture = pygame.Surface(
            (self.width * self.square_size, self.height * self.square_size), 
            pygame.SRCALPHA
        )
        for i in range(100):
            shade = random.randint(80, 120)
            pygame.draw.line(
                self.border_texture, 
                (shade, shade-30, shade-60), 
                (0, i), 
                (self.width * self.square_size, i)
            )
    
    def _create_coordinate_markers(self):
        """Create coordinate markers for board edges"""
        self.coord_font = pygame.font.SysFont("Arial", 14, bold=True)
        self.rank_labels = [
            self.coord_font.render(str(i+1), True, (255, 255, 255)) 
            for i in range(self.height)
        ]
        self.file_labels = [
            self.coord_font.render(chr(97+i), True, (255, 255, 255)) 
            for i in range(self.width)
        ]

    # Board drawing methods
    def draw(self, screen, y_offset=0):
        """Draw the chess board with all visual elements"""
        self._draw_board_border(screen, y_offset)
        self._draw_chess_squares(screen, y_offset)
        self._draw_coordinates(screen, y_offset)
    
    def _draw_board_border(self, screen, y_offset):
        """Draw the wooden border around the chess board"""
        border_rect = pygame.Rect(
            -10, y_offset-10, 
            self.width*self.square_size+20, 
            self.height*self.square_size+20
        )
        pygame.draw.rect(screen, (80, 50, 30), border_rect, border_radius=8)
        screen.blit(self.border_texture, (0, y_offset))
    
    def _draw_chess_squares(self, screen, y_offset):
        """Draw all chess squares with textures and effects"""
        for r in range(self.height):
            for c in range(self.width):
                self._draw_single_square(screen, r, c, y_offset)
    
    def _draw_single_square(self, screen, row, col, y_offset):
        """Draw a single chess square with visual effects"""
        base_color = const.LIGHT_SQUARE if (row + col) % 2 == 0 else const.DARK_SQUARE
        square_surf = pygame.Surface((self.square_size, self.square_size))
        
        self._apply_square_texture(square_surf, base_color, row, col)
        self._apply_square_border(square_surf, base_color)
        
        screen.blit(
            square_surf, 
            (col*self.square_size, row*self.square_size + y_offset)
        )
    
    def _apply_square_texture(self, surface, base_color, row, col):
        """Apply wood grain texture to a square"""
        surface.fill(base_color)
        for i in range(5):
            shade = 20 if (row + col) % 2 == 0 else -20
            adjusted_color = (
                min(255, max(0, base_color[0]+shade)),
                min(255, max(0, base_color[1]+shade)),
                min(255, max(0, base_color[2]+shade))
            )
            pygame.draw.line(
                surface, adjusted_color, 
                (0, i*self.square_size//5), 
                (self.square_size, i*self.square_size//5), 
                1
            )
    
    def _apply_square_border(self, surface, base_color):
        """Apply 3D border effect to a square"""
        border_color = (
            min(255, base_color[0]+30), 
            min(255, base_color[1]+30), 
            min(255, base_color[2]+30)
        )
        pygame.draw.rect(
            surface, border_color, 
            (0, 0, self.square_size, self.square_size), 
            1
        )
    
    def _draw_coordinates(self, screen, y_offset):
        """Draw rank and file coordinates"""
        for i in range(self.height):
            screen.blit(
                self.rank_labels[i], 
                (5, y_offset + i*self.square_size + 5)
            )
        for i in range(self.width):
            screen.blit(
                self.file_labels[i], 
                (i*self.square_size + self.square_size - 15, 
                y_offset + (self.height-1)*self.square_size + self.square_size - 20)
            )

    # Piece drawing methods
    def draw_pieces(self, screen, images, y_offset=0):
        """Draw all chess pieces with visual effects"""
        for r in range(self.height):
            for c in range(self.width):
                piece = self.board[r][c]
                if piece:
                    self._draw_single_piece(screen, images, r, c, piece, y_offset)
    
    def _draw_single_piece(self, screen, images, row, col, piece, y_offset):
        """Draw a single chess piece with effects"""
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
        """Draw shadow under a chess piece"""
        shadow_surf = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        shadow_radius = self.square_size // 3
        pygame.draw.circle(
            shadow_surf, (0, 0, 0, 80), 
            (self.square_size//2, self.square_size//2 + 2), 
            shadow_radius
        )
        shadow_rect = shadow_surf.get_rect(center=(center_x, center_y))
        screen.blit(shadow_surf, shadow_rect)
    
    def _draw_king_glow(self, screen, center_x, center_y, color):
        """Draw special glow effect for kings"""
        glow = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        glow_color = (255, 215, 0, 50) if color == 'w' else (200, 200, 255, 50)
        pygame.draw.circle(
            glow, glow_color, 
            (self.square_size//2, self.square_size//2), 
            self.square_size//2
        )
        glow_rect = glow.get_rect(center=(center_x, center_y))
        screen.blit(glow, glow_rect)

    # Highlighting methods
    def highlight_square(self, screen, row, col, color, y_offset=0):
        """Highlight a square with visual effects"""
        center_x, center_y = self._get_square_center(col, row, y_offset)
        highlight_surf = self._create_highlight_surface(color)
        highlight_rect = highlight_surf.get_rect(center=(center_x, center_y))
        screen.blit(highlight_surf, highlight_rect)
    
    def _create_highlight_surface(self, color):
        """Create the appropriate highlight effect based on type"""
        s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        
        if color == const.HIGHLIGHT_COLOR:  # Selected piece
            self._draw_selection_highlight(s)
        elif color == const.MOVE_COLOR:    # Valid move
            self._draw_move_highlight(s)
        elif color == const.LAST_MOVE_COLOR:  # Last move
            self._draw_last_move_highlight(s)
        
        return s
    
    def _draw_selection_highlight(self, surface):
        """Draw golden halo for selected piece"""
        highlight_radius = self.square_size//2 - 5
        pygame.draw.circle(
            surface, (255, 215, 0, 150), 
            (self.square_size//2, self.square_size//2), 
            highlight_radius
        )
        inner_radius = self.square_size//3
        pygame.draw.circle(
            surface, (255, 255, 255, 200), 
            (self.square_size//2, self.square_size//2), 
            inner_radius
        )
    
    def _draw_move_highlight(self, surface):
        """Draw pulsating green circle for valid moves"""
        radius = int(self.square_size//3 * (0.8 + 0.2 * abs(pygame.time.get_ticks() % 1000 - 500)/500))
        pygame.draw.circle(
            surface, (50, 200, 50, 180), 
            (self.square_size//2, self.square_size//2), 
            radius
        )
    
    def _draw_last_move_highlight(self, surface):
        """Draw animated blue arrows for last move"""
        arrow_size = self.square_size//4
        time_offset = pygame.time.get_ticks() % 1000 / 1000
        for i in range(2):
            offset = (i * 2 - 1) * (5 + 5 * time_offset)
            points = [
                (self.square_size//2 - arrow_size + offset, self.square_size//2),
                (self.square_size//2 + arrow_size + offset, self.square_size//2),
                (self.square_size//2 + offset, self.square_size//2 + arrow_size)
            ]
            pygame.draw.polygon(
                surface, (0, 100, 255, 200), 
                points
            )

    # Game logic methods
    def get_piece(self, row, col):
        """Get the piece at a specific position"""
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.board[row][col]
        return None
    
    # def make_move(self, start, end):
    #     """Move a piece from start to end position"""
    #     sr, sc = start
    #     er, ec = end
    #     self.board[er][ec] = self.board[sr][sc]
    #     self.board[sr][sc] = None

    def make_move(self, start, end):
        """Move a piece from start to end position and handle pawn promotion"""
        sr, sc = start
        er, ec = end
        moving_piece = self.board[sr][sc]
    
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
    
    def undo_move(self, start, end, captured_piece):
        """Undo a move by restoring original positions"""
        sr, sc = start
        er, ec = end
        self.board[sr][sc] = self.board[er][ec]
        self.board[er][ec] = captured_piece
    
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
      
def _draw_check_highlight(self, surface):
    """Draw red pulsing effect for king in check"""
    radius = int(self.square_size//2 * (0.9 + 0.1 * abs(pygame.time.get_ticks() % 1000 - 500)/500))
    pygame.draw.circle(
        surface, (255, 0, 0, 180), 
        (self.square_size//2, self.square_size//2), 
        radius
    )
    # Inner white circle for better visibility
    pygame.draw.circle(
        surface, (255, 255, 255, 100), 
        (self.square_size//2, self.square_size//2), 
        radius//2
    )      
      