from typing import Any
import pygame
from abc import ABC, abstractstaticmethod

class AbstractItem(ABC, pygame.sprite.Sprite):
    # x - местоположение шарика на экране,
    # filename - путь(имя) файла
    def __init__(self, x, speed, surf, score, group) -> None:
        pygame.sprite.Sprite.__init__(self)
        # изображение
        self.image = surf
        self.image = pygame.transform.scale(self.image, (50, 50))
        # размер и местоположение
        # шарик распологается по координате х всегда сверху окна, т.к. у = 0
        self.rect = self.image.get_rect(center = (x, 0))
        self.speed = speed
        # ценность объекта
        self.score = score
        # добавляет объект в группу
        self.add(group)
    
    # метод который определяет поведение объекта
    @abstractstaticmethod
    def update(self, *args: Any, **kwargs: Any) -> None:   
       pass


class Ball(AbstractItem):
    
    def __init__(self, x, speed, surf, score, group) -> None:
        super().__init__(x, speed, surf, score, group)
    
    # метод который определяет поведение объекта
    def update(self, *args: Any, **kwargs: Any) -> None:   
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        # если объект достигает установленной границы (args[0] - 20)
        else:
            # то он уничтожается
            # удаляется из всех групп
            # self.sub = self.score
            self.kill()


class Buff(AbstractItem):
    def __init__(self, x, speed, surf, score, group) -> None:
        super().__init__(x, speed, surf, score, group)
    
    def update(self, *args: Any, **kwargs: Any) -> None:   
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()

class DeBuff(AbstractItem):
    def __init__(self, x, speed, surf, score, group) -> None:
        super().__init__(x, speed, surf, score, group)
    
    def update(self, *args: Any, **kwargs: Any) -> None:   
        if self.rect.y < args[0] - 20:
            self.rect.y += self.speed
        else:
            self.kill()
    
