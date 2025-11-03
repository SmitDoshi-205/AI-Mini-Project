# Game rules, constants, and difficulty configuration

from enum import Enum

SCREEN_W, SCREEN_H = 1100, 700
FPS = 60

GRID_SIZE = 30

# Player/Bot modes
class Mode(Enum):
    PLAYER = 1
    BOT = 2

# Difficulty parameters for bot (easy, medium, hard)
DIFFICULTY = {
    "easy": {
        "view_distance": 90,
        "fire_chance": 0.01,
        "minimax_noise": 35,  
        "path_recalc": 4
    },
    "medium": {
        "view_distance": 150,
        "fire_chance": 0.05,
        "minimax_noise": 25,
        "path_recalc": 3
    },
    "hard": {
        "view_distance": 250,
        "fire_chance": 0.10,
        "minimax_noise": 17,
        "path_recalc": 2.5
    }
}

# Gameplay constants
TANK_RADIUS = 16
BULLET_SPEED = 500
BULLET_RADIUS = 4
FIRE_COOLDOWN = 0.35
RELOAD_TIME = 1.0
MAX_AMMO = 6
MAX_HEALTH = 100
AI_LOW_HEALTH = 32
PARTICLE_COUNT = 18
PARTICLE_LIFETIME = 0.7