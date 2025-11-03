# Game entity classes: Tank, Bullet, Particle

import pygame
import math
import random
from settings import MAX_HEALTH, MAX_AMMO, FIRE_COOLDOWN, RELOAD_TIME, TANK_RADIUS, BULLET_RADIUS, BULLET_SPEED, PARTICLE_COUNT, PARTICLE_LIFETIME

Vec2 = pygame.math.Vector2

class Bullet:
    def __init__(self, pos, vel, owner):
        self.pos = Vec2(pos)
        self.vel = Vec2(vel)
        self.owner = owner
        self.radius = BULLET_RADIUS
        self.alive = True
        self.life = 3.5

    def update(self, dt, obstacles):
        self.pos += self.vel * dt
        self.life -= dt
        if self.life <= 0:
            self.alive = False
            return
        rect = pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius*2, self.radius*2)
        for ob in obstacles:
            if rect.colliderect(ob):
                self.alive = False
                return

class Particle:
    def __init__(self, pos):
        self.pos = Vec2(pos)
        angle = random.random()*math.tau
        speed = random.uniform(90,260)
        self.vel = Vec2(math.cos(angle)*speed, math.sin(angle)*speed)
        self.lifetime = PARTICLE_LIFETIME
        self.age = 0
        self.radius = random.randint(2,4)

    def update(self, dt):
        self.age += dt
        self.pos += self.vel * dt
        self.vel *= (1 - min(dt*3, 0.8))
        return self.age < self.lifetime

class Tank:
    def __init__(self, pos, color, name="Tank"):
        self.pos = Vec2(pos)
        self.vel = Vec2(0,0)
        self.angle = 0
        self.turret_angle = 0
        self.radius = TANK_RADIUS
        self.color = color
        self.health = MAX_HEALTH
        self.ammo = MAX_AMMO
        self.fire_timer = 0
        self.reload_timer = 0
        self.speed = 150
        self.name = name

    def can_fire(self):
        return self.fire_timer <= 0 and self.ammo > 0 and self.reload_timer <= 0

    def fire(self, target_pos):
        if not self.can_fire():
            return None
        dirv = (Vec2(target_pos) - self.pos).normalize()
        vel = dirv * BULLET_SPEED
        b = Bullet(self.pos + dirv*(self.radius+6), vel, self)
        self.ammo -= 1
        self.fire_timer = FIRE_COOLDOWN
        if self.ammo <= 0:
            self.reload_timer = RELOAD_TIME
        return b

    def reload(self):
        if self.reload_timer <= 0 and self.ammo < MAX_AMMO:
            self.reload_timer = RELOAD_TIME

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def update_timers(self, dt):
        if self.fire_timer > 0:
            self.fire_timer -= dt
        if self.reload_timer > 0:
            self.reload_timer -= dt
            if self.reload_timer <= 0:
                self.ammo = MAX_AMMO