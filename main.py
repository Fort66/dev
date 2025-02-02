import pygame as pg
from pygame import Surface
from pygame.locals import *
from pygame.transform import scale

from loguru import logger
from sys import stdout

from icecream import ic
from dataclasses import dataclass, field, InitVar

logger.add(stdout,
           format="{time:DD.MM.YYYY HH:mm:ss} | {level} | {file}:{line} |{message}",
           level="DEBUG")

from classScreen import screen
from classHorizontalSliderButton import HorizontalSliderButton
from classVerticalSliderButton import VerticalSliderButton

pg.init()




hSliderEn = HorizontalSliderButton(screen = screen,
                                 pos = (50, 50),
                                 size = (200, 50),
                                 minValue = 0,
                                 maxValue = 100,
                                 currentValue = 50,
                                 onEnabled = True,)

hSliderDis = HorizontalSliderButton(screen = screen,
                                 pos = (350, 50),
                                 size = (200, 50),
                                 minValue = 0,
                                 maxValue = 100,
                                 currentValue = 50,
                                 onEnabled = False,)

vSliderEn = VerticalSliderButton(screen = screen,
                               pos = (50, 200),
                               size = (50, 200),
                               minValue = 0,
                               maxValue = 100,
                               currentValue = 50,
                               onEnabled = True,)

vSliderDis = VerticalSliderButton(screen = screen,
                               pos = (300, 200),
                               size = (50, 200),
                               minValue = 0,
                               maxValue = 100,
                               currentValue = 50,
                               onEnabled = False,)



def runGame():
    run  = True
    while run:
        screen.fill('steelblue')
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            hSliderEn.handleEvent(event)
            hSliderDis.handleEvent(event)
            vSliderEn.handleEvent(event)
            vSliderDis.handleEvent(event)

        hSliderEn.update()
        hSliderDis.update()
        vSliderEn.update()
        vSliderDis.update()

        pg.display.update()
    pg.quit()


@logger.catch
def main():
    runGame()



if __name__ == '__main__':
    main()