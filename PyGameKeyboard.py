#!python3
import pygame as pg
from pygame import gfxdraw
from pygame.locals import *

win_width = 900
win_height = 400

margin = 0.125
keyboard = [
    ['esc'] + ['F{}'.format(x+1) for x in range(12)] + ['eject'],
    ['`'] + ['{}'.format(x+1) for x in range(9)] + ['0', '-', '=', ('delete', 1.5)],
    [('tab', 1.5), 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    [('caps', 1.8), 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', ('enter', 1.8)],
    [('shift', 2), 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', ('shift', 2)],
    ['fn', 'ctrl', 'alt', ('cmd', 1.25), ('space', 7), ('cmd', 1.25), 'alt', ('ARROWS', 3+2*margin)],
    ]
keyshift = [
    ['esc'] + ['F{}'.format(x+1) for x in range(12)] + ['eject'],
    ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', ('delete', 1.5)],
    [('tab', 1.5), 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
    [('caps', 1.8), 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', ('enter', 1.8)],
    [('shift', 2), 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', ('shift', 2)],
    ['fn', 'ctrl', 'alt', ('cmd', 1.25), ('space', 7), ('cmd', 1.25), 'alt', ('ARROWS', 3+2*margin)],
    ]
bindings = [
    [K_ESCAPE, K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10, K_F11, K_F12, None],
    [K_BACKQUOTE, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9, K_0, K_MINUS, K_EQUALS, K_BACKSPACE],
    [K_TAB, K_q, K_w, K_e, K_r, K_t, K_y, K_u, K_i, K_o, K_p, K_LEFTBRACKET, K_RIGHTBRACKET, K_BACKSLASH],
    [K_CAPSLOCK, K_a, K_s, K_d, K_f, K_g, K_h, K_j, K_k, K_l, K_SEMICOLON, K_QUOTE, K_RETURN],
    [K_LSHIFT, K_z, K_x, K_c, K_v, K_b, K_n, K_m, K_COMMA, K_PERIOD, K_SLASH, K_RSHIFT],
    [None, K_LCTRL, K_LALT, K_LMETA, K_SPACE, K_RMETA, K_RALT, None],
]

pg.init()
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("PyGame Key Press Visualizer")  # The window title


class Key():
    def __init__(self, name, shift, binding, x, y, width, height):
        self.name = name
        self.shift = shift
        self.binding = binding
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # Draw in unuesd state, will be overwritten as soon as run loop starts
        if binding is None:
            self.draw(None, False)
        else:
            self.draw(False, False)

    def draw(self, pressed, shifted):

        if pressed is None:  # Unused state (overwritten if binding exists)
            key_color = (50, 50, 50)
            txt_color = (80, 80, 80)
        elif pressed:
            key_color = (150, 150, 150)
            txt_color = (0, 0, 0)
        else:
            key_color = (50, 50, 50)
            txt_color = (250, 250, 250)

        points = [
                  [self.x, self.y],
                  [self.x, self.y+self.height],
                  [self.x+self.width, self.y+self.height],
                  [self.x+self.width, self.y]
                 ]
        points = [[int(round(x)) for x in xy] for xy in points]

        gfxdraw.filled_polygon(screen, points, key_color)
        gfxdraw.aapolygon(screen, points, key_color)

        font = pg.font.SysFont("monospace", 12)
        if shifted:
            name = self.shift
        else:
            name = self.name
        label = font.render(name, 1, txt_color)
        r = label.get_rect()
        center = [self.x+self.width/2, self.y+self.height/2]
        corner = [center[0]-r.width/2, center[1]-r.height/2]
        corner = [int(round(x)) for x in corner]
        screen.blit(label, corner)


class Row():
    def __init__(self, keys, shift, bindings, y, height):
        self.keys = []
        # Determine full length of row so it can be normalized to keyboard
        length = margin * (len(keys) + 1)
        for key in keys:
            if type(key) is tuple:
                length += key[1]
            else:
                length += 1
        dx = win_width/length
        x = margin * dx
        for ii, (key, sh, bind) in enumerate(zip(keys, shift, bindings)):
            width = dx
            if type(key) is tuple:
                key, width = key[0], key[1]*dx
                sh = sh[0]
            if key == "ARROWS":
                width = dx
                m = margin*dx
                h = float(height-m)/2.
                self.keys.append(Key('<', '<', K_LEFT, x, y+h+m, width, h))
                self.keys.append(Key('^', '^', K_UP, x+m+width, y, width, h))
                self.keys.append(Key('v', 'v', K_DOWN, x+m+width, y+h+m, width, h))
                self.keys.append(Key('>', '>', K_RIGHT, x+2*(m+width), y+h+m, width, h))
            else:
                self.keys.append(Key(key, sh, bind, x, y, width, height))
                x += width + margin*dx


is_first = True
dy = win_height/(len(keyboard) - 1/2 + 7*margin)
y = margin * dy
keys = []
for k_row, s_row, b_row in zip(keyboard, keyshift, bindings):
    height = dy
    if is_first:
        is_first = False
        height = dy/2
    r = Row(k_row, s_row, b_row, y, height)
    keys += r.keys
    y += height + margin*dy

clock = pg.time.Clock()
fps = 60

draw_by_event = False
k_dict = {}
for key in keys:
    k_dict[key.binding] = key

running = True
while running:

    clock.tick(fps)
    actual_fps = clock.get_fps()

    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            running = False
        if (event.type == pg.KEYDOWN and
                event.key == K_w and
                pg.key.get_mods() & KMOD_META):
            running = False

    pressed = pg.key.get_pressed()
    shifted = pg.key.get_mods() & KMOD_SHIFT

    if draw_by_event:
        """Using keydown and keyup events is slightly less straightforward than
        using get_pressed, but the Pygame event queue is sure to keep all
        keydown events, so they won't be missed, even if the keyup event
        occurred in the same interval."""
        for event in events:
            if event.type == pg.KEYDOWN:
                k_dict[event.key].draw(True, shifted)
            elif event.type == pg.KEYUP:
                k_dict[event.key].draw(False, shifted)
    else:
        """Drawing using get_pressed is easy! But is it possible that some key
        presses would be missed because they occurred between iterations?"""
        for key in keys:
            if key.binding is not None:
                key.draw(pressed[key.binding], shifted)

    pg.display.flip()

pg.display.quit()
pg.quit()
