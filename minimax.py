import random

def evaluate_action(action, bot_health, player_health, bot_ammo, player_ammo, distance, noise=0):
    score = 0
    if action == "attack":
        score += max(0, 150 - distance)
        score += (bot_health - player_health) * 0.6
        score += (bot_ammo - player_ammo) * 4
    elif action == "evade":
        score += (100 - bot_health) * 1.5
        score += max(0, distance - 120)
    elif action == "seek_ammo":
        score += (6 - bot_ammo) * 6
        score += max(0, 200 - distance)
    score += random.uniform(-noise, noise)
    return score

def choose_best_action(bot_health, player_health, bot_ammo, player_ammo, distance, noise=6):
    actions = ["attack", "evade", "seek_ammo", "patrol"]
    best = None
    best_score = -1e9
    for a in actions:
        sc = evaluate_action(a, bot_health, player_health, bot_ammo, player_ammo, distance, noise)
        if sc > best_score:
            best_score = sc
            best = a
    return best