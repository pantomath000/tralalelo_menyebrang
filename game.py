from ursina import *
from multiprocessing import Process, Manager
from gesture_worker import run_gesture_recognizer
import time
import random
import zipfile
import os

app = Ursina()

# Game constants
START_X = -25
FINISH_X = 25
CAR_LANES_X = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
CAR_SPAWN_Z = 60
CAR_DESPAWN_Z = -10

cars = []
car_spawn_timer = 0
game_over = False
last_valid_gesture = 'Stop'
game_start_time = time.time()
difficulty_multiplier = 1.0

# Shared gesture
manager = Manager()
shared_gesture = manager.Value('u', 'Stop')

# Start gesture recognizer process
gesture_process = Process(target=run_gesture_recognizer, args=(shared_gesture,))
gesture_process.start()

# Unzip character assets if not already done
asset_folder = 'assets/character/'
if not os.path.exists(asset_folder):
    os.makedirs(asset_folder)
    with zipfile.ZipFile('assets/character.zip', 'r') as zip_ref:
        zip_ref.extractall(asset_folder)

# Load character model and texture
player = Entity(
    model=f'{asset_folder}scene.gltf', 
    texture=f'{asset_folder}Material.001_baseColor.png',
    scale=(0.2, 0.2, 0.2),  # Adjusted size
    position=(START_X, 0, 0),  # Ensure character is on the ground
    collider='box'  # Use box collider for collision detection
)

# Adjusting the collider to match the character size
player.collider = BoxCollider(player, center=(0, 0, 0), size=(10, 10, 10))

# Scene setup
ground = Entity(model='plane', texture='white_cube', texture_scale=(25, 5),
                scale=(50, 1, 10), color=color.gray, y=0)

camera.position = (0, 5, -20)
camera.rotation_x = 10
camera.look_at(player.position + Vec3(0, 0, 5))

# Lane Lines (visuals)
lane_lines = []
for x in CAR_LANES_X:
    line = Entity(model='cube', scale=(0.2, 0.01, 60),
                  color=color.white33, position=(x, 0.01, 25))
    lane_lines.append(line)

# UI Elements
win_text = Text(text='', origin=(0, 0), scale=2, enabled=False)
retry_button = Button(text='Retry', scale=(0.2, 0.1), y=-0.4, enabled=False)
gesture_display = Text(text='', position=window.top_left + Vec2(0.02, -0.05), scale=1.5)

def reset_game():
    global game_over, car_spawn_timer, last_valid_gesture, game_start_time, difficulty_multiplier
    player.position = (START_X, 0, 0)
    player.scale = (0.2, 0.2, 0.2)
    game_over = False
    car_spawn_timer = 0
    last_valid_gesture = 'Stop'
    game_start_time = time.time()
    difficulty_multiplier = 1.0
    win_text.enabled = False
    retry_button.enabled = False
    for car in cars[:]:
        destroy(car)
    cars.clear()

retry_button.on_click = reset_game

# Car class using the .glb model for cars
class Car(Entity):
    def __init__(self, x_lane, speed):
        super().__init__(
            model='assets/airport_car.glb',  # Use the .glb car model
            scale=(2, 1, 1.5),  # Adjust car size if needed
            position=(x_lane, 0.5, CAR_SPAWN_Z), 
            collider='box'  # Add collider to cars
        )
        self.speed = speed

    def update(self):
        self.z -= self.speed
        if self.z < CAR_DESPAWN_Z:
            destroy(self)
            if self in cars:
                cars.remove(self)

def spawn_car():
    if game_over:
        return
    x_lane = random.choice(CAR_LANES_X)
    base_speed = random.uniform(0.1, 0.2)
    speed = base_speed * difficulty_multiplier
    car = Car(x_lane, speed)
    cars.append(car)

def update():
    global car_spawn_timer, game_over, last_valid_gesture, difficulty_multiplier

    if game_over:
        return

    # Difficulty scales over time
    elapsed = time.time() - game_start_time
    difficulty_multiplier = 1 + min(elapsed / 30, 2)  # Caps at 3x after 60 seconds

    # Read gesture input
    gesture = shared_gesture.value
    if gesture not in ["Move Forward", "Move Backward", "Stop"]:
        gesture = last_valid_gesture
    else:
        last_valid_gesture = gesture

    # Apply gesture-based movement
    if gesture == "Move Forward":
        player.x += 0.1
        # Face right (positive x-direction relative to camera)
        player.rotation_y = 270  # Fixed direction for moving forward
    elif gesture == "Move Backward":
        player.x -= 0.1
        # Face left (negative x-direction relative to camera)
        player.rotation_y = 90  # Fixed direction for moving backward

    # If the character is stopped, face directly at the camera
    if gesture == "Stop":
        player.rotation_y = camera.rotation_y  # Face the camera

    player.x = clamp(player.x, START_X, FINISH_X)
    gesture_display.text = f"Gesture: {gesture}"

    # Win condition
    if player.x >= FINISH_X:
        win_text.text = "You Win!"
        win_text.enabled = True
        retry_button.enabled = True
        game_over = True
        return

    camera.look_at(player.position + Vec3(0, 0, 5))

    # Car spawn logic
    car_spawn_timer += time.dt
    if car_spawn_timer > random.uniform(0.8, 1.5):
        spawn_car()
        car_spawn_timer = 0

    # Update and check for collisions with cars
    for car in cars[:]:
        if car in scene.entities:
            car.update()
            if car.intersects(player).hit:
                player.scale = (0.2, 0.05, 0.2)  # Make the character flat
                player.position = (player.x, -0.1, player.z)
                win_text.text = "Game Over!"
                win_text.enabled = True
                retry_button.enabled = True
                game_over = True
                return
        else:
            cars.remove(car)

def on_exit():
    print("Shutting down...")
    gesture_process.terminate()

app.run()
on_exit()
