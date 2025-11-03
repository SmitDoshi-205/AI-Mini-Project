# AI controller that wires FSM, A*, and Minimax together.

import math
import pygame
import random
from fsm import FSM           # FSM algorithm usage
from astar import a_star     # A* algorithm usage
from minimax import choose_best_action  # Minimax-style decision usage
from map import world_to_grid, grid_to_world

class AITankController:
    def __init__(self, tank, grid, obstacles, difficulty_cfg):
        self.tank = tank
        self.grid = grid
        self.obstacles = obstacles
        self.fsm = FSM()
        self.path = []
        self.path_target = None
        self.patrol_timer = 0
        self.last_decision = 0
        self.dcfg = difficulty_cfg

    def visible_player(self, player):
        to_player = player.pos - self.tank.pos
        if to_player.length_squared() > self.dcfg["view_distance"]**2:
            return False
        steps = int(to_player.length() // (15)) + 1
        for i in range(1, steps+1):
            p = self.tank.pos + to_player * (i/steps)
            pr = pygame.Rect(p.x-2, p.y-2, 4, 4)
            for ob in self.obstacles:
                if pr.colliderect(ob):
                    return False
        return True

    def compute_grid_path_to(self, world_target):
        start = world_to_grid(self.tank.pos)
        goal = world_to_grid(world_target)
        cells = a_star(self.grid, start, goal)
        if not cells:
            return []
        return [grid_to_world(c) for c in cells]

    def pick_patrol_target(self):
        cols = len(self.grid[0])
        rows = len(self.grid)
        for _ in range(25):
            gx = random.randint(2, cols-3)
            gy = random.randint(2, rows-3)
            if self.grid[gy][gx] == 0:
                return grid_to_world((gx,gy))
        return self.tank.pos + pygame.math.Vector2(random.uniform(-150,150), random.uniform(-150,150))

    def follow_path(self, dt):
        if not self.path:
            return
        target = self.path[0]
        to_target = target - self.tank.pos
        if to_target.length() < 8:
            self.path.pop(0)
            return
        desired = to_target.normalize() * self.tank.speed
        self.tank.vel = desired
        self.tank.pos += self.tank.vel * dt

    def update(self, player, dt, time):
        visible = self.visible_player(player)
        state = self.fsm.transition(visible, self.tank.health, 32)

        if time - self.last_decision > self.dcfg["path_recalc"]:
            self.last_decision = time
            dist = (player.pos - self.tank.pos).length()
            action = choose_best_action(self.tank.health, player.health, self.tank.ammo, player.ammo, dist, noise=self.dcfg["minimax_noise"])
            if action == "attack":
                self.path = self.compute_grid_path_to(player.pos)
                state = "Attack"
            elif action == "evade":
                away = (self.tank.pos - player.pos).normalize()
                target = self.tank.pos + away * 220
                self.path = self.compute_grid_path_to(target)
                state = "Evade"
            elif action == "seek_ammo":
                self.path = self.compute_grid_path_to(self.pick_patrol_target())
                state = "Patrol"
            else:
                self.path = self.compute_grid_path_to(self.pick_patrol_target())
                state = "Patrol"

        # state behaviors
        if state == "Patrol":
            self.patrol_timer += dt
            if (not self.path) or self.patrol_timer > 2.5:
                self.path = self.compute_grid_path_to(self.pick_patrol_target())
                self.patrol_timer = 0
            self.follow_path(dt)
            self.tank.turret_angle += 0.02
        elif state == "Attack":
            if time % 1.0 < 0.6:
                self.path = self.compute_grid_path_to(player.pos)
            self.follow_path(dt)
            self.tank.turret_angle = math.atan2(player.pos.y - self.tank.pos.y, player.pos.x - self.tank.pos.x)
        elif state == "Evade":
            if not self.path:
                away = (self.tank.pos - player.pos).normalize()
                self.path = self.compute_grid_path_to(self.tank.pos + away*220)
            self.follow_path(dt)
            self.tank.turret_angle = math.atan2(player.pos.y - self.tank.pos.y, player.pos.x - self.tank.pos.x)