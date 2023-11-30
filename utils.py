from cmu_graphics import *
import random

class Button:
    def __init__(self, label, x, y, width, height, action, fillColor='gray', textColor='black'):
        self.label = label
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        self.fillColor = fillColor
        self.textColor = textColor

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height, fill=self.fillColor)
        drawLabel(self.label, self.x + self.width / 2, self.y + self.height / 2, fill=self.textColor)

    def isClicked(self, x, y):
        return (self.x <= x <= self.x + self.width and
                self.y <= y <= self.y + self.height)

    def onClick(self, x, y):
        if self.isClicked(x, y):
            self.action()
