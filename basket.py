from typing import Any
import pygame

# на основе базового класса Sprite создаем свой класс для корзинки
class Basket(pygame.sprite.Sprite):
    def __init__(self, coord: tuple, speed: int, surf:object, group: object) -> None:
        pygame.sprite.Sprite.__init__(self)
        # изображение
        self.image = pygame.transform.scale(surf, (150, 150))
        # coord - кортеж с координатами для корзинки
        self.rect = self.image.get_rect(center = (coord[0], coord[1]))
        self.speed = speed
        # добавляет объект в группу
        self.add(group)
    
    # метод который определяет поведение объекта
    def update(self, move_right, move_left, W) -> None:
        # move_right - зажатая правая стрелка
        # move_left - зажатая левая стрелка
        # W - ширина экрана для контроля передвижения корзинки
        if move_left:
            self.rect.x += self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        elif move_right:
            self.rect.x -= self.speed
            if self.rect.x > W:
                self.rect.x = W

        