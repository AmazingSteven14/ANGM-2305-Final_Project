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


class Prize:
    def __init__(self, x, y):
        self.start_x = x
        self.start_y = y
        self.rect = pygame.Rect(x, y, 40, 40)

        #Movement
        self.speed = 3
        self.direction = 1 # 1 = right, -1 = left

    def update(self, width):
        self.rect.x += self.speed * self.direction

        # Bounce off walls
        if self.rect.right >= width or self.rect.left <= 0:
            self.direction *= -1

    def reset_position(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y



def handle_input(crane):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        crane.move_left()
    if keys[pygame.K_RIGHT]:
        crane.move_right()

def update_game(crane, prize, score, width):
    previous_holding = crane.holding

    # Update crane
    crane.update(prize)

    # Update moving prize (only when not being held)
    if not crane.holding:
        prize.update(width)
    
    # Score when prize is delivered to top
    if previous_holding and not crane.holding and crane.y == crane.min_y:
        score += 1
        prize.reset_position()
    
    return score

def draw_game(screen, crane, prize, score, font):
    screen.fill((255, 255, 255))


    # Draw crane
    pygame.draw.line(screen, (180, 180, 180), (crane.x, crane.y), 4)
    pygame.draw.rect(screen, (220, 50, 50), (crane.x - 20, crane.y, 40, 20))

    # Draw prize
    pygame.draw.rect(screen, (50, 100, 200), prize.rect)

    # Draw score
    score_text = font.render(f"Score:  {score}", True, (0, 0, 0))
    screen.blit(score_text, (20, 20))

    pygame.display.flip()

def draw_end_screen(screen, font, score):
    screen.fill((240, 240, 240))

    title = font.render("Game Over!", True, (0, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (0, 0, 0))
    restart_text = font.render("Press SPACE to play again", True, (80, 80, 80))

    screen.blit(title, (200, 150))
    screen.blit(score_text, (200, 220))
    screen.blit(restart_text, (150, 300))

    pygame.display.flip()