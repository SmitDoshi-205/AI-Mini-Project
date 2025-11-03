import pygame
import sys
import math
import random
from settings import SCREEN_W, SCREEN_H, FPS, DIFFICULTY
from entities import Tank, Bullet, Particle
from map import generate_random_obstacles, rects_to_grid
from ai_bot import AITankController
from settings import Mode
from settings import TANK_RADIUS, MAX_HEALTH, MAX_AMMO
from settings import BULLET_SPEED
from entities import Bullet as BulletClass

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)
bigfont = pygame.font.SysFont("consolas", 28, bold=True)

def choose_difficulty_pygame(screen, font):
    options = ["easy", "medium", "hard"]
    selected = 0
    while True:
        screen.fill((10, 15, 25))
        title = font.render("Select Bot Difficulty", True, (220, 220, 220))
        screen.blit(title, (SCREEN_W//2 - title.get_width()//2, 180))

        for i, opt in enumerate(options):
            color = (255, 200, 50) if i == selected else (180, 180, 180)
            txt = font.render(opt.capitalize(), True, color)
            screen.blit(txt, (SCREEN_W//2 - txt.get_width()//2, 250 + i * 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return options[selected]

        pygame.display.flip()
        clock.tick(30)

def draw_hud(player, ai, score, time):
    pygame.draw.rect(screen, (20,20,26,180), (10, SCREEN_H-78, SCREEN_W-20, 68))
    ntext = bigfont.render(f"{player.name}", True, (220,220,220))
    screen.blit(ntext, (24, SCREEN_H-74+6))
    hp_txt = font.render(f"HP: {int(player.health)}", True, (230,230,230))
    screen.blit(hp_txt, (24, SCREEN_H-36))
    ammo_txt = font.render(f"Ammo: {int(player.ammo)}/{MAX_AMMO}  [R to reload]", True, (230,230,230))
    screen.blit(ammo_txt, (150, SCREEN_H-36))
    st = font.render(f"Score - You: {score['player']}  AI: {score['ai']}", True, (220,220,220))
    screen.blit(st, (SCREEN_W-320, SCREEN_H-74+8))
    tt = font.render(f"Time: {int(time)}s", True, (180,180,180))
    screen.blit(tt, (SCREEN_W-320, SCREEN_H-36))

def spawn_explosion(pos, particles):
    for _ in range(10):
        particles.append(Particle(pos))

def main():
    # Difficulty selection at startup 
    difficulty = choose_difficulty_pygame(screen, bigfont)
    dcfg = DIFFICULTY[difficulty]

    # generate map and grid, clear spawn areas
    obstacles = generate_random_obstacles(seed=42, ratio=0.028)
    obstacles = [o for o in obstacles if not o.colliderect(pygame.Rect(60, SCREEN_H//2-90, 160, 180))]
    obstacles = [o for o in obstacles if not o.colliderect(pygame.Rect(SCREEN_W-220, SCREEN_H//2-90, 160, 180))]
    grid = rects_to_grid(obstacles)

    player = Tank((120, SCREEN_H//2), (40,180,99), name="Player")
    ai_tank = Tank((SCREEN_W-120, SCREEN_H//2), (200,60,60), name="AI Bot")

    ai_controller = AITankController(ai_tank, grid, obstacles, dcfg)

    bullets = []
    particles = []
    score = {"player":0, "ai":0}
    time_total = 0

    debug = False
    show_minimap = True

    while True:
        dt = clock.tick(FPS)/1000.0
        time_total += dt
        # Input & events (player control)
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mv = pygame.math.Vector2(0,0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            mv.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            mv.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            mv.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            mv.x += 1
        if mv.length_squared() > 0:
            mv = mv.normalize() * player.speed
        player.vel = mv
        player.turret_angle = math.atan2(mouse_pos[1] - player.pos.y, mouse_pos[0] - player.pos.x)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif ev.key == pygame.K_SPACE:
                    b = player.fire(mouse_pos)
                    if b:
                        bullets.append(b)
                elif ev.key == pygame.K_r:
                    player.reload()
                elif ev.key == pygame.K_TAB:
                    debug = not debug
                elif ev.key == pygame.K_m:
                    show_minimap = not show_minimap
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    b = player.fire(mouse_pos)
                    if b: bullets.append(b)

        # Update timers & AI
        player.update_timers(dt)
        ai_tank.update_timers(dt)
        ai_controller.update(player, dt, time_total)

        # AI fire logic (uses difficulty fire chance)
        if ai_controller.visible_player(player) and ai_tank.can_fire():
            dist = (player.pos - ai_tank.pos).length()
            p_fire = min(1.0, max(0.1, dcfg["fire_chance"] - dist/800.0))
            if random.random() < p_fire:
                b = ai_tank.fire(player.pos)
                if b: bullets.append(b)

        # Move player with collision avoidance (simple)
        new_pos = player.pos + player.vel * dt
        prect = pygame.Rect(new_pos.x - player.radius, new_pos.y - player.radius, player.radius*2, player.radius*2)
        blocked = False
        for ob in obstacles:
            if prect.colliderect(ob):
                blocked = True
                break
        if not blocked:
            player.pos = new_pos
        else:
            tmp = pygame.math.Vector2(player.pos.x + player.vel.x*dt, player.pos.y)
            rtmp = pygame.Rect(tmp.x - player.radius, tmp.y - player.radius, player.radius*2, player.radius*2)
            if not any(rtmp.colliderect(o) for o in obstacles):
                player.pos = tmp
            else:
                tmp2 = pygame.math.Vector2(player.pos.x, player.pos.y + player.vel.y*dt)
                rtmp2 = pygame.Rect(tmp2.x - player.radius, tmp2.y - player.radius, player.radius*2, player.radius*2)
                if not any(rtmp2.colliderect(o) for o in obstacles):
                    player.pos = tmp2

        # AI movement collision handling (simple)
        aipnew = ai_tank.pos + ai_tank.vel * dt
        airect = pygame.Rect(aipnew.x - ai_tank.radius, aipnew.y - ai_tank.radius, ai_tank.radius*2, ai_tank.radius*2)
        if not any(airect.colliderect(o) for o in obstacles):
            ai_tank.pos = aipnew
        else:
            ai_tank.path = []
            ai_tank.vel = pygame.math.Vector2(0,0)

        # Update bullets
        for b in bullets:
            b.update(dt, obstacles)
            if b.alive and b.owner is not player:
                if (b.pos - player.pos).length() <= player.radius + b.radius:
                    player.take_damage(16)
                    b.alive = False
                    spawn_explosion(b.pos, particles)
            if b.alive and b.owner is not ai_tank:
                if (b.pos - ai_tank.pos).length() <= ai_tank.radius + b.radius:
                    ai_tank.take_damage(18)
                    b.alive = False
                    spawn_explosion(b.pos, particles)
        bullets = [b for b in bullets if b.alive]

        # particles
        new_parts = []
        for p in particles:
            if p.update(dt):
                new_parts.append(p)
        particles = new_parts

        # Reset round on death
        if player.health <= 0 or ai_tank.health <= 0:
            if player.health <= 0:
                score["ai"] += 1
            if ai_tank.health <= 0:
                score["player"] += 1
            player.health = MAX_HEALTH; player.ammo = MAX_AMMO; player.pos = pygame.math.Vector2(120, SCREEN_H//2)
            ai_tank.health = MAX_HEALTH; ai_tank.ammo = MAX_AMMO; ai_tank.pos = pygame.math.Vector2(SCREEN_W-120, SCREEN_H//2)
            bullets.clear(); particles.clear()

        # DRAW
        screen.fill((14,20,30))
        for ob in obstacles:
            pygame.draw.rect(screen, (80,80,80), ob)
        for b in bullets:
            pygame.draw.circle(screen, (250,220,60), (int(b.pos.x), int(b.pos.y)), b.radius)
        for p in particles:
            pygame.draw.circle(screen, (255, 160, 50), (int(p.pos.x), int(p.pos.y)), p.radius)
        pygame.draw.circle(screen, player.color, (int(player.pos.x), int(player.pos.y)), player.radius)
        turret_end = player.pos + pygame.math.Vector2(math.cos(player.turret_angle), math.sin(player.turret_angle))*(player.radius+10)
        pygame.draw.line(screen, (30,30,30), (int(player.pos.x), int(player.pos.y)), (int(turret_end.x), int(turret_end.y)), 6)
        pygame.draw.circle(screen, ai_tank.color, (int(ai_tank.pos.x), int(ai_tank.pos.y)), ai_tank.radius)
        turret_end2 = ai_tank.pos + pygame.math.Vector2(math.cos(ai_tank.turret_angle), math.sin(ai_tank.turret_angle))*(ai_tank.radius+10)
        pygame.draw.line(screen, (30,30,30), (int(ai_tank.pos.x), int(ai_tank.pos.y)), (int(turret_end2.x), int(turret_end2.y)), 6)

        draw_hud(player, ai_tank, score, time_total)

        pygame.display.flip()

if __name__ == "__main__":
    main()
