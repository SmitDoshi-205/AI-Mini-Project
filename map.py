# Map generation and grid conversion for pathfinding
import random
import pygame
from settings import GRID_SIZE, SCREEN_W, SCREEN_H

def generate_random_obstacles(seed=None, ratio=0.028):
    if seed:
        random.seed(seed)
    obstacles = []
    cols = SCREEN_W // GRID_SIZE
    rows = SCREEN_H // GRID_SIZE

    # Random scattered small obstacles
    for r in range(rows):
        for c in range(cols):
            if random.random() < ratio:
                rect = pygame.Rect(c*GRID_SIZE, r*GRID_SIZE, GRID_SIZE, GRID_SIZE)
                obstacles.append(rect)

    # Random large obstacles
    for _ in range(6):
        w = random.randint(2,6) * GRID_SIZE
        h = random.randint(2,5) * GRID_SIZE
        x = random.randint(1, cols - (w//GRID_SIZE) - 2) * GRID_SIZE
        y = random.randint(1, rows - (h//GRID_SIZE) - 2) * GRID_SIZE
        obstacles.append(pygame.Rect(x, y, w, h))
    return obstacles


def rects_to_grid(obstacles):
    cols = SCREEN_W // GRID_SIZE
    rows = SCREEN_H // GRID_SIZE
    grid = [[0]*cols for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            tile = pygame.Rect(c*GRID_SIZE, r*GRID_SIZE, GRID_SIZE, GRID_SIZE)
            for ob in obstacles:
                if tile.colliderect(ob):
                    grid[r][c] = 1
                    break
    return grid


def world_to_grid(pos):
    # Clamp to screen bounds
    x = max(0, min(SCREEN_W - 1, pos.x))
    y = max(0, min(SCREEN_H - 1, pos.y))
    return (int(x // GRID_SIZE), int(y // GRID_SIZE))


def grid_to_world(cell):
    cx, cy = cell
    # Clamp cell values to valid grid indices
    cols = SCREEN_W // GRID_SIZE
    rows = SCREEN_H // GRID_SIZE
    cx = max(0, min(cols - 1, cx))
    cy = max(0, min(rows - 1, cy))
    return pygame.math.Vector2(cx * GRID_SIZE + GRID_SIZE / 2, cy * GRID_SIZE + GRID_SIZE / 2)


def clamp_position(pos):
    pos.x = max(0, min(SCREEN_W - GRID_SIZE, pos.x))
    pos.y = max(0, min(SCREEN_H - GRID_SIZE, pos.y))
    return pos