# button_navigation.py
import pygame
from difficulty_screen import create_difficulty_screen

def create_button_gradient(width, height, color):
    """Create a gradient surface for the button background"""
    gradient = pygame.Surface((width, height))
    for i in range(height):
        intensity = 1 - (i / height) * 0.3
        grad_color = (
            int(color[0] * intensity),
            int(color[1] * intensity),
            int(color[2] * intensity)
        )
        pygame.draw.line(gradient, grad_color, (0, i), (width, i))
    return gradient

def draw_button_shadow(screen, x, y, width, height):
    """Draw the button shadow effect"""
    shadow_rect = pygame.Rect(x + 2, y + 2, width, height)
    pygame.draw.rect(screen, (0, 0, 0, 50), shadow_rect, border_radius=5)

def draw_button_border(screen, x, y, width, height):
    """Draw the button border"""
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (255, 255, 255, 200), button_rect, 2, border_radius=5)

def draw_button_text(screen, text, x, y, width, height, text_color):
    """Render and draw button text"""
    try:
        font = pygame.font.SysFont("Arial", 20, bold=True)
    except pygame.error:
        font = pygame.font.Font(None, 24)
    
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text_surface, text_rect)

def draw_click_effect(screen, x, y, width, height):
    """Visual feedback for button click"""
    click_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, (255, 255, 255, 50), click_rect, border_radius=5)
    pygame.display.flip()
    pygame.time.delay(100)

def create_button(screen, text, x, y, width, height, color, hover_color, text_color, action=None):
    """Creates and draws a styled button with rounded corners and shadow"""
    mouse_pos = pygame.mouse.get_pos()
    mouse_buttons = pygame.mouse.get_pressed()
    button_rect = pygame.Rect(x, y, width, height)
    is_hovering = button_rect.collidepoint(mouse_pos)

    # Draw button components
    draw_button_shadow(screen, x, y, width, height)
    
    current_color = hover_color if is_hovering else color
    gradient = create_button_gradient(width, height, current_color)
    screen.blit(gradient, button_rect)
    
    draw_button_border(screen, x, y, width, height)
    draw_button_text(screen, text, x, y, width, height, text_color)
    
    # Handle button click
    if is_hovering and mouse_buttons[0] == 1 and action is not None:
        draw_click_effect(screen, x, y, width, height)
        return action
    
    return None

def handle_difficulty_navigation(difficulty):
    """Process the result from difficulty selection"""
    if difficulty == "BACK_TO_PLAY":
        return None  # Return to main menu
    return difficulty

def select_difficulty_with_navigation(screen, width, height):
    """Handles the difficulty selection screen and navigation"""
    difficulty = create_difficulty_screen(screen, width, height)
    return handle_difficulty_navigation(difficulty)