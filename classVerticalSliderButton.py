import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Surface
from pygame.transform import scale

from classScreen import screen

from dataclasses import dataclass, field, InitVar


@dataclass
class VerticalSliderButton:
    """
    A class representing a vertical slider button with a scale and a slider.

    This class is designed to create a vertical slider button with a scale and a slider.
    It allows users to interact with the slider to change the current value, which can be
    used to control various parameters in a graphical user interface (GUI).

    Attributes:
        screen (object): The screen object where the button will be drawn.
        pos (tuple): The position of the button on the screen.
        size (tuple): The size of the button.
        minValue (int | float): The minimum value of the slider.
        maxValue (int | float): The maximum value of the slider.
        currentValue (int | float): The current value of the slider.
        colorButton (str | tuple): The color of the button.
        colorScaleLeft (str | tuple): The color of the left side of the scale.
        hoverColorSlider (str | tuple): The color of the slider when hovered.
        colorSlider (str | tuple): The color of the slider.
        hoverColor (str | tuple): The color when the button is hovered.
        textColor (str | tuple): The color of the text.
        disabledColor (str | tuple): The color when the button is disabled.
        isHovered (bool): Whether the button is currently hovered.
        isClicked (bool): Whether the button is currently clicked.
        onEnabled (bool): Whether the button is enabled.

    Methods:
        __post_init__(): Initializes the button surfaces and rectangles.
        createBottomSurface(): Creates the bottom surface of the scale.
        changeCurrentValue(): Changes the current value of the slider based on the slider's position.
        checkPosition(event): Checks the position of the slider based on the mouse event.
        handleEvent(event): Handles the mouse events for the button and slider.
        drawText(): Draws the text for the minimum, maximum, and current values.
        update(): Updates the button and slider surfaces on the screen.
    """
    screen: object = None
    pos: tuple = (0, 0)
    size: tuple = (50, 200)
    minValue: int | float = 0
    maxValue: int | float = 100
    currentValue: int | float = 50
    colorButton: str | tuple = 'LightGray'
    colorScaleLeft: str | tuple = 'green'
    hoverColorSlider: str | tuple = 'red'
    colorSlider: str | tuple = 'Maroon'
    hoverColor: str | tuple = 'darkgray'
    textColor: str | tuple = 'white'
    disabledColor: str | tuple = 'darkgray'

    isHovered: bool = False
    isClicked: bool = False
    onEnabled: bool = True

    def __post_init__(self):
        # Create a surface for the button with the size of the slider and set its alpha to 0
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(0)
        # Fill the button surface with the color of the button
        self.buttonSurface.fill(self.colorButton)
        # Get the rectangle of the button surface and set its top left corner to the position of the slider
        self.buttonRect = self.buttonSurface.get_rect(topleft = self.pos)

        # Create a surface for the scale with the size of the slider divided by 10 and set its alpha to 70
        self.scaleSurface = Surface((self.size[0] // 10, self.size[1]), pg.SRCALPHA)
        self.scaleSurface.set_alpha(70)
        # Fill the scale surface with the color of the button
        self.scaleSurface.fill(self.colorButton)
        # Get the rectangle of the scale surface and set its center to the center of the button rectangle
        self.scaleRect = self.scaleSurface.get_rect(center = self.buttonRect.center)

        # Create a surface for the slider with the size of the slider divided by 2 and the size of the slider divided by 20
        self.sliderSurface = Surface((self.size[0] // 2, self.size[1] // 20))
        # Fill the slider surface with the color of the slider
        self.sliderSurface.fill(self.colorSlider)

        # Calculate the value of one step on the scale
        self.oneStepValue = (self.scaleRect.bottom - self.scaleRect.top) / (self.maxValue - self.minValue)


        # Get the rectangle of the slider surface and set its center to the center of the scale rectangle
        self.sliderRect = self.sliderSurface.get_rect(center = (self.scaleRect.x + self.currentValue * self.oneStepValue, self.scaleRect.centery))
        # Get the rectangle of the slider surface and set its center to the center of the scale rectangle
        self.sliderRect = self.sliderSurface.get_rect(center = (self.scaleRect.centerx, self.scaleRect.bottom - self.currentValue * self.oneStepValue))
        print(self.sliderRect.center)

        self.createBottomSurface()
        self.changeCurrentValue()


    def createBottomSurface(self):
        # Check if the bottom of the slider is below the bottom of the scale
        if self.sliderRect.bottom < self.scaleRect.bottom:
            # Scale the scale surface to fit the width of the scale and the height from the bottom of the slider to the bottom of the scale
            self.scaleSurfaceBottom = scale(self.scaleSurface.copy(), (self.scaleRect.width, self.scaleRect.bottom - self.sliderRect.bottom))
        else:
            # If the slider is above the scale, create an empty surface
            self.scaleSurfaceBottom = Surface((0, 0))
        # Set the alpha of the scale surface to 256
        self.scaleSurfaceBottom.set_alpha(256)
        # Check if the slider is enabled
        if self.onEnabled:
            # If the slider is enabled, fill the scale surface with the color of the left side of the scale
            self.scaleSurfaceBottom.fill(self.colorScaleLeft)
        else:
            # If the slider is disabled, fill the scale surface with the disabled color
            self.scaleSurfaceBottom.fill(self.disabledColor)
        # Get the rectangle of the scale surface and set the bottom left corner to the bottom left corner of the scale
        self.scaleRectBottom = self.scaleSurfaceBottom.get_rect(bottomleft = self.scaleRect.bottomleft)

    def changeCurrentValue(self):
        # Calculate the current value based on the position of the slider and the scale
        self.currentValue = (self.scaleRect.bottom - self.sliderRect.centery) / self.oneStepValue

        # Set the width of the bottom surface of the scale to the distance between the left edge of the slider and the left edge of the scale
        self.scaleRectBottom.width = self.sliderRect.left - self.scaleRect.left
        # Set the top left corner of the bottom surface of the scale to the top left corner of the scale
        self.scaleRectBottom.topleft = self.scaleRect.topleft
        # Create the bottom surface of the scale
        self.createBottomSurface()

        # Print the current value
        print(self.currentValue)

    def checkPosition(self, event):
        self.sliderRect.center = (self.sliderRect.center[0], event.pos[1])
        if self.sliderRect.centery <= self.buttonRect.top:
            self.sliderRect.centery = self.buttonRect.top
        if self.sliderRect.centery >= self.buttonRect.bottom:
            self.sliderRect.centery = self.buttonRect.bottom

    def handleEvent(self, event):
        if self.onEnabled:
            if self.isClicked:
                if event.type == MOUSEMOTION:
                    self.checkPosition(event)
                    self.changeCurrentValue()

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
            elif event.type == MOUSEBUTTONDOWN and self.scaleRect.collidepoint(event.pos):
                if event.button == 1:
                    self.sliderRect.center = (self.sliderRect.center[0], event.pos[1])
                    self.changeCurrentValue()

            elif event.type == MOUSEBUTTONUP:
                self.isClicked = False
        else:
            self.sliderSurface.fill(self.disabledColor)

    def drawText(self):
        minText = pg.font.SysFont('arial', 14).render(str(self.minValue), True, self.textColor)
        maxText = pg.font.SysFont('arial', 14).render(str(self.maxValue), True, self.textColor)
        valueText = pg.font.SysFont('arial', 14).render(str(self.currentValue), True, self.textColor)

        screen.blit(minText, (self.scaleRect.x, self.scaleRect.bottom + maxText.get_width()))
        screen.blit(maxText, (self.scaleRect.x, self.scaleRect.top - maxText.get_width()))
        screen.blit(valueText, (self.buttonRect.left - valueText.get_width(), self.sliderRect.centery - valueText.get_height() // 2))

    def update(self):
        screen.blit(self.buttonSurface, self.buttonRect)
        screen.blit(self.scaleSurfaceBottom, self.scaleRectBottom)
        screen.blit(self.scaleSurface, self.scaleRect)
        screen.blit(self.sliderSurface, self.sliderRect)
        self.drawText()
