import pygame


class TextSprite(pygame.sprite.Sprite):
    def __init__(self, text='', font=None, color='black', anchor='center'):
        self.__font = font
        self.__text = text
        self.__color = color
        self.__anchor = anchor
        self.image = self.__font.render(self.__text, False, self.__color)
        self.rect = self.image.get_rect()

    def set_text(self, new_text: str):
        self.__text = new_text
        self.render()

    def set_color(self, new_color):
        self.__color = new_color
        self.render()

    def set_font(self, new_font):
        self.__font = new_font
        self.render()

    def render(self):
        rect_anchor = {self.__anchor: getattr(self.rect, self.__anchor)}
        self.image = self.__font.render(self.__text, False, self.__color)
        self.rect = self.image.get_rect(**rect_anchor)
