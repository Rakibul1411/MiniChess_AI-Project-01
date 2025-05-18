import pygame
import os
import math
import constants as const
from draw_title_button import draw_modern_button

def draw_star(screen, x, y, size, color):
    """
    Draw a five-pointed star at the specified position.
    
    Args:
        screen: The pygame screen to draw on
        x, y: Center position coordinates
        size: Size of the star
        color: Color of the star
    """
    points = []
    for i in range(10):
        if i % 2 == 0:
            angle = math.pi / 2 + (2 * math.pi / 10) * i
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
        else:
            angle = math.pi / 2 + (2 * math.pi / 10) * i
            px = x + (size * 0.4) * math.cos(angle)
            py = y + (size * 0.4) * math.sin(angle)
        points.append((px, py))
    pygame.draw.polygon(screen, color, points)
    pygame.draw.polygon(screen, const.WHITE, points, 1)

def load_game_over_sounds():
    """
    Load sound assets for the game over screen.
    
    Returns:
        Dictionary containing the sound assets
    """
    sounds = {
        'hover_sound': None,
        'click_sound': None,
        'game_over_sound': None
    }
    
    try:
        assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        pygame.mixer.init()
        sounds['hover_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'hover.mp3'))
        sounds['click_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'click.wav'))
        sounds['game_over_sound'] = pygame.mixer.Sound(os.path.join(assets_dir, 'game_over.wav'))
    except Exception as e:
        print(f"Error loading game over sounds: {e}")
    
    return sounds

def draw_game_over_screen(screen, game_state, turn, sounds=None, play_sound=True):
    """
    Draw a professional, aesthetic game over screen with state information and navigation buttons.
    
    Args:
        screen: The pygame screen to draw on
        game_state: "checkmate" or "stalemate"
        turn: Current turn ('w' or 'b')
        sounds: Dictionary containing sound assets (optional)
        play_sound: Whether to play the game over sound (default: True)
    
    Returns:
        Dictionary with button rectangles for click detection
    """
    # Load sounds if not provided
    if sounds is None:
        sounds = load_game_over_sounds()
    
    # Play game over sound if requested and add a flag to track if it's been played
    if play_sound and sounds['game_over_sound'] and not hasattr(draw_game_over_screen, 'game_over_sound_played'):
        sounds['game_over_sound'].play()
        draw_game_over_screen.game_over_sound_played = True
    
    # Create background overlay
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Load custom font if available, otherwise use system font
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    font_path = os.path.join(assets_dir, 'Rosemary.ttf')
    
    title_font = pygame.font.Font(font_path, 48) if os.path.exists(font_path) else \
                 pygame.font.SysFont("Georgia", 48, bold=True)
    subtitle_font = pygame.font.Font(font_path, 36) if os.path.exists(font_path) else \
                    pygame.font.SysFont("Georgia", 36, bold=True)
    button_font = pygame.font.Font(font_path, 28) if os.path.exists(font_path) else \
                  pygame.font.SysFont("Georgia", 28, bold=True)
    
    # Determine game over message
    if game_state == "checkmate":
        title_text = "Checkmate!"
        winner = "White" if turn == 'b' else "Black"
        subtitle_text = f"{winner} Wins!"
        title_color = const.GOLD  # Use GOLD constant for consistency
    else:  # stalemate
        title_text = "Stalemate!"
        subtitle_text = "Draw!"
        title_color = const.SILVER  # Use SILVER constant for consistency
    
    # Create central dialog box
    box_width = 500
    box_height = 320
    box_x = (const.WIDTH - box_width) // 2
    box_y = (const.HEIGHT - box_height) // 2
    
    # Draw the fancy box
    draw_fancy_box(screen, box_x, box_y, box_width, box_height, title_color)
    
    # Draw three small stars at the top
    star_y = box_y + 30
    star_spacing = 60
    star_size = 15
    for i in range(3):
        star_x = const.WIDTH // 2 + (i - 1) * star_spacing
        draw_star(screen, star_x, star_y, star_size, title_color)
    
    # Render title and subtitle
    title_surf = title_font.render(title_text, True, title_color)
    subtitle_surf = subtitle_font.render(subtitle_text, True, const.WHITE)
    
    # Position text in the box
    title_rect = title_surf.get_rect(center=(const.WIDTH // 2, box_y + 80))
    subtitle_rect = subtitle_surf.get_rect(center=(const.WIDTH // 2, box_y + 140))
    
    # Draw text
    screen.blit(title_surf, title_rect)
    screen.blit(subtitle_surf, subtitle_rect)
    
    # Create button positions (centered and in the box)
    buttons = {}
    button_width = 180
    button_height = 50
    button_spacing = 20
    button_y = box_y + box_height - 80
    
    # Play Again button
    play_again_x = const.WIDTH // 2 - button_width - button_spacing // 2
    play_again_rect = pygame.Rect(play_again_x, button_y, button_width, button_height)
    buttons["play_again"] = play_again_rect
    
    # Main Menu button
    menu_x = const.WIDTH // 2 + button_spacing // 2
    menu_rect = pygame.Rect(menu_x, button_y, button_width, button_height)
    buttons["menu"] = menu_rect
    
    # Initialize button states
    if not hasattr(draw_game_over_screen, 'button_states'):
        draw_game_over_screen.button_states = {
            'play_again': {'hover': False, 'played_sound': False},
            'menu': {'hover': False, 'played_sound': False}
        }
    
    # Draw buttons with consistent style
    draw_buttons(screen, buttons, button_font, draw_game_over_screen.button_states, sounds)
    
    return buttons

def draw_fancy_box(screen, x, y, width, height, accent_color):
    """
    Draw a fancy dialog box for the game over screen.
    
    Args:
        screen: The pygame screen to draw on
        x, y: Top-left coordinates of the box
        width, height: Dimensions of the box
        accent_color: Color for borders and decorative lines
    """
    box_color = const.DARK_GRAY  # Use DARK_GRAY constant for consistency
    border_radius = 15
    
    # Draw soft shadow for depth
    shadow_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
    shadow_rect = pygame.Rect(5, 5, width, height)
    pygame.draw.rect(shadow_surface, (0, 0, 0, 100), shadow_rect, border_radius=border_radius)
    screen.blit(shadow_surface, (x - 5, y - 5))
    
    # Main box with gradient effect
    box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(height):
        alpha = 230 - (i / height * 30)  # Gradient from top to bottom
        pygame.draw.line(box_surface, (box_color[0], box_color[1], box_color[2], alpha), 
                         (0, i), (width, i))
    
    # Apply rounded corners
    mask = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.rect(mask, (255, 255, 255), (0, 0, width, height), border_radius=border_radius)
    box_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    screen.blit(box_surface, (x, y))
    
    # Draw fancy border with accent color
    pygame.draw.rect(screen, accent_color, (x, y, width, height), 3, border_radius=border_radius)
    
    # Draw decorative lines at top and bottom
    line_margin = 20
    line_length = width - (line_margin * 2)
    line_height = 2
    pygame.draw.rect(screen, accent_color, 
                     (x + line_margin, y + 50, line_length, line_height))
    pygame.draw.rect(screen, accent_color, 
                     (x + line_margin, y + height - 120, line_length, line_height))

def draw_winner_symbol(screen, x, y, color, size=40):
    """
    Draw a chess crown/trophy symbol at the specified position.
    
    Args:
        screen: The pygame screen to draw on
        x, y: Position coordinates
        color: Color of the symbol
        size: Size of the symbol (default: 40)
    """
    points = []
    for i in range(5):
        angle_outer = math.pi / 2 + (2 * math.pi / 5) * i
        angle_inner = math.pi / 2 + (2 * math.pi / 5) * (i + 0.5)
        
        outer_x = x + size * math.cos(angle_outer)
        outer_y = y + size * math.sin(angle_outer)
        points.append((outer_x, outer_y))
        
        inner_x = x + (size * 0.6) * math.cos(angle_inner)
        inner_y = y + (size * 0.6) * math.sin(angle_inner)
        points.append((inner_x, inner_y))
    
    base_width = size * 1.5
    pygame.draw.polygon(screen, color, points)
    pygame.draw.rect(screen, color, 
                     (x - base_width / 2, y + size * 0.8, base_width, size * 0.3))
    
    pygame.draw.polygon(screen, const.WHITE, points, 1)
    pygame.draw.rect(screen, const.WHITE, 
                     (x - base_width / 2, y + size * 0.8, base_width, size * 0.3), 1)

def draw_buttons(screen, buttons, font, button_states, sounds=None):
    """
    Draw buttons with consistent modern style from draw_title_button.py
    
    Args:
        screen: The pygame screen to draw on
        buttons: Dictionary of button rectangles
        font: Font for button text
        button_states: Dictionary tracking button hover states
        sounds: Dictionary containing sound assets
    """
    mouse_pos = pygame.mouse.get_pos()
    
    if sounds is None:
        sounds = {'hover_sound': None}
    
    # Play Again button
    play_again_hover = buttons["play_again"].collidepoint(mouse_pos)
    
    # Play hover sound only once when the mouse first enters the button
    if play_again_hover and not button_states['play_again']['hover'] and sounds['hover_sound']:
        sounds['hover_sound'].play()
    
    # Update hover state
    button_states['play_again']['hover'] = play_again_hover
    
    draw_modern_button(
        screen, 
        buttons["play_again"], 
        "Play Again", 
        font, 
        play_again_hover,
        sounds,
        button_states,
        'play_again'
    )
    
    # Main Menu button
    menu_hover = buttons["menu"].collidepoint(mouse_pos)
    
    # Play hover sound only once when the mouse first enters the button
    if menu_hover and not button_states['menu']['hover'] and sounds['hover_sound']:
        sounds['hover_sound'].play()
    
    # Update hover state
    button_states['menu']['hover'] = menu_hover
    
    draw_modern_button(
        screen, 
        buttons["menu"], 
        "Main Menu", 
        font, 
        menu_hover,
        sounds,
        button_states,
        'menu'
    )

def handle_game_over_events(event, sounds=None):
    """
    Handle events for the game over screen.
    
    Args:
        event: The pygame event to handle
        sounds: Dictionary containing sound assets (optional)
        
    Returns:
        "DIFFICULTY", "MENU", or None
    """
    if sounds is None:
        sounds = load_game_over_sounds()
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        mouse_pos = pygame.mouse.get_pos()
        
        box_width = 500
        button_width = 180
        button_height = 50
        button_spacing = 20
        box_height = 320
        box_y = (const.HEIGHT - box_height) // 2
        button_y = box_y + box_height - 80
        
        play_again_x = const.WIDTH // 2 - button_width - button_spacing // 2
        play_again_rect = pygame.Rect(play_again_x, button_y, button_width, button_height)
        if play_again_rect.collidepoint(mouse_pos):
            if sounds['click_sound']:
                sounds['click_sound'].play()
            # Reset sound flags when navigating away from game over screen
            if hasattr(draw_game_over_screen, 'game_over_sound_played'):
                delattr(draw_game_over_screen, 'game_over_sound_played')
            if hasattr(draw_game_over_screen, 'button_states'):
                delattr(draw_game_over_screen, 'button_states')
            return "DIFFICULTY"
        
        menu_x = const.WIDTH // 2 + button_spacing // 2
        menu_rect = pygame.Rect(menu_x, button_y, button_width, button_height)
        if menu_rect.collidepoint(mouse_pos):
            if sounds['click_sound']:
                sounds['click_sound'].play()
            # Reset sound flags when navigating away from game over screen
            if hasattr(draw_game_over_screen, 'game_over_sound_played'):
                delattr(draw_game_over_screen, 'game_over_sound_played')
            if hasattr(draw_game_over_screen, 'button_states'):
                delattr(draw_game_over_screen, 'button_states')
            return "MENU"
    
    return None