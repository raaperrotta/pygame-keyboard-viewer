#!python3
import pygame as pg
from pygame import gfxdraw
from pygame.locals import *
from threading import Thread, Timer
from time import time

class CounterTask():

    def __init__(self, period):
        self.count = 0
        self.period = period
        self.timer = None
        self.run()

    def run(self):
        self.timer = Timer(self.period, self.run)
        self.timer.start()
        self.count += 1

    def quit(self):
        if self.timer is not None:
            self.timer.cancel()


class Display():
    def __init__(self, rates):
        self.screen_width = 300
        self.screen_height = 100
        self.update_rate = 0.02
        self.start = time()
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Threads!")  # The window title
        pg.init()  # must be called before pg.font.SysFont()

        self.tasks = []
        if rates:
            dx = self.screen_width / len(rates)
            x = dx/2
            for r in rates:
                self.tasks.append((CounterTask(r), x))
                x += dx

    def update(self):
        self.screen.fill((50, 50, 50))

        font = pg.font.SysFont("monospace", 16)
        label = font.render("{:.2f}".format(time()-self.start), 1, (250, 250, 250))
        r = label.get_rect()
        self.screen.blit(label, [10, 10])

        for t, x in self.tasks:
            font = pg.font.SysFont("monospace", 32)
            label = font.render(str(t.count), 1, (250, 250, 250))
            r = label.get_rect()
            pos = [x - r.width/2., self.screen_height/2 - r.height/2.]
            pos = [int(round(p)) for p in pos]
            self.screen.blit(label, pos)

        pg.display.flip()

    def check_for_quit(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if (event.type == pg.KEYDOWN and
                    event.key == K_w and
                    pg.key.get_mods() & KMOD_META):
                running = False
        return running

    def quit(self):
        pg.display.quit()
        pg.quit()
        for t, x in self.tasks:
            t.quit()

if __name__ == "__main__":
    d = Display([1, 2, 3, 4, 5, 6])
    clock = pg.time.Clock()
    while d.check_for_quit():
        clock.tick(60)
        d.update()
    d.quit()
