import pygame
pygame.init()

from abc import ABC, abstractmethod

# используем абстрактный класс для создания общего интерфейса любого меню
class AbstractMenu(ABC):
    def __init__(self, font: object) -> None:
        # список поверхностей (элементов) меню
        self.option_surfaces = []
        # список фукнций связанных с определенной опцией
        self.callbacks = []
        # список прямоугольников для каждой поверзности
        self.rects = []
        # формат текста для кнопок меню
        self.font = font
      
    @abstractmethod
    def append_option(self, option: str, option_callback: object, color: tuple) -> None:
        pass

    @abstractmethod
    def call_option(self, pos: tuple):
        pass

    @abstractmethod
    def draw(self, screen: object, x_s: tuple or int, y_s: tuple or int, option_paddings: int = 10):
        pass


class PauseMenu(AbstractMenu):
    def __init__(self, font: object) -> None:
        super().__init__(font)

    # метод принимает текст кнопки, фукнцию, которую должна выполнять кнопка, цвет цекста
    # и добавляет поверхность опции и ее поведение в соответсвуюшие списки
    def append_option(self, option: str, option_callback: object, color: tuple) -> None:
        self.option_surf = self.font.render(option, True, color)
        self.callbacks.append(option_callback)
        self.option_surfaces.append(self.option_surf)
        
        
    # функция принимает текущее положение мышки (нажатой кнопки)
    # находит опцию и вызывает функцию связанную с ней
    def call_option(self, pos: tuple):
        for ind, option in enumerate(self.option_surfaces):
            if self.rects[ind].collidepoint(pos[0], pos[1]) and self.callbacks[ind]:
                self.callbacks[ind]()
    
    # функция отрисовывет опции на экране
    # принимает координату х и стартовую координату y, или кортежи из координат для более аккуратного расставления
    # а так же отступы между пункатми меню, поверзность на которой будет отрисовываться и задний фон
    def draw(self, screen: object, x_s: tuple or int, y_s: tuple or int, option_paddings: int = 10):
        # если переданые координаты - целые числа
        # добавляем кнопки меню сверху вниз по порядку на экран
        if type(x_s) == int:
            for ind, option in enumerate(self.option_surfaces):
                option_rect = option.get_rect(center = (x_s, y_s + (ind * option_paddings)))
                self.rects.append(option_rect)
                screen.blit(option, option_rect)
        # если переданы кортежы координат, то для каждой опции устанавливаем свои координаты
        else:
            for ind, option in enumerate(self.option_surfaces):
                option_rect = option.get_rect(center = (x_s[ind], y_s[ind]))
                self.rects.append(option_rect)
                screen.blit(option, option_rect)




class FinishMenu(AbstractMenu):
    def __init__(self, font: object) -> None:
        super().__init__(font)

    # метод принимает текст кнопки, фукнцию, которую должна выполнять кнопка, цвет цекста
    # и добавляет поверхность опции и ее поведение в соответсвуюшие списки
    def append_option(self, option: str, option_callback: object, color: tuple) -> None:
        self.option_surf = self.font.render(option, True, color)
        self.callbacks.append(option_callback)
        self.option_surfaces.append(self.option_surf)
        
        
    # функция принимает текущее положение мышки (нажатой кнопки)
    # находит опцию и вызывает функцию связанную с ней
    def call_option(self, pos: tuple):
        for ind, option in enumerate(self.option_surfaces):
            if self.rects[ind].collidepoint(pos[0], pos[1]) and self.callbacks[ind]:
                self.callbacks[ind]()
    
    # функция отрисовывет опции на экране
    # принимает координату х и стартовую координату y, или кортежи из координат для более аккуратного расставления
    # а так же отступы между пункатми меню, поверзность на которой будет отрисовываться и задний фон
    # ПРОБЛЕМА ПРИ ОТРИСОВКИ ПОВЕРХНОСТИ!!!
    def draw(self, screen: object, x_s: tuple or int, y_s: tuple or int, option_paddings: int = 10):
        # если переданые координаты - целые числа
        # добавляем кнопки меню сверху вниз по порядку на экран
        if type(x_s) == int:
            for ind, option in enumerate(self.option_surfaces):
                option_rect = option.get_rect(center = (x_s, y_s + (ind * option_paddings)))
                self.rects.append(option_rect)
                screen.blit(option, option_rect)
        # если переданы кортежы координат, то для каждой опции устанавливаем свои координаты
        else:
            for ind, option in enumerate(self.option_surfaces):
                option_rect = option.get_rect(center = (x_s[ind], y_s[ind]))
                self.rects.append(option_rect)
                screen.blit(option, option_rect)

