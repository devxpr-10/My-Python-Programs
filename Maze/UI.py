import pygame

class Button:
    def __init__(self, pos: tuple, size: tuple, colors: tuple[str | tuple], font: pygame.font):
        """Colors: Default Color, Mouse Hover Color, Click Color, Text Color, Border Color"""
        self.x, self.y = pos
        self.wid, self.hei = size
        self.rect = pygame.Rect(self.x, self.y, self.wid, self.hei)

        self.colors = {}
        self.colors["def"], self.colors["hover"], self.colors["click"], self.colors["text"], self.colors['border'] = colors
        self.activeColor = self.colors["def"]

        self.font = font

        self.clicked: bool = False
        self.hovering: bool = False


        self._timePassed = pygame.time.get_ticks()
        self._delay = 500

    def render(self, window: pygame.Surface, text: str):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.clicked = pygame.mouse.get_pressed()[0]
        self.hovering = mouse_x > self.x and mouse_y > self.y and mouse_x < self.x + self.wid and mouse_y < self.y + self.hei
        if self.hovering and not self.clicked:
            self.activeColor = self.colors['hover']
        if self.clicked and self.hovering:
            self.activeColor = self.colors['click']
        if not self.hovering and not self.clicked:
            self.activeColor = self.colors['def']
        pygame.draw.rect(window, self.colors['border'], [self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4])
        pygame.draw.rect(window, self.activeColor, self.rect)
        self._renderedFont = self.font.render(text, True, self.colors["text"])
        window.blit(self._renderedFont, self._renderedFont.get_rect(center=self.rect.center))

    def onClick(self, function: callable):
        time_now = pygame.time.get_ticks()
        if self.clicked and self.hovering and time_now - self._delay > self._timePassed:
            function()
            self._timePassed = time_now