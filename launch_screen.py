import pygame
import os
import sys
import math
import random
import constants as const
from draw_title_button import draw_title, draw_launch_buttons

class LaunchScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
        self.assets = self.load_assets()
        self.animation_counter = 0
        self.particles = self.create_particles()
        self.chess_pieces = self.create_chess_pieces()
        self.button_states = {
            'play': {'hover': False, 'played_sound': False},
            'quit': {'hover': False, 'played_sound': False}
        }
        self.clock = pygame.time.Clock()
        self.play_button_rect = None
        self.quit_button_rect = None
        # self.pygame.mouse.set_visible(True)


    def load_assets(self):
        """Load all game assets (images, fonts, sounds)"""
        assets = {
            'title_image': None,
            'piece_images': [],
            'title_font': None,
            'button_font': None,
            'small_font': None,
            'hover_sound': None,
            'click_sound': None,
            'ambient_sound': None
        }
        
        try:
            assets.update(self.load_images())
            assets.update(self.load_fonts())
            assets.update(self.load_sounds())
            if assets['ambient_sound']:
                assets['ambient_sound'].play(0)  # Loop ambient sound
        except Exception as e:
            print(f"Error loading assets: {e}")
            assets.update(self.get_fallback_fonts())
        
        return assets

    def load_images(self):
        """Load all image assets"""
        images = {
            'title_image': None,
            'piece_images': []
        }
        
        # Load title image
        try:
            title_img = pygame.image.load(os.path.join(self.assets_dir, 'title.png'))
            images['title_image'] = pygame.transform.smoothscale(title_img, (self.width, self.height))
        except:
            pass
            
        # Load chess piece images
        piece_files = [
            'white_knight.png', 'white_queen.png', 'black_king.png', 
            'black_rook.png', 'white_pawn.png', 'white_bishop.png', 
            'black_queen.png', 'black_bishop.png'
        ]
        
        for file in piece_files:
            try:
                img = pygame.image.load(os.path.join(self.assets_dir, file))
                img = pygame.transform.smoothscale(img, (self.width//10, self.width//10))
                images['piece_images'].append(img)
            except:
                pass
                
        return images

    def load_fonts(self):
        """Load all font assets"""
        fonts = {}
        try:
            title_font_path = os.path.join(self.assets_dir, 'Bassy.ttf')
            button_font_path = os.path.join(self.assets_dir, 'Rosemary.ttf')
            subtitle_font_path = os.path.join(self.assets_dir, 'handsean.ttf')
            
            fonts['title_font'] = pygame.font.Font(title_font_path, 60) if os.path.exists(title_font_path) else \
                                  pygame.font.SysFont("Times New Roman", 60, bold=True)
            fonts['button_font'] = pygame.font.Font(button_font_path, 25) if os.path.exists(button_font_path) else \
                pygame.font.SysFont("Georgia", 25, bold=True)
            fonts['small_font'] = pygame.font.Font(subtitle_font_path, 21) if os.path.exists(subtitle_font_path) else \
                pygame.font.SysFont("Arial", 21)
        except:
            fonts.update(self.get_fallback_fonts())
            
        return fonts

    def get_fallback_fonts(self):
        """Return fallback fonts when loading fails"""
        return {
            'title_font': pygame.font.SysFont("Times New Roman", 60, bold=True),
            'button_font': pygame.font.SysFont("Georgia", 25, bold=True),
            'small_font': pygame.font.SysFont("Arial", 21)
        }

    def load_sounds(self):
        """Load all sound assets"""
        sounds = {}
        try:
            pygame.mixer.init()
            sounds['hover_sound'] = pygame.mixer.Sound(os.path.join(self.assets_dir, 'hover.mp3'))
            sounds['click_sound'] = pygame.mixer.Sound(os.path.join(self.assets_dir, 'click.wav'))
            sounds['ambient_sound'] = pygame.mixer.Sound(os.path.join(self.assets_dir, 'ambient.mp3'))
        except:
            pass
        return sounds

    def create_chess_pieces(self, count=6):
        """Create animated chess pieces for background"""
        pieces = []
        for _ in range(count):
            if self.assets['piece_images']:
                img = random.choice(self.assets['piece_images'])
                pieces.append({
                    'img': img,
                    'x': random.randint(0, self.width),
                    'y': random.randint(-self.height, 0),
                    'speed': random.uniform(0.5, 2.0),
                    'rotation': 0,
                    'rot_speed': random.uniform(-1, 1)
                })
        return pieces

    def create_particles(self, count=100):
        """Create particle system for background effects"""
        particles = []
        for _ in range(count):
            particles.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'size': random.randint(2, 6),
                'color': random.choice([const.GOLD, const.ROYAL_BLUE, (255, 255, 255)]),
                'speed': random.uniform(0.2, 1.0)
            })
        return particles

    def update_animations(self):
        """Update all animation states"""
        self.animation_counter += 0.03
        self.update_chess_pieces()
        self.update_particles()

    def update_chess_pieces(self):
        """Update positions of animated chess pieces"""
        for piece in self.chess_pieces:
            piece['y'] += piece['speed']
            piece['rotation'] += piece['rot_speed']
            if piece['y'] > self.height:
                piece['y'] = random.randint(-self.height//2, 0)
                piece['x'] = random.randint(0, self.width)

    def update_particles(self):
        """Update positions of background particles"""
        for particle in self.particles:
            particle['y'] += particle['speed']
            if particle['y'] > self.height:
                particle['y'] = 0
                particle['x'] = random.randint(0, self.width)

    def draw_background(self):
        """Draw the appropriate background (image or chess pattern)"""
        if self.assets['title_image']:
            self.draw_image_background()
        else:
            self.draw_chess_background()
        
        # Apply overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180 if not self.assets['title_image'] else 100))
        self.screen.blit(overlay, (0, 0))

    def draw_image_background(self):
        """Draw the title image background with subtle animation"""
        offset_x = math.sin(self.animation_counter * 0.5) * 20
        offset_y = math.cos(self.animation_counter * 0.3) * 20
        self.screen.blit(self.assets['title_image'], (offset_x, offset_y))

    def draw_chess_background(self):
        """Draw an animated chess pattern background"""
        square_size = self.width // 12
        for row in range(self.height // square_size + 1):
            for col in range(self.width // square_size + 1):
                color_offset = int(20 * math.sin(self.animation_counter + (row + col) * 0.2))
                if (row + col) % 2 == 0:
                    color = (min(255, 240 + color_offset), 
                            min(255, 217 + color_offset), 
                            min(255, 181 + color_offset))
                else:
                    color = (max(0, 181 - color_offset), 
                            max(0, 136 - color_offset), 
                            max(0, 99 - color_offset))
                
                pygame.draw.rect(self.screen, color, 
                                (col * square_size, row * square_size, square_size, square_size))

    def draw_animated_elements(self):
        """Draw all animated elements (chess pieces and particles)"""
        self.draw_chess_pieces()
        self.draw_particles()

    def draw_chess_pieces(self):
        """Draw the animated chess pieces"""
        for piece in self.chess_pieces:
            if piece['img']:
                rotated = pygame.transform.rotate(piece['img'], piece['rotation'])
                rot_rect = rotated.get_rect(center=(piece['x'], piece['y']))
                self.screen.blit(rotated, rot_rect)

    def draw_particles(self):
        """Draw the background particles"""
        for particle in self.particles:
            size_variation = math.sin(self.animation_counter * 2 + particle['x']) * 2
            pygame.draw.circle(self.screen, particle['color'], 
                             (int(particle['x']), int(particle['y'])), 
                             int(particle['size'] + size_variation))

    def draw_ui_elements(self):
        """Draw all UI elements (title, subtitle, divider, buttons)"""
        title_bottom = draw_title(self.screen, self.width, self.height, 
                                self.assets['title_font'], is_launch=True)
        
        subtitle_bottom = self.draw_subtitle(title_bottom)
        divider_y = subtitle_bottom + 10
        self.draw_divider(divider_y)
        
        self.play_button_rect, self.quit_button_rect = draw_launch_buttons(
            self.screen, self.assets, self.width, self.height, 
            self.animation_counter, self.button_states
        )

    def draw_subtitle(self, title_bottom):
        """Draw the subtitle text"""
        subtitle = "A Battle of Wits & Strategy"
        subtitle_text = self.assets['small_font'].render(subtitle, True, const.WHITE)
        subtitle_rect = subtitle_text.get_rect(midtop=(self.width//2, title_bottom + 20))
        self.screen.blit(subtitle_text, subtitle_rect)
        return subtitle_rect.bottom

    def draw_divider(self, y_pos):
        """Draw the decorative divider line"""
        pygame.draw.line(self.screen, const.GOLD, (self.width//4, y_pos), (self.width*3//4, y_pos), 2)
        for x_pos in [self.width//4, self.width//2, self.width*3//4]:
            pygame.draw.circle(self.screen, const.GOLD, (x_pos, y_pos), 8)
            pygame.draw.circle(self.screen, const.BLACK, (x_pos, y_pos), 4)

    def handle_events(self):
        """Handle all pygame events and return user choice"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return self.handle_button_clicks(mouse_pos)
        
        self.update_cursor(mouse_pos)
        return None

    def handle_button_clicks(self, mouse_pos):
        """Handle button click events"""
        if self.play_button_rect and self.play_button_rect.collidepoint(mouse_pos):
            self.play_click_sound()
            return "PLAY"
        elif self.quit_button_rect and self.quit_button_rect.collidepoint(mouse_pos):
            self.play_click_sound()
            pygame.quit()
            sys.exit()
        return None

    def play_click_sound(self):
        """Play the button click sound if available"""
        if self.assets['click_sound']:
            self.assets['click_sound'].play()

    def update_cursor(self, mouse_pos):
        """Update mouse cursor based on hover state"""
        any_hover = (
            (self.play_button_rect and self.play_button_rect.collidepoint(mouse_pos)) or
            (self.quit_button_rect and self.quit_button_rect.collidepoint(mouse_pos))
        )
        
        if any_hover:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def run(self):
        """Main loop for the launch screen"""
        while True:
            self.update_animations()
            self.draw_background()
            
            self.draw_animated_elements()
            self.draw_ui_elements()
            
            result = self.handle_events()
            if result is not None:
                return result
            
            pygame.display.flip()
            self.clock.tick(120)

def create_launch_screen(screen, width, height):
    """Create and run the launch screen"""
    launch_screen = LaunchScreen(screen, width, height)
    return launch_screen.run()