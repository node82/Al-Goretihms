import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Life Decisions")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)  # Changed the unchosen branches to blue
BLACK = (0, 0, 0)

# Button settings
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

# Branch settings
branch_length = 50
angle_variation = math.pi / 6  # +/- 30 degrees for branches
max_depth = 25  # Max depth of the tree, set to 25

# Number of starting points (trees)
NUM_TREES = 100

# Function to calculate new coordinates based on an angle
def get_new_coordinates(x, y, length, angle):
    new_x = x + length * math.cos(angle)  # Moving horizontally rightward
    new_y = y + length * math.sin(angle)  # Angle defines up or down movement
    return new_x, new_y

# Function to draw a branch (line)
def draw_branch(screen, start_pos, end_pos, color):
    pygame.draw.line(screen, color, start_pos, end_pos, 3)

# Recursive function to draw the tree
def draw_tree(screen, node_x, node_y, angle, depth):
    if depth >= max_depth:
        return

    # Randomly choose how many branches to create at this point (between 2 and 10)
    num_choices = random.randint(2, 10)

    # Step size for angle between branches
    angle_step = angle_variation / num_choices

    # Base angle for branches, starting at a random spread around the current angle
    base_angle = angle - (angle_step * (num_choices - 1)) / 2

    # Randomly choose one path to continue
    chosen_index = random.randint(0, num_choices - 1)

    for i in range(num_choices):
        # Calculate the angle and position for each branch
        current_angle = base_angle + i * angle_step
        next_x, next_y = get_new_coordinates(node_x, node_y, branch_length, current_angle)

        # Draw the branch (all choices are drawn)
        branch_color = RED if i == chosen_index else BLUE
        draw_branch(screen, (node_x, node_y), (next_x, next_y), branch_color)

        # If this is the chosen path, continue drawing recursively
        if i == chosen_index:
            draw_tree(screen, next_x, next_y, current_angle, depth + 1)

# Function to draw a button on the screen
def draw_button(screen, x, y, width, height, text):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
    font = pygame.font.SysFont(None, 36)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

# Main function to draw the trees and handle the reset button
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
                    screen.fill(WHITE)  # Clear screen when resetting
                    tree_drawn = False  # Reset the trees

        # If the trees haven't been drawn yet, draw the trees
        if not tree_drawn:
            screen.fill(WHITE)  # Fill the background once

            # Starting point (all trees will start from the same x position but with different angles)
            start_x = SCREEN_WIDTH // 2  # Centered horizontally
            start_y = SCREEN_HEIGHT // 2  # Centered vertically

            # Each tree will have a different initial angle
            for i in range(NUM_TREES):
                initial_angle = (i - (NUM_TREES // 2)) * (math.pi / 12)  # Spread the angles for different trees

                # Draw each tree recursively (only once per reset)
                draw_tree(screen, start_x, start_y, initial_angle, depth=0)

            # Draw the reset button
            button_x = SCREEN_WIDTH - BUTTON_WIDTH - 20
            button_y = SCREEN_HEIGHT - BUTTON_HEIGHT - 20
            draw_button(screen, button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT, "Reset")

            tree_drawn = True

        pygame.display.flip()

    pygame.quit()

# Run the visualization
if __name__ == "__main__":
    visualize_decision_tree()
