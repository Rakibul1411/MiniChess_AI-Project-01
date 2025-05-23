import pygame
import constants as const

def draw_title(screen, width, height, font, animation_timer=None, is_launch=False):
    """Draw the animated title with shadow effect (no subtitle)."""
    TITLE_TOP = int(height * 0.12)
    TITLE_HEIGHT = 60
    title_text = "MINI CHESS" if is_launch else "Select Difficulty"
    title_surf = font.render(title_text, True, const.GOLD)
    title_rect = title_surf.get_rect(center=(width//2, TITLE_TOP + TITLE_HEIGHT//2))
    shadow = font.render(title_text, True, (0,0,0))
    shadow_rect = shadow.get_rect(center=(width//2+2, TITLE_TOP + TITLE_HEIGHT//2+2))
    screen.blit(shadow, shadow_rect)
    screen.blit(title_surf, title_rect)
    return TITLE_TOP + TITLE_HEIGHT + 10  # Return position for subtitle if needed

def draw_modern_button(screen, rect, text, font, hover, assets=None, button_states=None, button_key=None, selected=False):
    """Draw a modern, centered button with clean style, hover, and selected effect."""
    # Button background with hover or selected effect
    if selected:
        bg_color = (255, 230, 120)  # Gold highlight for selected
        border_color = (255, 200, 40)
    elif hover:
        bg_color = (220, 220, 220)
        border_color = (181, 136, 99)
    else:
        bg_color = (30, 30, 30, 180)
        border_color = (181, 136, 99)
    pygame.draw.rect(screen, bg_color, rect, border_radius=32)
    # Glow effect for hover
    if hover:
        glow_surf = pygame.Surface((rect.width+16, rect.height+16), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (200, 200, 200, 120), (0, 0, rect.width, rect.height), border_radius=32)
        screen.blit(glow_surf, (rect.x, rect.y))
        if assets and button_states and button_key and assets['hover_sound']:
            if not button_states[button_key]['hover']:
                assets['hover_sound'].play()
            button_states[button_key]['hover'] = True
    else:
        if assets and button_states and button_key:
            button_states[button_key]['hover'] = False
    # Border
    border_width = 4 if selected else 1
    pygame.draw.rect(screen, border_color, rect, border_width, border_radius=32)
    # Button text
    text_color = (205, 127, 50) if not selected else (120, 80, 0)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return hover, rect

def draw_button_with_description(screen, width, height, font, desc_font, 
                                y_pos, text, color, description, button_states, button_key, assets, selected=False):
    """Draw a button with description text below it"""
    button_width = int(width * 0.3)
    button_height = 50
    
    button_rect = pygame.Rect(
        (width - button_width) // 2,
        y_pos,
        button_width,
        button_height
    )
    
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)
    
    # Draw button using common function
    hover, button_rect = draw_modern_button(
        screen, button_rect, text, font, hover, assets, button_states, button_key, selected=selected
    )
    
    # Description text
    desc_text = desc_font.render(description, True, const.WHITE)
    desc_rect = desc_text.get_rect(center=(width//2, button_rect.bottom + 15))
    screen.blit(desc_text, desc_rect)
    
    return button_rect

def draw_back_button(screen, height, font, button_states, assets):
    """Draw the back button with hover effect"""
    button_rect = pygame.Rect(20, height - 70, 120, 50)
    mouse_pos = pygame.mouse.get_pos()
    hover = button_rect.collidepoint(mouse_pos)

    hover, button_rect = draw_modern_button(
        screen, button_rect, "Back", font, hover, assets, button_states, 'back'
    )

    center_y = button_rect.centery # centery = button_rect.y + (button_rect.height / 2)

    start_x = button_rect.x + 15   
    tip_x   = button_rect.x + 30   
    arrow_points = [
        (start_x, center_y),             
        (tip_x,   center_y - 8.5),         
        (tip_x,   center_y + 8.5),         
    ]
    pygame.draw.polygon(screen, (205, 127, 50), arrow_points)

    return button_rect


def draw_launch_buttons(screen, assets, width, height, animation_counter, button_states):
    """Draw buttons for launch screen"""
    BUTTON_WIDTH = int(width * 0.3)
    BUTTON_HEIGHT = 50
    BUTTON_SPACING = 36
    BUTTON_AREA_TOP = int(height * 0.60)
    
    # Create button rectangles
    play_rect = pygame.Rect(
        (width - BUTTON_WIDTH) // 2,
        BUTTON_AREA_TOP,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    quit_rect = pygame.Rect(
        (width - BUTTON_WIDTH) // 2,
        BUTTON_AREA_TOP + BUTTON_HEIGHT + BUTTON_SPACING,
        BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    
    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()
    
    # Check hover states
    play_hover = play_rect.collidepoint(mouse_pos)
    quit_hover = quit_rect.collidepoint(mouse_pos)
    
    # Draw buttons using common function
    play_hover, play_button_rect = draw_modern_button(
        screen, play_rect, "Start Game", assets['button_font'],
        play_hover, assets, button_states, 'play'
    )
    
    quit_hover, quit_button_rect = draw_modern_button(
        screen, quit_rect, "Quit Game", assets['button_font'],
        quit_hover, assets, button_states, 'quit'
    )
    
    return play_button_rect, quit_button_rect 