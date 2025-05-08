import pygame
import os

def create_placeholder_piece(piece_key, square_size):
    """Create a placeholder piece when image is missing"""
    surf = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    
    # Draw circle background with appropriate color
    circle_color = (60, 60, 60, 230) if piece_key[0] == 'b' else (240, 240, 240, 230)
    pygame.draw.circle(surf, circle_color, (square_size//2, square_size//2), square_size//2 - 5)
    
    # Add identifying letter
    font = pygame.font.SysFont("Arial", square_size // 2)
    letter = piece_key[1].upper()
    text_color = (200, 200, 200) if piece_key[0] == 'b' else (50, 50, 50)
    text = font.render(letter, True, text_color)
    text_rect = text.get_rect(center=(square_size/2, square_size/2))
    surf.blit(text, text_rect)
    
    # Add subtle border
    pygame.draw.circle(surf, (180, 180, 180, 150), (square_size//2, square_size//2), 
                     square_size//2 - 5, 2)
    
    return surf

def load_and_scale_image(path, square_size, image_size):
    """Load and properly scale a single chess piece image"""
    try:
        original_img = pygame.image.load(path).convert_alpha()
        img_surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
        scaled_img = pygame.transform.smoothscale(original_img, (image_size, image_size))
        
        # Center the piece in the square
        pos_x = (square_size - image_size) // 2
        pos_y = (square_size - image_size) // 2
        img_surface.blit(scaled_img, (pos_x, pos_y))
        
        return img_surface
    except pygame.error:
        return None

def ensure_assets_directory(assets_dir):
    """Create assets directory if it doesn't exist"""
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        print(f"Created assets directory at {assets_dir}")
        print("Please ensure you have all required chess piece images in this directory.")

def get_piece_mapping():
    """Return the mapping of piece keys to filenames"""
    return {
        'bbishop': 'black_bishop.png',
        'bking':   'black_king.png',
        'bknight': 'black_knight.png',
        'bpawn':   'black_pawn.png',
        'bqueen':  'black_queen.png',
        'brook':   'black_rook.png',
        'wbishop': 'white_bishop.png',
        'wking':   'white_king.png',
        'wknight': 'white_knight.png',
        'wpawn':   'white_pawn.png',
        'wqueen':  'white_queen.png',
        'wrook':   'white_rook.png',
    }

def load_piece_images(square_size):
    """Main function to load all chess piece images with proper scaling and centering"""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    ensure_assets_directory(assets_dir)
    
    images = {}
    file_map = get_piece_mapping()
    image_size = int(square_size * 0.85)  # Slightly smaller than square for visual balance
    
    for piece_key, fname in file_map.items():
        path = os.path.join(assets_dir, fname)
        img = load_and_scale_image(path, square_size, image_size)
        
        if img:
            images[piece_key] = img
        else:
            print(f"Warning: Could not load image {fname}. Using placeholder.")
            images[piece_key] = create_placeholder_piece(piece_key, square_size)
    
    return images