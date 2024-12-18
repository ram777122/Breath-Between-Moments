import math
import time

# Define initial parameters
n_stars = 50  # Example value for number of stars
m = 0.5 * (n_stars - 1)
t = 0.33333 * n_stars * 0.15
ayo = math.radians(0)  # Initial rotation angle
aye = math.radians(30)  # Example value for rotation
ty0 = 10.0  # Initial translation along y-axis
ty1 = 0.0  # Final translation along y-axis
frames = 100  # Number of frames for the animation

def animate():
    for frame in range(frames):
        # Calculate the current rotation and translation
        progress = frame / frames
        ay = aye * progress
        ty = ty0 + (ty1 - ty0) * progress
        
        # Transformations (example outputs)
        print(f"Frame {frame}:")
        print(f"  Rotate Y: {math.degrees(ay):.2f} degrees")
        print(f"  Translate Y: {ty:.2f}")
        
        # Simulate rendering delay
        time.sleep(0.1)

# Run the animation
animate()
