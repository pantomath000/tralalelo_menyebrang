from ursina import *
import random

app = Ursina()

# === Constants ===
START_X = -25
FINISH_X = 25
LANES_X = [-20, -10, 0, 10, 20]  # Car lanes across the road (X axis)
CAR_SPAWN_Z = 60
CAR_DESPAWN_Z = -10

# === Game State ===
cars = []
car_spawn_timer = 0
game_over = False

# === Window ===
window.title = "3D Road Crossing - Final"
window.size = (480, 800)
window.borderless = False
window.fullscreen = False

# === Ground ===
ground = Entity(
    model='plane',
    texture='white_cube',
    texture_scale=(25, 5),
    scale=(50, 1, 10),
    color=color.gray,
    y=0
)

# === Player ===
player = Entity(
    model='cube',
    color=color.orange,
    scale=(1, 2, 1),
    position=(START_X, 1, 0),
    collider='box'
)

# === Camera: Side View ===
camera.position = (0, 5, -20)         # Behind the player on Z axis
camera.rotation_x = 10                # Tilt slightly downward
camera.look_at(player.position + Vec3(0, 0, 5))  # Look forward

# === UI ===
win_text = Text(text='', origin=(0, 0), scale=2, enabled=False)
retry_button = Button(text='Retry', scale=(0.2, 0.1), y=-0.4, enabled=False)

def reset_game():
    global game_over, car_spawn_timer
    player.position = (START_X, 1, 0)
    game_over = False
    car_spawn_timer = 0
    win_text.enabled = False
    retry_button.enabled = False
    for car in cars[:]:
        destroy(car)
    cars.clear()

retry_button.on_click = reset_game

# === Car Entity ===
class Car(Entity):
    def __init__(self, lane_x):
        super().__init__(
            model='cube',
            color=color.red,
            scale=(2, 1, 1.5),
            position=(lane_x, 0.5, CAR_SPAWN_Z),
            collider='box'
        )
        self.speed = random.uniform(0.1, 0.2)

    def update(self):
        self.z -= self.speed
        if self.z < CAR_DESPAWN_Z:
            destroy(self)
            if self in cars:
                cars.remove(self)

# === Spawn Car ===
def spawn_car():
    if game_over:
        return
    lane_x = random.choice(LANES_X)
    car = Car(lane_x=lane_x)
    cars.append(car)

# === Game Update Loop ===
def update():
    global car_spawn_timer, game_over

    if game_over:
        return

    # === Player Movement (Left/Right to cross road) ===
    if held_keys['a']:
        player.x -= 0.1
    if held_keys['d']:
        player.x += 0.1

    # Clamp within road
    player.x = clamp(player.x, START_X, FINISH_X)

    # === Win Condition ===
    if player.x >= FINISH_X:
        win_text.text = "You Win!"
        win_text.enabled = True
        retry_button.enabled = True
        game_over = True
        return

    # === Camera Follows Player Z Position Only (optional) ===
    camera.look_at(player.position + Vec3(0, 0, 5))

    # === Car Spawning ===
    car_spawn_timer += time.dt
    if car_spawn_timer > random.uniform(0.8, 1.5):
        spawn_car()
        car_spawn_timer = 0

    # === Update Cars + Collision ===
    for car in cars[:]:
        if car in scene.entities:
            car.update()
            if car.intersects(player).hit:
                win_text.text = "Game Over!"
                win_text.enabled = True
                retry_button.enabled = True
                game_over = True
                return
        else:
            cars.remove(car)

app.run()
