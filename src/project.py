import pygame
import sys

class Crane:
    def __init__(self, x, min_y, max_y):
        self.x = x
        self.y = min_y
        self.min_y = min_y
        self.max_y = max_y
        self.speed = 4
        self.drop_speed = 6
        self.up_speed = 6
        self.dropping = False
        self.holding = False

def move_left(self):
    if not self.dropping:
        self.x -= self.speed

def move_right(self):
    if not self.dropping:
        self.x += self.speed

def drop(self):
    if not self.dropping:
        self.dropping = True

def update(self, prize):
    if self.dropping:
        self.y += self.drop_speed

        claw_rect = pygame.Rect(self.x - 20, self.y, 40, 20)
        if claw_rect.colliderect(prize.rect) and not self.holding:
            self.holding = True
        
        if self.y >= self.max_y:
            self.dropping = False
    
    else:
        if self.y > self.min_y:
            self.y -= self.up_speed
            if self.holding:
                prize.rect.centerx = self.x
                prize.rect.top = self.y + 20
        else:
            self.y = self.min_y