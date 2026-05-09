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
            self.x = max(20, self.x - self.speed)

    def move_right(self):
        if not self.dropping:
            self.x = min(580, self.x + self.speed)

    def drop(self):
        if not self.dropping:
         self.dropping = True

    def update(self, prize):
        # Dropping phase
        if self.dropping:
            self.y += self.drop_speed

        # Collision check MUST be inside the dropping block
            claw_rect = pygame.Rect(self.x - 20, self.y, 40, 20)
            if claw_rect.colliderect(prize.rect) and not self.holding:
                self.holding = True

            # Stop dropping at bottom
            if self.y >= self.max_y:
                self.dropping = False

        # Rising phase
        else:
            if self.y > self.min_y:
                self.y -= self.up_speed
                if self.holding:
                    prize.rect.centerx = self.x
                    prize.rect.top = self.y + 20
            else:
                self.y = self.min_y
                self.holding = False


       


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
        if self.rect.right >= width:
            self.rect.right = width
            self.direction *= -1
        
        if self.rect.left <= 0:
            self.rect.left = 0
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
    pygame.draw.line(screen, (180,180,180), (int(crane.x), 0), (int(crane.x), int(crane.y)), 4)
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



def main():
    pygame.init()
    WIDTH, HEIGHT = 600, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    target_score = 5
    score = 0
    game_over = False


    crane = Crane(WIDTH // 2, min_y=80, max_y=380)
    prize = Prize(260, 380)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                score = 0
                game_over = False
                crane = Crane(WIDTH //2, min_y=80, max_y=350)
                prize = Prize(260, 380)

            if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                crane.drop()

        if not game_over:
            handle_input(crane)
            score = update_game(crane, prize, score, WIDTH)

            if score >= target_score:
                game_over = True
            
            draw_game(screen, crane, prize, score, font)
        else:
            draw_end_screen(screen, font, score)

        clock.tick(60)


if __name__ == "__main__":
    main()