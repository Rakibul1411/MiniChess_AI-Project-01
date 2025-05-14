# color_selection.py
import pygame
import os
import sys
import math
import random
import constants as const

def draw_board_preview(screen, x, y, size, color_choice):
    """Draw a small chess board preview with player pieces in the selected color"""
    square_size = size // 8
    is_white = color_choice == "WHITE"
    
    # Draw the board
    for row in range(8):
        for col in range(8):
            color = const.LIGHT_SQUARE if (row + col) % 2 == 0 else const.DARK_SQUARE
            pygame.draw.rect(
                screen, 
                color, 
                pygame.Rect(x + col * square_size, y + row * square_size, square_size, square_size)
            )
    
    # Draw player's pieces (at bottom if white, top if black)
    player_row = 6 if is_white else 1
    player_color = const.WHITE if is_white else const.BLACK
    opponent_row = 1 if is_white else 6
    opponent_color = const.BLACK if is_white else const.WHITE
    
    # Draw player pawns
    for col in range(8):
        # Player pawns
        pygame.draw.circle(
            screen,
            player_color,
            (x + col * square_size + square_size//2, y + player_row * square_size + square_size//2),
            square_size // 3
        )
        # Opponent pawns
        pygame.draw.circle(
            screen,
            opponent_color,
            (x + col * square_size + square_size//2, y + opponent_row * square_size + square_size//2),
            square_size // 3
        )
    
    # Draw player major pieces (bottom row)
    player_back_row = 7 if is_white else 0
    opponent_back_row = 0 if is_white else 7
    
    # Draw player pieces
    for col in range(8):
        piece_size = square_size // 2
        # Player pieces
        pygame.draw.rect(
            screen,
            player_color,
            pygame.Rect(
                x + col * square_size + square_size//4,
                y + player_back_row * square_size + square_size//4,
                piece_size,
                piece_size
            ),
            border_radius=5
        )
        # Opponent pieces
        pygame.draw.rect(
            screen,
            opponent_color,
            pygame.Rect(
                x + col * square_size + square_size//4,
                y + opponent_back_row * square_size + square_size//4,
                piece_size,
                piece_size
            ),
            border_radius=5
        )
    
    # Draw border around the board
    pygame.draw.rect(
        screen,
        const.GOLD,
        pygame.Rect(x, y, size, size),
        width=3,
        border_radius=2
    )

def create_gradient_button(screen, rect, base_color, hover=False, selected=False):
    """Create a gradient button with hover and selected effect"""
    if selected:
        base_color = (min(base_color[0] + 60, 255), min(base_color[1] + 60, 255), min(base_color[2] + 60, 255))
    elif hover:
        base_color = (min(base_color[0] + 30, 255), min(base_color[1] + 30, 255), min(base_color[2] + 30, 255))
    
    gradient = pygame.Surface((rect.width, rect.height))
    for i in range(rect.height):
        intensity = 1 - (i / rect.height) * 0.3
        color = (
            int(base_color[0] * intensity),
            int(base_color[1] * intensity),
            int(base_color[2] * intensity)
        )
        pygame.draw.line(gradient, color, (0, i), (rect.width, i))
    screen.blit(gradient, rect)
    
    # Add border
    border_color = (255, 255, 255, 200) if not selected else const.GOLD
    border_width = 2 if not selected else 3
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=10)
    
    return rect

def draw_title(screen, width, height, animation_timer):
    """Draw the animated title with glow effect"""
    try:
        font = pygame.font.SysFont("Arial", 60, bold=True)
    except:
        font = pygame.font.Font(None, 60)
        
    pulse = math.sin(animation_timer) * 5
    title_text = font.render("CHOOSE YOUR COLOR", True, const.GOLD)
    title_rect = title_text.get_rect(center=(width//2, height//6 + pulse))
    
    glow_size = 10 + int((abs(math.sin(animation_timer * 2)) * 8))
    glow_surf = pygame.Surface((title_rect.width + glow_size, title_rect.height + glow_size), pygame.SRCALPHA)
    pygame.draw.rect(glow_surf, (const.GOLD[0], const.GOLD[1], const.GOLD[2], 50), 
                     (0, 0, title_rect.width + glow_size, title_rect.height + glow_size), 
                     border_radius=20)
    screen.blit(glow_surf, (title_rect.x - glow_size//2, title_rect.y - glow_size//2))
    screen.blit(title_text, title_rect)

def draw_footer(screen, width, height):
    """Draw the footer text"""
    footer_font = pygame.font.SysFont("Arial", 16)
    footer_text = footer_font.render("White moves first. Choose wisely!", True, (200, 200, 200))
    footer_rect = footer_text.get_rect(bottom=height-10, centerx=width//2)
    screen.blit(footer_text, footer_rect)

def draw_back_button(screen, height):
    """Draw the back button with arrow icon"""
    try:
        font = pygame.font.SysFont("Arial", 36)
    except:
        font = pygame.font.Font(None, 36)
        
    button_rect = pygame.Rect(20, height - 70, 120, 50)
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    back_color = (180, 0, 0) if hover else (120, 0, 0)
    
    # Create gradient
    gradient = pygame.Surface((120, 50))
    for i in range(50):
        intensity = 1 - (i / 50) * 0.3
        color = (
            int(back_color[0] * intensity),
            int(back_color[1] * intensity),
            int(back_color[2] * intensity)
        )
        pygame.draw.line(gradient, color, (0, i), (120, i))
    screen.blit(gradient, button_rect)
    
    # Add border
    pygame.draw.rect(screen, const.WHITE, button_rect, 2, border_radius=10)
    
    # Arrow icon
    pygame.draw.polygon(screen, const.WHITE, [
        (button_rect.x + 20, button_rect.centery),
        (button_rect.x + 35, button_rect.y + 10),
        (button_rect.x + 35, button_rect.y + 40)
    ])
    
    back_text = font.render("Back", True, const.WHITE)
    back_text_rect = back_text.get_rect(center=(button_rect.centerx + 10, button_rect.centery))
    screen.blit(back_text, back_text_rect)
    
    return button_rect

def draw_color_option(screen, width, height, x, y, color, selected):
    """Draw a color selection option with preview board"""
    button_width = width // 3
    button_height = height // 3
    
    # Create button rectangle
    button_rect = pygame.Rect(x, y, button_width, button_height)
    
    # Check for mouse hover
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos) and not selected
    
    # Button color based on chess color
    button_color = (240, 240, 240) if color == "WHITE" else (70, 70, 70)
    create_gradient_button(screen, button_rect, button_color, hover, selected)
    
    # Determine text color based on button color
    text_color = const.BLACK if color == "WHITE" else const.WHITE
    
    # Draw button text
    try:
        font = pygame.font.SysFont("Arial", 36, bold=True)
        desc_font = pygame.font.SysFont("Arial", 18)
    except:
        font = pygame.font.Font(None, 36)
        desc_font = pygame.font.Font(None, 18)
        
    button_text = font.render(f"Play as {color.capitalize()}", True, text_color)
    button_text_rect = button_text.get_rect(centerx=button_rect.centerx, top=button_rect.top + 20)
    screen.blit(button_text, button_text_rect)
    
    # Draw description
    if color == "WHITE":
        desc_text = desc_font.render("Move first with advantage", True, text_color)
    else:
        desc_text = desc_font.render("Respond to AI's first move", True, text_color)
    
    desc_rect = desc_text.get_rect(centerx=button_rect.centerx, top=button_text_rect.bottom + 10)
    screen.blit(desc_text, desc_rect)
    
    # Draw board preview
    board_size = min(button_width, button_height) - 80
    board_x = button_rect.centerx - board_size // 2
    board_y = button_rect.bottom - board_size - 20
    draw_board_preview(screen, board_x, board_y, board_size, color)
    
    # Add checkmark if selected
    if selected:
        check_color = const.BLACK if color == "WHITE" else const.WHITE
        pygame.draw.circle(screen, check_color, (button_rect.right - 25, button_rect.top + 25), 15, 2)
        pygame.draw.line(screen, check_color, (button_rect.right - 33, button_rect.top + 25), 
                         (button_rect.right - 25, button_rect.top + 33), 3)
        pygame.draw.line(screen, check_color, (button_rect.right - 25, button_rect.top + 33), 
                         (button_rect.right - 15, button_rect.top + 15), 3)
    
    return button_rect

def draw_continue_button(screen, width, height, selection_made):
    """Draw continue button that appears once selection is made"""
    try:
        font = pygame.font.SysFont("Arial", 32, bold=True)
    except:
        font = pygame.font.Font(None, 32)
        
    button_width = 200
    button_height = 60
    button_rect = pygame.Rect(width//2 - button_width//2, height - 100, button_width, button_height)
    
    if not selection_made:
        # Draw disabled button
        disabled_color = (100, 100, 100)
        gradient = pygame.Surface((button_width, button_height))
        for i in range(button_height):
            intensity = 1 - (i / button_height) * 0.3
            color = (
                int(disabled_color[0] * intensity),
                int(disabled_color[1] * intensity),
                int(disabled_color[2] * intensity)
            )
            pygame.draw.line(gradient, color, (0, i), (button_width, i))
        screen.blit(gradient, button_rect)
        pygame.draw.rect(screen, (150, 150, 150), button_rect, 2, border_radius=10)
        
        button_text = font.render("Continue", True, (170, 170, 170))
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        
        return button_rect, False
    else:
        # Draw active button
        mouse_pos = pygame.mouse.get_pos()
        hover = button_rect.collidepoint(mouse_pos)
        button_color = const.BRIGHT_GREEN if hover else const.GREEN
        
        gradient = pygame.Surface((button_width, button_height))
        for i in range(button_height):
            intensity = 1 - (i / button_height) * 0.3
            color = (
                int(button_color[0] * intensity),
                int(button_color[1] * intensity),
                int(button_color[2] * intensity)
            )
            pygame.draw.line(gradient, color, (0, i), (button_width, i))
        screen.blit(gradient, button_rect)
        pygame.draw.rect(screen, const.WHITE, button_rect, 2, border_radius=10)
        
        button_text = font.render("Continue", True, const.WHITE)
        text_rect = button_text.get_rect(center=button_rect.center)
        screen.blit(button_text, text_rect)
        
        return button_rect, hover

def create_color_selection_screen(screen, width, height):
    """Create the color selection screen and handle user input"""
    # Initialize variables
    running = True
    animation_timer = 0
    clock = pygame.time.Clock()
    selected_color = None  # None = no selection, "WHITE" or "BLACK"
    
    # Background elements
    chess_pattern = []
    for _ in range(20):  # Create some floating chess patterns
        pattern = {
            'x': random.randint(0, width),
            'y': random.randint(0, height),
            'size': random.randint(30, 80),
            'rotation': random.uniform(0, 360),
            'rot_speed': random.uniform(-1, 1),
            'drift_x': random.uniform(-0.5, 0.5),
            'drift_y': random.uniform(-0.5, 0.5)
        }
        chess_pattern.append(pattern)
    
    while running:
        # Update animation
        animation_timer += 0.03
        
        # Update floating patterns
        for pattern in chess_pattern:
            pattern['rotation'] += pattern['rot_speed']
            pattern['x'] += pattern['drift_x']
            pattern['y'] += pattern['drift_y']
            
            # Wrap around screen
            if pattern['x'] < -pattern['size']: pattern['x'] = width + pattern['size']
            if pattern['x'] > width + pattern['size']: pattern['x'] = -pattern['size']
            if pattern['y'] < -pattern['size']: pattern['y'] = height + pattern['size']
            if pattern['y'] > height + pattern['size']: pattern['y'] = -pattern['size']
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if white option clicked
                if white_rect.collidepoint(mouse_pos):
                    selected_color = "WHITE"
                # Check if black option clicked
                elif black_rect.collidepoint(mouse_pos):
                    selected_color = "BLACK"
                # Check if back button clicked
                elif back_rect.collidepoint(mouse_pos):
                    return "BACK"
                # Check if continue button clicked
                elif continue_active and continue_rect.collidepoint(mouse_pos):
                    return selected_color
        
        # Draw background gradient
        for i in range(height):
            color = (0, 0, 40 + int(40 * i/height))
            pygame.draw.line(screen, color, (0, i), (width, i))
        
        # Draw floating chess patterns
        for pattern in chess_pattern:
            size = pattern['size']
            squares = 4  # 4x4 mini chess pattern
            square_size = size // squares
            for r in range(squares):
                for c in range(squares):
                    if (r + c) % 2 == 0:
                        # Calculate rotated position
                        angle = math.radians(pattern['rotation'])
                        center_x, center_y = pattern['x'], pattern['y']
                        offset_x = (c - squares/2 + 0.5) * square_size
                        offset_y = (r - squares/2 + 0.5) * square_size
                        
                        # Rotate point around center
                        x = center_x + offset_x * math.cos(angle) - offset_y * math.sin(angle)
                        y = center_y + offset_x * math.sin(angle) + offset_y * math.cos(angle)
                        
                        square_rect = pygame.Rect(
                            x - square_size/2, 
                            y - square_size/2, 
                            square_size, 
                            square_size
                        )
                        pygame.draw.rect(screen, (220, 220, 220, 30), square_rect)
        
        # Draw title
        draw_title(screen, width, height, animation_timer)
        
        # Calculate positions for options
        white_x = width//4 - width//6
        black_x = width*3//4 - width//6
        options_y = height//3
        
        # Draw color options
        white_rect = draw_color_option(
            screen, width, height, white_x, options_y, "WHITE", selected_color == "WHITE"
        )
        black_rect = draw_color_option(
            screen, width, height, black_x, options_y, "BLACK", selected_color == "BLACK"
        )
        
        # Draw back button
        back_rect = draw_back_button(screen, height)
        
        # Draw continue button (enabled only when color is selected)
        continue_rect, continue_active = draw_continue_button(screen, width, height, selected_color is not None)
        
        # Draw footer
        draw_footer(screen, width, height)
        
        pygame.display.flip()
        clock.tick(60)
    
    # Default return if the loop exits
    return "WHITE"