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
    hoverColorSlider: str | tuple = 'red'
    colorSlider: str | tuple = 'Maroon'
    hoverColor: str | tuple = 'darkgray'
    
    
    isHovered: bool = False
    isClicked: bool = False
    isDragDroped: bool = False
    
    def __post_init__(self):
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(0)
        self.buttonSurface.fill(self.colorButton)
        self.buttonRect = self.buttonSurface.get_rect(topleft = self.pos)
        
        self.scaleSurface = Surface((self.size[0], self.size[0] // 30))
        self.scaleSurface.fill(self.colorScale)
        self.scaleRect = self.scaleSurface.get_rect(center = self.buttonRect.center)
        
        self.sliderSurface = Surface((self.size[0] // 20, self.size[1] // 2))
        self.sliderSurface.fill(self.colorSlider)
        self.sliderRect = self.sliderSurface.get_rect(center = self.scaleRect.center)
    
    
    def handleEvent(self, event):
        if self.isClicked:
            if event.type == MOUSEMOTION:
                self.sliderRect.center = (event.pos[0], self.sliderRect.center[1])
                if self.sliderRect.right > self.buttonRect.right:
                    self.sliderRect.right = self.buttonRect.right
                if self.sliderRect.left < self.buttonRect.left:
                    self.sliderRect.left = self.buttonRect.left
                print(event.pos[0])

        if event.type == MOUSEMOTION:
            if self.sliderRect.collidepoint(event.pos):
                self.isHovered = True
                self.sliderSurface.fill(self.hoverColorSlider)
            else:
                self.isHovered = False
                self.sliderSurface.fill(self.colorSlider)
        if event.type == MOUSEBUTTONDOWN and self.isHovered:
            if event.button == 1:
                self.isClicked = True
                self.isDragDroped = True
                
        elif event.type == MOUSEBUTTONUP:
            self.isClicked = False
            self.isDragDroped = False
                
    
    def update(self):
        screen.blit(self.buttonSurface, self.buttonRect)
        screen.blit(self.scaleSurface, self.scaleRect)
        screen.blit(self.sliderSurface, self.sliderRect)




screen = pg.display.set_mode((800,600))


slider = SliderButton(screen = screen, pos = (100, 100), size = (200, 50), minValue = 0, maxValue = 100, currentValue = 50)


run  = True
while run:
    screen.fill('steelblue')
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        slider.handleEvent(event)
    
    slider.update()
    
    
    pg.display.update()
pg.quit()
