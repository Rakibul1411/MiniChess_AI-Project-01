import pygame
import os
import sys
import math
import random
import constants as const
from launch_screen import create_launch_screen
from draw_title_button import draw_title, draw_button_with_description, draw_back_button

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
            'back': {'hover': False}
        }
        self.clock = pygame.time.Clock()
        self.button_rects = {
            'easy': None,
            'medium': None,
            'hard': None,
            'back': None
        }

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
            'fonts': {},
            'hover_sound': None,
            'click_sound': None
        }
        
        self.load_background_image(assets)
        self.load_chess_piece_images(assets)
        self.load_fonts(assets)
        self.load_sounds(assets)
        
        return assets

    def load_background_image(self, assets):
        """Load background image if available"""
        try:
            bg_image = pygame.image.load(os.path.join(self.assets_dir, 'difficulty.png'))
            assets['bg_image'] = pygame.transform.smoothscale(bg_image, (self.width, self.height))
        except:
            pass

    def load_chess_piece_images(self, assets):
        """Load chess piece images if available"""
        piece_types = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        piece_colors = ['white', 'black']
        
        try:
            for color in piece_colors:
                for piece_type in piece_types:
                    image_name = f"{color}_{piece_type}.png"
                    image_path = os.path.join(self.assets_dir, image_name)
                    if os.path.exists(image_path):
                        assets['piece_images'][f"{color}_{piece_type}"] = pygame.image.load(image_path)
                    else:
                        assets['piece_images'][f"{color}_{piece_type}"] = None
        except:
            pass

    def load_fonts(self, assets):
        """Load fonts or fall back to system fonts"""
        try:
            title_font_path = os.path.join(self.assets_dir, 'Bassy.ttf')
            button_font_path = os.path.join(self.assets_dir, 'Rosemary.ttf')
            desc_font_path = os.path.join(self.assets_dir, 'Handsean.ttf')
            
            if os.path.exists(title_font_path):
                assets['fonts']['title'] = pygame.font.Font(title_font_path, 60)
            else:
                assets['fonts']['title'] = pygame.font.SysFont("Times New Roman", 60, bold=True)
                
            if os.path.exists(button_font_path):
                assets['fonts']['button'] = pygame.font.Font(button_font_path, 25)
                assets['fonts']['back'] = pygame.font.Font(button_font_path, 25)
            else:
                assets['fonts']['button'] = pygame.font.SysFont("Georgia", 25, bold=True)
                assets['fonts']['back'] = pygame.font.SysFont("Georgia", 25)
                
            if os.path.exists(desc_font_path):
                assets['fonts']['desc'] = pygame.font.Font(desc_font_path, 20)
            else:
                assets['fonts']['desc'] = pygame.font.SysFont("Georgia", 20)
        except:
            assets['fonts']['title'] = pygame.font.SysFont("Times New Roman", 60, bold=True)
            assets['fonts']['button'] = pygame.font.SysFont("Georgia", 25, bold=True)
            assets['fonts']['back'] = pygame.font.SysFont("Georgia", 25)
            assets['fonts']['desc'] = pygame.font.SysFont("Georgia", 20)

    def load_sounds(self, assets):
        """Load sound effects if available"""
        try:
            pygame.mixer.init()
            assets['hover_sound'] = pygame.mixer.Sound(os.path.join(self.assets_dir, 'hover.mp3'))
            assets['click_sound'] = pygame.mixer.Sound(os.path.join(self.assets_dir, 'click.wav'))
        except:
            pass

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
            self.button_states, 'easy', self.assets
        )
        
        self.button_rects['medium'] = draw_button_with_description(
            self.screen, self.width, self.height, 
            self.assets['fonts']['button'], self.assets['fonts']['desc'],
            start_y + button_height + button_spacing, "Medium", const.SILVER,
            "For casual players - AI has moderate strategy",
            self.button_states, 'medium', self.assets
        )
        
        self.button_rects['hard'] = draw_button_with_description(
            self.screen, self.width, self.height, 
            self.assets['fonts']['button'], self.assets['fonts']['desc'],
            start_y + 2*(button_height + button_spacing), "Hard", const.GOLD,
            "For experts - AI uses advanced tactics",
            self.button_states, 'hard', self.assets
        )

    def handle_events(self):
        """Handle pygame events and return selected difficulty or None"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return self.handle_button_clicks(mouse_pos)
        
        return None

    def handle_button_clicks(self, mouse_pos):
        """Handle button click events and return appropriate action"""
        if self.button_rects['easy'] and self.button_rects['easy'].collidepoint(mouse_pos):
            self.play_click_sound()
            return "EASY"
        elif self.button_rects['medium'] and self.button_rects['medium'].collidepoint(mouse_pos):
            self.play_click_sound()
            return "MEDIUM"
        elif self.button_rects['hard'] and self.button_rects['hard'].collidepoint(mouse_pos):
            self.play_click_sound()
            return "HARD"
        elif self.button_rects['back'] and self.button_rects['back'].collidepoint(mouse_pos):
            self.play_click_sound()
            choice = create_launch_screen(self.screen, self.width, self.height)
            if choice == "PLAY":
                return self.run()  # Restart difficulty selection
            else:
                pygame.quit()
                sys.exit()
        return None

    def play_click_sound(self):
        """Play button click sound if available"""
        if self.assets['click_sound']:
            self.assets['click_sound'].play()

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
        while True:
            self.animation_timer += 0.03
            self.update_chess_pieces()
            
            result = self.handle_events()
            if result is not None:
                return result
            
            self.draw_background()
            self.draw_chess_pieces()
            self.draw_ui_elements()
            self.update_cursor()
            
            pygame.display.flip()
            self.clock.tick(120)

def create_difficulty_screen(screen, width, height):
    """Create and run the difficulty selection screen"""
    difficulty_screen = DifficultyScreen(screen, width, height)
    return difficulty_screen.run()