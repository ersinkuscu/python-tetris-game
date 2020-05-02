import pygame as game
from tetris_game.components import Shape
from tetris_game.colors import RED, GREEN, WHITE, BLACK, BLUE
import numpy as np

# game initials
TETRIS_EDGE_LINEWIDTH = 2
TETRIS_GRID_LINEWIDTH = 1
TETRIS_BOX_SIZE = 10
TETRIS_BLOCK_SIZE = TETRIS_BOX_SIZE + TETRIS_GRID_LINEWIDTH
TETRIS_DISPLAY_WIDTH = (200 // TETRIS_BLOCK_SIZE) * TETRIS_BLOCK_SIZE + 2 * TETRIS_GRID_LINEWIDTH
TETRIS_DISPLAY_HEIGHT = (400 // TETRIS_BLOCK_SIZE) * TETRIS_BLOCK_SIZE + 2 * TETRIS_GRID_LINEWIDTH
TETRIS_TIME_COUNTER = 250
TETRIS_KEY_COUNTER = 60

GAME_DISPLAY_WIDTH = 400
GAME_DISPLAY_HEIGHT = TETRIS_DISPLAY_HEIGHT + TETRIS_EDGE_LINEWIDTH
GAME_LINEWIDTH = 2
GAME_TIME_STEP = 1


class Game:
    def __init__(self):
        game.init()
        game.display.set_caption('Tetris Game')
        game.key.set_repeat()
        self.screen = game.display.set_mode((GAME_DISPLAY_WIDTH, GAME_DISPLAY_HEIGHT))
        self.grid_show = False
        self.t = 0
        self.score = 0
        self.h_size, self.v_size = self.get_grid_size()
        self.shape_id_curr = None
        self.shape_id_next = None
        self.width_offset = 8
        self.height_offset = 0
        self.selected_shape = None
        self.ix = 0
        self.tetris_board = np.zeros((self.h_size + 1, self.v_size + 1), dtype=int)
        self.key_counter = {'L': 0,
                            'R': 0,
                            'D': 0,
                            'U': 0,
                            'B': 0}
        
        self.key_pressed = {'L': False,
                            'R': False,
                            'D': False,
                            'U': False,
                            'B': False}
        self.active = True
    
    def step(self):
        if not self.active:
            return
        self.t += 1
    
    def reset(self):
        self.t = 0
    
    def update_score(self, point: int):
        self.score += point
    
    def get_score(self):
        return self.score
    
    def get_random_id(self):
        return np.random.randint(0, 4)
    
    def get_screen(self):
        return self.screen
    
    def control_game(self):
        for event in game.event.get():
            if event.type == game.QUIT:
                game.quit()
                quit()
    
    def draw_base(self):
        # draw base for the game
        # tetris main board
        game.draw.line(self.screen, WHITE, [0, 0], [TETRIS_DISPLAY_WIDTH, 0], TETRIS_EDGE_LINEWIDTH)
        game.draw.line(self.screen, WHITE, [TETRIS_DISPLAY_WIDTH, 0], [TETRIS_DISPLAY_WIDTH, TETRIS_DISPLAY_HEIGHT],
                       TETRIS_EDGE_LINEWIDTH)
        game.draw.line(self.screen, WHITE, [TETRIS_DISPLAY_WIDTH, TETRIS_DISPLAY_HEIGHT], [0, TETRIS_DISPLAY_HEIGHT],
                       TETRIS_EDGE_LINEWIDTH)
        game.draw.line(self.screen, WHITE, [0, TETRIS_DISPLAY_HEIGHT], [0, 0], TETRIS_EDGE_LINEWIDTH)
        
        # grid on the main board(this will be removed at the end)
        if self.grid_show:
            h = TETRIS_EDGE_LINEWIDTH + TETRIS_BOX_SIZE
            while h < TETRIS_DISPLAY_HEIGHT:
                game.draw.line(self.screen, GREEN, [TETRIS_EDGE_LINEWIDTH, h],
                               [TETRIS_DISPLAY_WIDTH - TETRIS_EDGE_LINEWIDTH, h], TETRIS_GRID_LINEWIDTH)
                h += TETRIS_BLOCK_SIZE
            
            v = TETRIS_EDGE_LINEWIDTH + TETRIS_BOX_SIZE
            while v < TETRIS_DISPLAY_WIDTH:
                game.draw.line(self.screen, GREEN, [v, TETRIS_EDGE_LINEWIDTH],
                               [v, TETRIS_DISPLAY_HEIGHT - TETRIS_EDGE_LINEWIDTH], TETRIS_GRID_LINEWIDTH)
                v += TETRIS_BLOCK_SIZE
    
    def get_grid_size(self):
        # find the grid size
        h = TETRIS_EDGE_LINEWIDTH + TETRIS_BOX_SIZE
        h_size = 0
        while h < TETRIS_DISPLAY_HEIGHT:
            game.draw.line(self.screen, GREEN, [TETRIS_EDGE_LINEWIDTH, h],
                           [TETRIS_DISPLAY_WIDTH - TETRIS_EDGE_LINEWIDTH, h], TETRIS_GRID_LINEWIDTH)
            h += TETRIS_BLOCK_SIZE
            h_size += 1
        
        v = TETRIS_EDGE_LINEWIDTH + TETRIS_BOX_SIZE
        v_size = 0
        while v < TETRIS_DISPLAY_WIDTH:
            game.draw.line(self.screen, GREEN, [v, TETRIS_EDGE_LINEWIDTH],
                           [v, TETRIS_DISPLAY_HEIGHT - TETRIS_EDGE_LINEWIDTH], TETRIS_GRID_LINEWIDTH)
            v += TETRIS_BLOCK_SIZE
            v_size += 1
        
        return h_size, v_size
    
    def print_score(self):
        offset = 200
        
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 10 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 110 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 110 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 180, 110 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 20, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 110 + offset])
        font = game.font.Font('freesansbold.ttf', 32)
        
        text = font.render('SCORE', True, RED, BLACK)
        textRect = text.get_rect()
        textRect.center = (GAME_DISPLAY_WIDTH - 100, 40 + offset)
        self.screen.blit(text, textRect)
        
        text = font.render('{}'.format(self.get_score()), True, GREEN, BLACK)
        textRect = text.get_rect()
        textRect.center = (GAME_DISPLAY_WIDTH - 100, 85 + offset)
        self.screen.blit(text, textRect)
        
        text = font.render('NEXT', True, BLUE, BLACK)
        textRect = text.get_rect()
        textRect.center = (GAME_DISPLAY_WIDTH - 100, 50)
        self.screen.blit(text, textRect)
    
    def draw_next(self, shapes):
        offset = 15
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 10 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 120 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 120 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 180, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 180, 120 + offset])
        game.draw.line(self.screen, WHITE, [GAME_DISPLAY_WIDTH - 20, 10 + offset],
                       [GAME_DISPLAY_WIDTH - 20, 120 + offset])
        
        width = 26
        height = 8
        for pos in shapes.get_shape(self.shape_id_next, 0)['shape']:
            h = TETRIS_EDGE_LINEWIDTH + (width + int(pos[1])) * TETRIS_BLOCK_SIZE
            v = TETRIS_EDGE_LINEWIDTH + (height + pos[0]) * TETRIS_BLOCK_SIZE
            game.draw.rect(self.screen, RED, [h, v, TETRIS_BOX_SIZE, TETRIS_BOX_SIZE])
    
    def lower(self):
        self.height_offset = self.height_offset + 1
    
    def keyboard_control(self, shapes: Shape):
        if not self.active:
            return
        keys = game.key.get_pressed()
        if keys[game.K_LEFT]:
            self.key_counter['L'] += 1
            if self.key_counter['L'] % TETRIS_KEY_COUNTER == 0:
                self.width_offset -= 1
                self.key_counter['L'] = 0
                self.key_pressed['L'] = True
        if keys[game.K_RIGHT]:
            self.key_counter['R'] += 1
            if self.key_counter['R'] % TETRIS_KEY_COUNTER == 0:
                self.width_offset += 1
                self.key_counter['R'] = 0
                self.key_pressed['R'] = True
        if keys[game.K_DOWN]:
            self.key_counter['D'] += 4
            if self.key_counter['D'] % TETRIS_KEY_COUNTER == 0:
                self.height_offset += 1
                self.key_counter['D'] = 0
                self.key_pressed['D'] = True
        if keys[game.K_SPACE]:
            self.key_counter['B'] += 1
            if self.key_counter['B'] % TETRIS_KEY_COUNTER == 0:
                self.key_pressed['B'] = True
                self.ix += 1
                self.ix = self.ix % self.selected_shape['len']
                self.key_counter['B'] = 0
                self.selected_shape = shapes.get_shape(self.shape_id_curr, self.ix)
    
    def check_game_over(self):
        if np.sum(self.tetris_board[0][:]) > 0 and self.active:
            self.active = False
            print('Game Over...')
    
    def tetris_board_control(self):
        for pos in self.selected_shape['shape']:
            if self.tetris_board[self.height_offset + pos[0]][self.width_offset + pos[1]] == 1:
                if self.key_pressed['L']:
                    self.width_offset += 1
                    self.key_pressed['L'] = False
                    break
                if self.key_pressed['R']:
                    self.width_offset -= 1
                    self.key_pressed['R'] = False
                    break
        
        self.key_pressed['L'] = False
        self.key_pressed['R'] = False
    
    def show_game_over_message(self):
        font = game.font.Font('freesansbold.ttf', 48)
        
        text = font.render('GAME OVER', True, RED, GREEN)
        textRect = text.get_rect()
        textRect.center = (GAME_DISPLAY_WIDTH // 2, GAME_DISPLAY_HEIGHT // 2)
        self.screen.blit(text, textRect)


def main():
    # get all shapes
    shapes = Shape()
    
    # create game object
    my_game = Game()
    screen = my_game.get_screen()
    
    my_game.shape_id_curr = my_game.get_random_id()
    my_game.shape_id_next = my_game.get_random_id()
    
    my_game.selected_shape = shapes.get_shape(my_game.shape_id_curr, 0)
    
    while True:
        my_game.check_game_over()
        
        reach_bottom = False
        screen.fill(BLACK)
        
        my_game.control_game()
        my_game.draw_base()
        
        # keyboard control
        my_game.keyboard_control(shapes)
        
        my_game.tetris_board_control()
        
        min_ver = my_game.selected_shape['min_ver']
        max_ver = my_game.selected_shape['max_ver']
        max_hor = my_game.selected_shape['max_hor']
        
        if my_game.width_offset + min_ver[1] < 0:
            my_game.width_offset = -min_ver[1]
        
        if my_game.width_offset + max_ver[1] >= my_game.v_size:
            my_game.width_offset = my_game.v_size - max_ver[1] - 1
        
        if my_game.height_offset + max_hor[0] >= my_game.h_size:
            my_game.height_offset = my_game.h_size - max_hor[0] - 1
            reach_bottom = True
        
        for pos in my_game.selected_shape['shape']:
            if my_game.tetris_board[my_game.height_offset + pos[0] + 1][my_game.width_offset + pos[1]] == 1:
                reach_bottom = True
        
        if not my_game.active:
            reach_bottom = False
        
        if reach_bottom:
            for pos in my_game.selected_shape['shape']:
                my_game.tetris_board[my_game.height_offset + pos[0]][my_game.width_offset + pos[1]] = 1
            to_be_deleted = []
            for r in range(my_game.h_size):
                if np.sum(my_game.tetris_board[r][:]) == my_game.v_size:
                    to_be_deleted.append(r)
            if len(to_be_deleted) != 0:
                my_game.update_score(len(to_be_deleted))
                my_game.tetris_board = np.delete(my_game.tetris_board, tuple(to_be_deleted), 0)
                
                for s in range(len(to_be_deleted)):
                    new_row = np.zeros((1, my_game.v_size + 1), dtype=int)
                    my_game.tetris_board = np.concatenate((new_row, my_game.tetris_board), axis=0)
            
            my_game.width_offset = 8
            my_game.height_offset = 0
            my_game.shape_id_curr = my_game.shape_id_next
            my_game.shape_id_next = my_game.get_random_id()
            my_game.selected_shape = shapes.get_shape(my_game.shape_id_curr, 0)
        
        for pos in my_game.selected_shape['shape']:
            h = TETRIS_EDGE_LINEWIDTH + (my_game.width_offset + int(pos[1])) * TETRIS_BLOCK_SIZE
            v = TETRIS_EDGE_LINEWIDTH + (my_game.height_offset + pos[0]) * TETRIS_BLOCK_SIZE
            game.draw.rect(screen, RED, [h, v, TETRIS_BOX_SIZE, TETRIS_BOX_SIZE])
        
        for r in range(my_game.h_size):
            for c in range(my_game.v_size):
                if my_game.tetris_board[r][c] == 1:
                    h = TETRIS_EDGE_LINEWIDTH + c * TETRIS_BLOCK_SIZE
                    v = TETRIS_EDGE_LINEWIDTH + r * TETRIS_BLOCK_SIZE
                    game.draw.rect(screen, BLUE, [h, v, TETRIS_BOX_SIZE, TETRIS_BOX_SIZE])
        
        my_game.print_score()
        
        my_game.step()
        
        my_game.draw_next(shapes)
        
        if not my_game.active:
            my_game.show_game_over_message()
        
        if my_game.t % TETRIS_TIME_COUNTER == 0:
            my_game.lower()
            my_game.reset()
        
        game.display.update()


if __name__ == '__main__':
    main()
