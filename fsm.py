# Finite State Machine for AI behavior states (Patrol, Attack, Evade)
# This is used by the bot to transition between high-level behaviors.

class FSM:
    def __init__(self):
        self.state = "Patrol"

    def transition(self, visible, health, low_health_thresh):
        # Minimal transitions based on visibility and health
        if health <= low_health_thresh:
            self.state = "Evade"
        elif visible:
            self.state = "Attack"
        else:
            self.state = "Patrol"
        return self.state