import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Decisions")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

branch_length = 50
angle_variation = math.pi / 6
max_depth = 25  # Max depth of the tree, set to 25

def get_new_coordinates(x, y, length, angle):
    new_x = x + length * math.cos(angle)
    new_y = y + length * math.sin(angle) 
    return new_x, new_y

def draw_branch(screen, start_pos, end_pos, color):
    pygame.draw.line(screen, color, start_pos, end_pos, 3)

def draw_tree(screen, node_x, node_y, angle, depth):
    if depth >= max_depth:
        return

    num_choices = random.randint(2, 4)

    angle_step = angle_variation / num_choices

    base_angle = angle - (angle_step * (num_choices - 1)) / 2

    chosen_index = random.randint(0, num_choices - 1)

    for i in range(num_choices):
        current_angle = base_angle + i * angle_step
        next_x, next_y = get_new_coordinates(node_x, node_y, branch_length, current_angle)

        branch_color = RED if i == chosen_index else BLUE
        draw_branch(screen, (node_x, node_y), (next_x, next_y), branch_color)

        if i == chosen_index:
            draw_tree(screen, next_x, next_y, current_angle, depth + 1)

def draw_button(screen, x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    font = pygame.font.SysFont(None, 36)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

def visualize_decision_tree():
    running = True
    tree_drawn = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if the reset button was clicked
                button_x = SCREEN_WIDTH - BUTTON_WIDTH - 20
                button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 20
                if button_x <= mouse_x <= button_x + BUTTON_WIDTH and button_y <= mouse_y <= button_y + BUTTON_HEIGHT:
                    screen.fill(WHITE)
                    tree_drawn = False 

        if not tree_drawn:
            screen.fill(WHITE) 

            start_x = 50
            start_y = SCREEN_HEIGHT // 2  
            initial_angle = 0 

            draw_tree(screen, start_x, start_y, initial_angle, depth=0)

            button_x = SCREEN_WIDTH - BUTTON_WIDTH - 20
            button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 20
            draw_button(screen, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Again")

            tree_drawn = True

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    visualize_decision_tree()
