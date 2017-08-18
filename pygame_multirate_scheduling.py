#!python3
import pygame as pg
from pygame.locals import K_w, KMOD_META
from sched import scheduler
from time import time, sleep


class Counter():

    def __init__(self):
        self.count = -1

    def incr(self):
        self.count += 1


class Periodic():

    def __init__(self, scheduler, period, priority, action):
        self.scheduler = scheduler
        self.period = period
        self.priority = priority
        self.action = action
        self.next = None
        self.event = None

    def start(self):
        self.next = time()
        self.run()

    def run(self):
        self.next += self.period
        self.event = self.scheduler.enterabs(self.next, self.priority, self.run)
        self.action()

    def stop(self):
        if self.event:
            self.scheduler.cancel(self.event)


class Display():

    def __init__(self, rates):
        assert len(rates) > 0, "Must enter an iterable of at least one rate!"

        self.screen_width = 300
        self.screen_height = 150
        self.update_rate = 0.02
        self.screen = pg.display.set_mode((self.screen_width,
                                           self.screen_height))
        pg.display.set_caption("Threads!")  # The window title
        pg.init()  # must be called before pg.font.SysFont()
        self.font = pg.font.SysFont("monospace", 24)
        self.clock = pg.time.Clock()

        self.scheduler = scheduler(time, sleep)

        fps = 1 / 50
        self.tasks = [Periodic(self.scheduler, fps, 0, self.update),
                      Periodic(self.scheduler, fps, 2, self.check_for_quit)]
        self.counters = []
        self.x = []

        dx = self.screen_width / len(rates)
        x = dx / 2
        for r in rates:
            counter = Counter()
            self.tasks.append(Periodic(self.scheduler, r, 1, counter.incr))
            self.counters.append(counter)
            self.x.append(x)
            x += dx
        self.start = time()
        for task in self.tasks:
            task.start()

    def update(self):

        self.clock.tick()

        self.screen.fill((50, 50, 50))

        label = self.font.render("{:.2f} ({:.2f} fps)".format(time() - self.start, self.clock.get_fps()),
                                 1, (250, 250, 250))
        r = label.get_rect()
        self.screen.blit(label, [10, 10])

        y = (self.screen_height - 10) / 3
        y = [20 + y, 20 + 2 * y]

        for t, c, x in zip(self.tasks[2:], self.counters, self.x):
            expected = int((time() - self.start) // t.period)
            if c.count == expected:
                color = (50, 250, 50)  # green for good
            else:
                color = (250, 50, 50)  # red for bad
            # Draw the counter from the task
            label = self.font.render(str(c.count), 1, color)
            r = label.get_rect()
            pos = [x - r.width / 2, y[0] - r.height / 2]
            pos = [int(round(p)) for p in pos]
            self.screen.blit(label, pos)
            # Draw the expected value based on the rate and current time
            label = self.font.render(str(expected), 1, (250, 250, 250))
            r = label.get_rect()
            pos = [x - r.width / 2, y[1] - r.height / 2]
            pos = [int(round(p)) for p in pos]
            self.screen.blit(label, pos)

        pg.display.flip()

    def check_for_quit(self):
        running = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                break
            if (event.type == pg.KEYDOWN and
                    event.key == K_w and
                    pg.key.get_mods() & KMOD_META):
                running = False
                break
        if not running:
            self.quit()

    def quit(self):
        for t in self.tasks:
            t.stop()
        pg.display.quit()
        pg.quit()

    def run(self):
        self.scheduler.run()


if __name__ == "__main__":
    d = Display([1 / 10, 1 / 2, 1, 2, 5])
    d.run()
