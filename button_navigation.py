# button_navigation.py
import pygame
from difficulty_screen import create_difficulty_screen

def create_button_gradient(width, height, color, hover=False, selected=False):
    """Create an enhanced gradient surface for the button background"""
    gradient = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Enhanced gradient with multiple layers
    for i in range(height):
        # Base gradient
        intensity = 1 - (i / height) * 0.4
        base_color = (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity)
        )
        
        # Add shine effect
        if i < height * 0.3:
            shine = int(30 * (1 - i / (height * 0.3)))
            base_color = (
                min(255, base_color[0] + shine),
                min(255, base_color[1] + shine),
                min(255, base_color[2] + shine)
            )
        
        # Add hover/selected effects
        if hover or selected:
            highlight = 30 if hover else 50
            base_color = (
                min(255, base_color[0] + highlight),
                min(255, base_color[1] + highlight),
                min(255, base_color[2] + highlight)
            )
        
        pygame.draw.line(gradient, base_color, (0, i), (width, i))
    
    return gradient

def draw_button_shadow(screen, x, y, width, height, hover=False):
    """Draw enhanced button shadow effect"""
    shadow_surface = pygame.Surface((width + 10, height + 10), pygame.SRCALPHA)
    
    # Multiple shadow layers for depth
    for i in range(3):
        alpha = 40 - i * 10
        offset = i * 2
        shadow_rect = pygame.Rect(offset + 2, offset + 2, width, height)
        pygame.draw.rect(shadow_surface, (0, 0, 0, alpha), shadow_rect, border_radius=10)
    
    screen.blit(shadow_surface, (x - 5, y - 5))

def draw_button_border(screen, x, y, width, height, hover=False, selected=False):
    """Draw enhanced button border with effects"""
    border_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Main border
    border_color = (255, 255, 255, 200) if not selected else (255, 215, 0, 255)
    border_width = 2 if not selected else 3
    
    # Draw outer glow if hovered or selected
    if hover or selected:
        for i in range(3):
            glow_alpha = 100 - i * 30
            glow_color = (255, 255, 255, glow_alpha)
            pygame.draw.rect(border_surface, glow_color, 
                           (i, i, width - i*2, height - i*2), 
                           border_radius=10)
    
    # Draw main border
    pygame.draw.rect(border_surface, border_color, 
                    (0, 0, width, height), 
                    border_width, border_radius=10)
    
    screen.blit(border_surface, (x, y))

def draw_button_text(screen, text, x, y, width, height, text_color, hover=False, selected=False):
    """Render and draw enhanced button text with effects"""
    try:
        font = pygame.font.SysFont("Arial", 24, bold=True)
    except pygame.error:
        font = pygame.font.Font(None, 28)
    
    # Create text with shadow
    shadow_offset = 2
    shadow_surface = font.render(text, True, (0, 0, 0, 150))
    text_surface = font.render(text, True, text_color)
    
    # Calculate text position
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    shadow_rect = shadow_surface.get_rect(center=(text_rect.centerx + shadow_offset, text_rect.centery + shadow_offset))
    
    # Draw text with effects
    if hover or selected:
        # Add text glow
        glow_surface = pygame.Surface((text_rect.width + 10, text_rect.height + 10), pygame.SRCALPHA)
        glow_color = (255, 255, 255, 100) if hover else (255, 215, 0, 150)
        pygame.draw.rect(glow_surface, glow_color, 
                        (0, 0, text_rect.width + 10, text_rect.height + 10),
                        border_radius=5)
        screen.blit(glow_surface, (text_rect.x - 5, text_rect.y - 5))
    
    # Draw shadow and text
    screen.blit(shadow_surface, shadow_rect)
    screen.blit(text_surface, text_rect)

def draw_click_effect(screen, x, y, width, height):
    """Enhanced visual feedback for button click"""
    click_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Create ripple effect
    for i in range(3):
        alpha = 150 - i * 40
        size = width + i * 10
        offset = i * 5
        pygame.draw.rect(click_surface, (255, 255, 255, alpha),
                        (offset, offset, size - offset*2, height - offset*2),
                        border_radius=10)
    
    screen.blit(click_surface, (x, y))
    pygame.display.flip()
    pygame.time.delay(100)

def create_button(screen, text, x, y, width, height, color, hover_color, text_color, action=None):
    """Creates and draws a modern, styled button with enhanced effects"""
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    is_hovering = button_rect.collidepoint(mouse_pos)
    
    # Draw enhanced button components
    draw_button_shadow(screen, x, y, width, height, is_hovering)
    
    # Create and draw gradient background
    current_color = hover_color if is_hovering else color
    gradient = create_button_gradient(width, height, current_color, is_hovering)
    screen.blit(gradient, button_rect)
    
    # Draw enhanced border
    draw_button_border(screen, x, y, width, height, is_hovering)
    
    # Draw enhanced text
    draw_button_text(screen, text, x, y, width, height, text_color, is_hovering)
    
    # Handle button click with enhanced effect
    if is_hovering and mouse_buttons[0] == 1 and action is not None:
        draw_click_effect(screen, x, y, width, height)
        return action
    
    return None

def handle_difficulty_navigation(result):
    """Process the result from difficulty selection"""
    if result is None:
        return None  # Return to main menu
    return result  # Return (difficulty, opponent) tuple

def select_difficulty_with_navigation(screen, width, height):
    """Handles the difficulty selection screen and navigation"""
    result = create_difficulty_screen(screen, width, height)
    return handle_difficulty_navigation(result)