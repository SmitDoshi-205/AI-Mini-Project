Tank Battle Game
An AI-powered Tank Battle Game built using Python (Pygame) where the player competes against an intelligent bot.
The bot uses multiple AI algorithms for decision-making, pathfinding, and behavior simulation — giving it adaptive difficulty levels.
## 🎯Project Overview

This project implements a **Tank Battle Game** that includes:
- **Interactive UI** with Player vs AI Bot setup.  
- **AI Bot** capable of navigating around obstacles, firing intelligently, and adapting difficulty based on player performance.  
- **Three Difficulty Levels**: Easy, Medium, and Hard.  
- **Three AI Algorithms** for smart bot control:
  - **A\*** – Pathfinding around obstacles.  
  - **Finite State Machine (FSM)** – Managing bot behavior states.  
  - **Minimax** – Decision-making during combat situations.
## 🧩 Project Structure

TANK BATTLE/
│
├── ai_bot.py # Core AI Bot logic - integrates A*, FSM, and Minimax
├── astar.py # A* pathfinding algorithm (used for movement planning)
├── entities.py # Player, Bot, and Bullet classes (tank behavior)
├── fsm.py # Finite State Machine for bot states (chase, idle, attack)
├── main.py # Main game loop and entry point (executed to run the game)
├── map.py # Map and obstacle generation + grid system
├── minimax.py # Minimax algorithm with heuristics for shooting logic
├── settings.py # Game settings, difficulty levels, constants (e.g. speed, fire rate)
└── pycache/ # Auto-generated compiled Python cache files

## 🧮 Algorithms Used

### 1️⃣ A* (A-Star Pathfinding)
**File:** `astar.py`  
**Purpose:** Finds the shortest path from the bot to the player while avoiding obstacles.  
**Logic:** Calculates the best route based on **distance cost (g)** and **heuristic cost (h)**, minimizing total cost **f = g + h**.  
**Usage:** The bot uses this algorithm to move intelligently around barriers toward the player.

---

### 2️⃣ Finite State Machine (FSM)
**File:** `fsm.py`  
**Purpose:** Controls the bot’s behavior based on the situation.  
**States:**
- **Search:** When player is not visible.  
- **Chase:** When player is visible.  
- **Attack:** When player is in range.  
**Logic:** The FSM allows the bot to switch states dynamically — e.g., start chasing when it detects the player, or attack when in range.

---

### 3️⃣ Minimax Algorithm
**File:** `minimax.py`  
**Purpose:** Helps the bot make intelligent firing decisions (attack or defend).  
**Logic:** Evaluates all possible actions, predicts the player’s response, and chooses the move that maximizes its advantage and minimizes risk.  
**Usage:** The bot determines when and where to shoot.

---

## 🎮 Game Difficulty

Defined in `settings.py`:

| Mode   | View Distance  | Fire Chance  | Minimax Noise   | Path Recalc Delay  | Behavior Description |
|--------|----------------|--------------|-----------------|--------------------|----------------------|
| Easy   | 90  px         | 0.01         | 35              |4s                  | Slow movement, long aiming delay, fires rarely |
| Medium | 150 px         | 0.05         | 25              |3s                  | Balanced difficulty, moderate speed |
| Hard   | 250 px         | 0.10         | 17              |2.5s                | Fast reaction, accurate aim, fires aggressively |

🕹️ Controls
Action	Key
Move    Up	W
Move    Down	S
Move    Left	A
Move    Right	D
Fire	  Spacebar
Quit    Game	Esc
