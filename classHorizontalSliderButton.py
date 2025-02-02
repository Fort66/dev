import pygame as pg
from pygame.locals import MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame import Surface
from pygame.transform import scale

from classScreen import screen

from dataclasses import dataclass, field, InitVar


@dataclass
class HorizontalSliderButton:
    """
    A class representing a horizontal slider button with a draggable slider.

    This class is designed to create a horizontal slider button with a draggable slider.
    It supports various customization options such as colors, text, and event handling.
    The slider can be moved using mouse events and its position is reflected in the `currentValue` attribute.

    Attributes:
        screen (object): The screen object where the slider button will be drawn.
        pos (tuple): The position of the slider button on the screen.
        size (tuple): The size of the slider button.
        minValue (int | float): The minimum value of the slider.
        maxValue (int | float): The maximum value of the slider.
        currentValue (int | float): The current value of the slider.
        colorButton (str | tuple): The color of the button.
        colorScaleLeft (str | tuple): The color of the left scale.
        hoverColorSlider (str | tuple): The color of the slider when hovered.
        colorSlider (str | tuple): The color of the slider.
        hoverColor (str | tuple): The color when the slider button is hovered.
        textColor (str | tuple): The color of the text.
        disabledColor (str | tuple): The color when the slider button is disabled.
        isHovered (bool): Whether the slider button is currently hovered.
        isClicked (bool): Whether the slider button is currently clicked.
        onEnabled (bool): Whether the slider button is enabled.

    Methods:
        __post_init__(): Initializes the slider button surfaces and rectangles.
        createLeftSurface(): Creates the left surface of the slider button.
        changeCurrentValue(): Updates the current value of the slider based on its position.
        checkPosition(event): Checks and updates the position of the slider based on mouse events.
        handleEvent(event): Handles mouse events to move the slider and change its state.
        drawText(): Draws the text (min, max, and current values) on the screen.
        update(): Updates and draws the slider button on the screen.
    """

    screen: object = None
    pos: tuple = (0, 0)
    size: tuple = (200, 50)
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
        # Create a surface for the button with the given size and transparency
        self.buttonSurface = Surface(self.size, pg.SRCALPHA)
        self.buttonSurface.set_alpha(0)
        # Fill the button surface with the given color
        self.buttonSurface.fill(self.colorButton)
        # Get the rectangle of the button surface
        self.buttonRect = self.buttonSurface.get_rect(topleft=self.pos)

        # Create a surface for the scale with the given size and transparency
        self.scaleSurface = Surface((self.size[0], self.size[1] // 10), pg.SRCALPHA)
        self.scaleSurface.set_alpha(70)
        # Fill the scale surface with the given color
        self.scaleSurface.fill(self.colorButton)
        # Get the rectangle of the scale surface
        self.scaleRect = self.scaleSurface.get_rect(center=self.buttonRect.center)

        # Create a surface for the slider with the given size
        self.sliderSurface = Surface((self.size[0] // 20, self.size[1] // 2))
        # Fill the slider surface with the given color
        self.sliderSurface.fill(self.colorSlider)

        # Calculate the value of one step on the scale
        self.oneStepValue = (self.scaleRect.right - self.scaleRect.left) / (self.maxValue - self.minValue)

        # Get the rectangle of the slider surface and set its center to the current value
        self.sliderRect = self.sliderSurface.get_rect(center=(self.scaleRect.x + self.currentValue * self.oneStepValue, self.scaleRect.centery))

        # Create the left surface
        self.createLeftSurface()
        self.changeCurrentValue()

    def createLeftSurface(self):
        # Check if the left side of the slider is to the right of the left side of the scale
        if self.sliderRect.left > self.scaleRect.left:
            # Scale the scale surface to the width of the slider
            self.scaleSurfaceLeft = scale(self.scaleSurface.copy(), (self.sliderRect.left - self.scaleRect.left, self.scaleRect.height))
        else:
            # If not, create an empty surface
            self.scaleSurfaceLeft = Surface((0, 0))
        # Set the alpha of the scale surface to 256
        self.scaleSurfaceLeft.set_alpha(256)
        # If the slider is enabled, fill the scale surface with the colorScaleLeft color
        if self.onEnabled:
            self.scaleSurfaceLeft.fill(self.colorScaleLeft)
        # Otherwise, fill the scale surface with the disabledColor
        else:
            self.scaleSurfaceLeft.fill(self.disabledColor)
        # Get the rectangle of the scale surface and set the top left corner to the top left corner of the scale
        self.scaleRectLeft = self.scaleSurfaceLeft.get_rect(topleft=self.scaleRect.topleft)

    def changeCurrentValue(self):
        # Calculate the current value based on the position of the slider and the scale
        self.currentValue = (self.sliderRect.centerx - self.scaleRect.x) / self.oneStepValue

        # Calculate the width of the left scale rectangle
        self.scaleRectLeft.width = self.sliderRect.left - self.scaleRect.left
        # Set the top left corner of the left scale rectangle to the top left corner of the scale rectangle
        self.scaleRectLeft.topleft = self.scaleRect.topleft
        # Create the left surface of the scale
        self.createLeftSurface()

        # Print the current value
        print(self.currentValue)

    def checkPosition(self, event):
        self.sliderRect.center = (event.pos[0], self.sliderRect.center[1])
        if self.sliderRect.centerx >= self.buttonRect.right:
            self.sliderRect.centerx = self.buttonRect.right
        if self.sliderRect.centerx <= self.buttonRect.left:
            self.sliderRect.centerx = self.buttonRect.left

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
                    self.checkPosition(event)
                    self.changeCurrentValue()

            elif event.type == MOUSEBUTTONUP:
                self.isClicked = False
        else:
            self.sliderSurface.fill(self.disabledColor)

    def drawText(self):
        minText = pg.font.SysFont('arial', 14).render(str(self.minValue), True, self.textColor)
        maxText = pg.font.SysFont('arial', 14).render(str(self.maxValue), True, self.textColor)
        valueText = pg.font.SysFont('arial', 14).render(str(self.currentValue), True, self.textColor)

        screen.blit(minText, (self.scaleRect.left - maxText.get_width(), self.scaleRect.y))
        screen.blit(maxText, (self.scaleRect.right + maxText.get_width(), self.scaleRect.y))
        screen.blit(valueText, (self.sliderRect.centerx - valueText.get_width() // 2, self.buttonRect.top - valueText.get_height()))

    def update(self):
        screen.blit(self.buttonSurface, self.buttonRect)
        screen.blit(self.scaleSurfaceLeft, self.scaleRectLeft)
        screen.blit(self.scaleSurface, self.scaleRect)
        screen.blit(self.sliderSurface, self.sliderRect)
        self.drawText()
