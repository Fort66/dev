import pygame as pg
from pygame import Surface
from pygame.locals import *

from dataclasses import dataclass, field, InitVar


@dataclass
class SliderButton:
    screen: object = None
    pos: tuple = (0, 0)
    size: tuple = (200, 50)
    minValue: int | float = 0
    maxValue: int | float = 100
    currentValue: int | float = 50
    colorButton: str | tuple = 'LightGray'
    colorScale: str | tuple = 'green'
    colorSlider: str | tuple = 'red'
    hoverColor: str | tuple = 'darkgray'
    
    isHovered: bool = False
    isClicked: bool = False
    isDragDroped: bool = False
    
    def __post_init__(self):
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(50)
        self.buttonSurface.fill(self.colorButton)
        self.buttonRect = self.buttonSurface.get_rect(topleft = self.pos)
        
        self.scaleSurface = Surface((self.size[0], self.size[0] // 30))
        self.scaleSurface.fill(self.colorScale)
        self.scaleRect = self.scaleSurface.get_rect(center = self.buttonRect.center)
    
    
    def update(self):
        screen.blit(self.buttonSurface, self.buttonRect)
        screen.blit(self.scaleSurface, self.scaleRect)




screen = pg.display.set_mode((800,600))


slider = SliderButton(screen = screen, pos = (100, 100), size = (200, 50), minValue = 0, maxValue = 100, currentValue = 50)


run  = True
while run:
    screen.fill('steelblue')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    slider.update()
    
    
    pg.display.update()
pg.quit()
