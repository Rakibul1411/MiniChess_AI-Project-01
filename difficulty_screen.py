import pygame
import os
import sys
import math
import random
import constants as const
from launch_screen import create_launch_screen
from draw_title_button import draw_title, draw_button_with_description, draw_back_button, draw_modern_button
import traceback

class DifficultyScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        self.assets = self.load_assets()
        self.animation_timer = 0
        self.chess_pieces = self.initialize_chess_pieces()
        self.button_states = {
            'easy': {'hover': False},
            'medium': {'hover': False},
            'hard': {'hover': False},
            'back': {'hover': False},
            'reset': {'hover': False},
            'opponent_ai': {'hover': False},
            'opponent_human': {'hover': False}
        }
        self.clock = pygame.time.Clock()
        self.button_rects = {
            'easy': None,
            'medium': None,
            'hard': None,
            'back': None,
            'opponent_ai': None,
            'opponent_human': None,
            'reset': None
        }
        self.selected_difficulty = None
        self.selected_opponent = None

    def initialize_chess_pieces(self, count=15):
        """Initialize falling chess pieces with random properties"""
        piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        piece_colors = ['white', 'black']
        
        chess_pieces = []
        for _ in range(count):
            piece = {
                'x': random.randint(0, self.width),
                'y': random.randint(-500, -50),
                'speed': random.uniform(1, 3),
                'rotation': random.randint(0, 360),
                'rot_speed': random.uniform(-2, 2),
                'size': random.randint(30, 50),
                'type': random.choice(piece_types),
                'color': random.choice(piece_colors)
            }
            chess_pieces.append(piece)
        return chess_pieces

    def update_chess_pieces(self):
        """Update positions of falling chess pieces"""
        for piece in self.chess_pieces:
            piece['y'] += piece['speed']
            piece['rotation'] += piece['rot_speed']
            
            if piece['y'] > self.height + 50:
                piece['y'] = random.randint(-200, -50)
                piece['x'] = random.randint(0, self.width)
                piece['speed'] = random.uniform(1, 3)
                piece['type'] = random.choice(['pawn', 'knight', 'bishop', 'rook', 'queen', 'king'])
                piece['color'] = random.choice(['white', 'black'])

    def load_assets(self):
        """Load all game assets (images, fonts, sounds)"""
        assets = {
            'bg_image': None,
            'piece_images': {},
            'fonts': {
                'title': pygame.font.SysFont("Times New Roman", 60, bold=True),
                'button': pygame.font.SysFont("Georgia", 25, bold=True),
                'back': pygame.font.SysFont("Georgia", 25),
                'desc': pygame.font.SysFont("Georgia", 20)
            },
            'hover_sound': None,
            'click_sound': None
        }
        
        try:
            self.load_background_image(assets)
            self.load_chess_piece_images(assets)
            self.load_fonts(assets)
            self.load_sounds(assets)
        except Exception as e:
            print(f"Error loading assets: {e}")
            traceback.print_exc()
        
        return assets

    def load_background_image(self, assets):
        """Load background image if available"""
        try:
            bg_image = pygame.image.load(os.path.join(self.assets_dir, 'difficulty.png'))
            assets['bg_image'] = pygame.transform.smoothscale(bg_image, (self.width, self.height))
        except Exception as e:
            print(f"Failed to load background image: {e}")
            assets['bg_image'] = None

    def load_chess_piece_images(self, assets):
        """Load chess piece images if available"""
        piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        piece_colors = ['white', 'black']
        
        for color in piece_colors:
            for piece_type in piece_types:
                image_name = f"{color}_{piece_type}.png"
                image_path = os.path.join(self.assets_dir, image_name)
                try:
                    if os.path.exists(image_path):
                        assets['piece_images'][f"{color}_{piece_type}"] = pygame.image.load(image_path)
                    else:
                        assets['piece_images'][f"{color}_{piece_type}"] = None
                except Exception as e:
                    print(f"Failed to load {image_name}: {e}")
                    assets['piece_images'][f"{color}_{piece_type}"] = None

    def load_fonts(self, assets):
        """Load fonts or fall back to system fonts"""
        try:
            title_font_path = os.path.join(self.assets_dir, 'Bassy.ttf')
            button_font_path = os.path.join(self.assets_dir, 'Rosemary.ttf')
            desc_font_path = os.path.join(self.assets_dir, 'Handsean.ttf')
            
            assets['fonts']['title'] = pygame.font.Font(title_font_path, 60) if os.path.exists(title_font_path) else \
                                      pygame.font.SysFont("Times New Roman", 60, bold=True)
            assets['fonts']['button'] = pygame.font.Font(button_font_path, 25) if os.path.exists(button_font_path) else \
                                       pygame.font.SysFont("Georgia", 25, bold=True)
            assets['fonts']['back'] = pygame.font.Font(button_font_path, 25) if os.path.exists(button_font_path) else \
                                     pygame.font.SysFont("Georgia", 25)
            assets['fonts']['desc'] = pygame.font.Font(desc_font_path, 20) if os.path.exists(desc_font_path) else \
                                     pygame.font.SysFont("Georgia", 20)
        except Exception as e:
            print(f"Failed to load fonts: {e}")

    def load_sounds(self, assets):
        """Load sound effects if available"""
        try:
            pygame.mixer.init()
            hover_path = os.path.join(self.assets_dir, 'hover.mp3')
            click_path = os.path.join(self.assets_dir, 'click.wav')
            assets['hover_sound'] = pygame.mixer.Sound(hover_path) if os.path.exists(hover_path) else None
            assets['click_sound'] = pygame.mixer.Sound(click_path) if os.path.exists(click_path) else None
        except Exception as e:
            print(f"Failed to load sounds: {e}")

    def draw_chess_piece(self, piece):
        """Draw a single chess piece with rotation"""
        piece_key = f"{piece['color']}_{piece['type']}"
        if piece_key in self.assets['piece_images'] and self.assets['piece_images'][piece_key]:
            img = self.assets['piece_images'][piece_key]
            img = pygame.transform.scale(img, (piece['size'], piece['size']))
            img = pygame.transform.rotate(img, piece['rotation'])
            img_rect = img.get_rect(center=(piece['x'], piece['y']))
            self.screen.blit(img, img_rect.topleft)
        else:
            self.draw_fallback_chess_piece(piece)

    def draw_fallback_chess_piece(self, piece):
        """Draw a simple representation of a chess piece when images aren't available"""
        piece_color = const.WHITE if piece['color'] == 'white' else const.BLACK
        piece_border = const.BLACK if piece['color'] == 'white' else const.WHITE
        
        if piece['type'] == 'pawn':
            pygame.draw.circle(self.screen, piece_color, (int(piece['x']), int(piece['y'])), piece['size']//2)
            pygame.draw.circle(self.screen, piece_border, (int(piece['x']), int(piece['y'])), piece['size']//2, 2)
        elif piece['type'] == 'knight':
            points = []
            for i in range(5):
                angle = math.radians(piece['rotation'] + i * 72)
                points.append((
                    piece['x'] + piece['size']//2 * math.cos(angle),
                    piece['y'] + piece['size']//2 * math.sin(angle)
                ))
            pygame.draw.polygon(self.screen, piece_color, points)
            pygame.draw.polygon(self.screen, piece_border, points, 2)
        else:
            rect = pygame.Rect(0, 0, piece['size'], piece['size'])
            rect.center = (piece['x'], piece['y'])
            pygame.draw.rect(self.screen, piece_color, rect, border_radius=8)
            pygame.draw.rect(self.screen, piece_border, rect, 2, border_radius=8)

    def draw_background(self):
        """Draw the background image or gradient fallback"""
        if self.assets['bg_image']:
            self.screen.blit(self.assets['bg_image'], (0, 0))
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            self.screen.blit(overlay, (0, 0))
        else:
            for i in range(self.height):
                color = (0, 0, 50 + int(50 * i/self.height))
                pygame.draw.line(self.screen, color, (0, i), (self.width, i))

    def draw_chess_pieces(self):
        """Draw all falling chess pieces"""
        for piece in self.chess_pieces:
            self.draw_chess_piece(piece)

    def draw_ui_elements(self):
        """Draw all UI elements (title, buttons)"""
        draw_title(self.screen, self.width, self.height, self.assets['fonts']['title'], self.animation_timer)
        self.draw_difficulty_buttons()
        self.button_rects['back'] = draw_back_button(
            self.screen, self.height, self.assets['fonts']['back'], self.button_states, self.assets
        )

    def draw_difficulty_buttons(self):
        """Draw the difficulty selection buttons"""
        button_spacing = 50
        button_height = 70
        start_y = self.height * 2 // 5
        
        self.button_rects['easy'] = draw_button_with_description(
            self.screen, self.width, self.height, 
            self.assets['fonts']['button'], self.assets['fonts']['desc'],
            start_y, "Easy", const.BRONZE, 
            "For beginners - AI makes basic moves",
            self.button_states, 'easy', self.assets,
            selected=(self.selected_difficulty == "EASY")
        )
        
        self.button_rects['medium'] = draw_button_with_description(
            self.screen, self.width, self.height, 
            self.assets['fonts']['button'], self.assets['fonts']['desc'],
            start_y + button_height + button_spacing, "Medium", const.SILVER,
            "For casual players - AI has moderate strategy",
            self.button_states, 'medium', self.assets,
            selected=(self.selected_difficulty == "MEDIUM")
        )
        
        self.button_rects['hard'] = draw_button_with_description(
            self.screen, self.width, self.height, 
            self.assets['fonts']['button'], self.assets['fonts']['desc'],
            start_y + 2*(button_height + button_spacing), "Hard", const.GOLD,
            "For experts - AI uses advanced tactics",
            self.button_states, 'hard', self.assets,
            selected=(self.selected_difficulty == "HARD")
        )

        # Draw 'Opponent' label below Hard
        opponent_label_y = start_y + 3*(button_height + button_spacing)
        label_font = self.assets['fonts']['button']
        label_text = label_font.render("Opponent", True, const.ROYAL_BLUE)
        label_rect = label_text.get_rect(center=(self.width//2, opponent_label_y + 25))
        self.screen.blit(label_text, label_rect)

        # Draw AI and Human buttons horizontally below the label
        ai_human_y = opponent_label_y + 60
        button_width = int(self.width * 0.18)
        button_height = 50
        gap = 30
        total_width = button_width * 2 + gap
        start_x = (self.width - total_width) // 2
        ai_rect = pygame.Rect(start_x, ai_human_y, button_width, button_height)
        human_rect = pygame.Rect(start_x + button_width + gap, ai_human_y, button_width, button_height)
        mouse_pos = pygame.mouse.get_pos()
        ai_hover = ai_rect.collidepoint(mouse_pos)
        human_hover = human_rect.collidepoint(mouse_pos)
        
        # Draw AI and Human buttons, enabled only if a difficulty is selected for AI
        if self.selected_difficulty or self.selected_opponent == "OPPONENT_HUMAN":
            _, self.button_rects['opponent_ai'] = draw_modern_button(
                self.screen, ai_rect, "AI", self.assets['fonts']['button'], ai_hover,
                self.assets, self.button_states, 'opponent_ai',
                selected=(self.selected_opponent == "OPPONENT_AI")
            )
            _, self.button_rects['opponent_human'] = draw_modern_button(
                self.screen, human_rect, "Human", self.assets['fonts']['button'], human_hover,
                self.assets, self.button_states, 'opponent_human',
                selected=(self.selected_opponent == "OPPONENT_HUMAN")
            )
        else:
            # Draw disabled buttons
            disabled_color = (180, 180, 180)
            pygame.draw.rect(self.screen, disabled_color, ai_rect, border_radius=12)
            ai_text = self.assets['fonts']['button'].render("AI", True, (120,120,120))
            ai_text_rect = ai_text.get_rect(center=ai_rect.center)
            self.screen.blit(ai_text, ai_text_rect)
            self.button_rects['opponent_ai'] = None

            pygame.draw.rect(self.screen, disabled_color, human_rect, border_radius=12)
            human_text = self.assets['fonts']['button'].render("Human", True, (120,120,120))
            human_text_rect = human_text.get_rect(center=human_rect.center)
            self.screen.blit(human_text, human_text_rect)
            self.button_rects['opponent_human'] = None

        # Draw Reset button at the bottom right
        reset_width, reset_height = 120, 50
        reset_x = self.width - reset_width - 30
        reset_y = self.height - reset_height - 30
        reset_rect = pygame.Rect(reset_x, reset_y, reset_width, reset_height)
        reset_hover = reset_rect.collidepoint(mouse_pos)
        _, self.button_rects['reset'] = draw_modern_button(
            self.screen, reset_rect, "Reset", self.assets['fonts']['button'], reset_hover,
            self.assets, self.button_states, 'reset'
        )

    def handle_events(self):
        """Handle pygame events and return selected difficulty or None"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                try:
                    return self.handle_button_clicks(mouse_pos)
                except Exception as e:
                    print(f"Error handling button click: {e}")
                    traceback.print_exc()
                    return None
        
        return None

    def handle_button_clicks(self, mouse_pos):
        """Handle button click events and return appropriate action"""
        if self.button_rects['easy'] and self.button_rects['easy'].collidepoint(mouse_pos):
            self.play_click_sound()
            self.selected_difficulty = "EASY"
            if self.selected_opponent == "OPPONENT_HUMAN":
                self.selected_opponent = None  # Reset opponent if switching to AI-compatible difficulty
            return None
        elif self.button_rects['medium'] and self.button_rects['medium'].collidepoint(mouse_pos):
            self.play_click_sound()
            self.selected_difficulty = "MEDIUM"
            if self.selected_opponent == "OPPONENT_HUMAN":
                self.selected_opponent = None
            return None
        elif self.button_rects['hard'] and self.button_rects['hard'].collidepoint(mouse_pos):
            self.play_click_sound()
            self.selected_difficulty = "HARD"
            if self.selected_opponent == "OPPONENT_HUMAN":
                self.selected_opponent = None
            return None
        elif self.button_rects['opponent_ai'] and self.button_rects['opponent_ai'].collidepoint(mouse_pos) and self.selected_difficulty:
            self.play_click_sound()
            self.selected_opponent = "OPPONENT_AI"
            return (self.selected_difficulty, self.selected_opponent)
        elif self.button_rects['opponent_human'] and self.button_rects['opponent_human'].collidepoint(mouse_pos):
            self.play_click_sound()
            self.selected_difficulty = None  # No difficulty needed for human vs human
            self.selected_opponent = "OPPONENT_HUMAN"
            return (self.selected_difficulty, self.selected_opponent)
        elif self.button_rects['back'] and self.button_rects['back'].collidepoint(mouse_pos):
            self.play_click_sound()
            try:
                choice = create_launch_screen(self.screen, self.width, self.height)
                if choice == "PLAY":
                    return None  # Restart difficulty selection
                else:
                    pygame.quit()
                    sys.exit()
            except Exception as e:
                print(f"Error navigating back: {e}")
                traceback.print_exc()
                return None
        elif self.button_rects['reset'] and self.button_rects['reset'].collidepoint(mouse_pos):
            self.play_click_sound()
            self.selected_difficulty = None
            self.selected_opponent = None
            return None
        return None

    def play_click_sound(self):
        """Play button click sound if available"""
        try:
            if self.assets['click_sound']:
                self.assets['click_sound'].play()
        except Exception as e:
            print(f"Error playing click sound: {e}")

    def update_cursor(self):
        """Update mouse cursor based on hover state"""
        mouse_pos = pygame.mouse.get_pos()
        any_hover = any(
            rect and rect.collidepoint(mouse_pos) 
            for rect in self.button_rects.values()
        )
        
        if any_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def run(self):
        """Main loop for difficulty screen"""
        self.selected_difficulty = None
        self.selected_opponent = None
        while True:
            try:
                self.animation_timer += 0.03
                self.update_chess_pieces()
                result = self.handle_events()
                if result:
                    return result
                self.draw_background()
                self.draw_chess_pieces()
                self.draw_ui_elements()
                self.update_cursor()
                pygame.display.flip()
                self.clock.tick(120)
            except Exception as e:
                print(f"Error in DifficultyScreen.run: {e}")
                traceback.print_exc()
                pygame.quit()
                sys.exit()

def create_difficulty_screen(screen, width, height):
    """Create and run the difficulty selection screen"""
    try:
        difficulty_screen = DifficultyScreen(screen, width, height)
        return difficulty_screen.run()
    except Exception as e:
        print(f"Error creating difficulty screen: {e}")
        traceback.print_exc()
        pygame.quit()
        sys.exit()