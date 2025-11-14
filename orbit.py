import math
import arcade
from arcade.math import rotate_point

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
HALF_WIDTH = WINDOW_WIDTH // 2
HALF_HEIGHT = WINDOW_HEIGHT // 2
WINDOW_TITLE = "Solar System"


class RotatingSprite(arcade.Sprite):
    """
    This sprite subclass implements a generic rotate_around_point method.
    """

    def rotate_around_point(self, point, degrees, change_angle=True):
        """
        Rotate the sprite around a point by the set amount of degrees

        You could remove the change_angle keyword and/or angle change
        if you know that sprites will always or never change angle.

        Args:
            point:
                The point that the sprite will rotate about
            degrees:
                How many degrees to rotate the sprite
            change_angle:
                Whether the sprite's angle should also be adjusted.
        """

        # If change_angle is true, change the sprite's angle
        if change_angle:
            self.angle += degrees

        # Move the sprite along a circle centered on the point by degrees
        self.position = rotate_point(
            self.center_x, self.center_y,
            point[0], point[1], degrees)


class Planet(RotatingSprite):
    """
    Planet with elliptical orbit around a center point.
    """

    def __init__(self, texture, scale, orbit_center, a, b, speed):
        super().__init__(texture, scale=scale)

        self.original_scale = scale     # save original scale for zoom in/out
        self.orbit_center = orbit_center  # the point planet orbits around(sun)
        self.a = a  # semi-major axis (horizontal radius)
        self.b = b  # semi-minor axis (vertical radius)
        self.angle_deg = 0  # current pos in orbit expressed in degrees
        self.speed = speed  # angular speed (how fast it moves along its orbit)

        # Initial position at angle 0 (3 o'clock)
        self.center_x = orbit_center[0] + a
        self.center_y = orbit_center[1]


    def update_orbit(self, delta_time, zoom=1.0):
        # To animate planet along ellipse, we use parametric equations
        # Parametric equations
        # x = h + a * cos(θ)
        # y = k + b * sin(θ)

        # Where:
        # (h, k) is the center of ellipse (sun position)
        # θ(theta) is angle in radians
        # cos/sin give smooth circular/elliptical motion
        # a,b scale the motion horizontally/vertically
        
        # Increases angle_deg based on speed and elapsed time(delta_time)
        self.angle_deg = (self.angle_deg + self.speed * delta_time) % 360
        # Convert to radians for cos/sin calculations
        rad = math.radians(self.angle_deg)
        # Update center_x,y to move planet along its ellipse
        self.center_x = self.orbit_center[0] + self.a * zoom * math.cos(rad)
        self.center_y = self.orbit_center[1] + self.b * zoom * math.sin(rad)


class SolarSystem(arcade.View):
    def __init__(self):
        super().__init__()

        # Background
        self.background = arcade.load_texture("planets/bg.jpg")

        # Sun
        self.sun = arcade.Sprite(
            "planets/sun.png",
            scale=1.0,
            center_x=HALF_WIDTH,
            center_y=HALF_HEIGHT,
        )
        self.sun.original_scale = 1.0  # save original scale

        # Save sun position to its own variables
        cx, cy = self.sun.center_x, self.sun.center_y

        # Zoom parameters
        self.zoom = 1.0
        self.min_zoom = 0.07
        self.max_zoom = 2.0

        # Base speed for Earth
        base_speed = 50  # degrees per second for Earth

        # Scaling factor for distances (AU -> pixels)
        scale_factor = 200

        # Planet Data: (filename, sprite scale, semi-major axis in AU, relative speed)
        planet_data = [
            ("mercury.png", 0.033, 0.49, 4.15),
            ("venus.png", 0.095, 0.72, 1.61),
            ("earth.png", 0.075, 1.00, 1.00),
            ("mars.png", 0.060, 1.52, 0.53),
            ("jupiter.png", 0.825, 5.20, 0.084),
            ("saturn.png", 0.675, 9.58, 0.034),
            ("uranus.png", 0.300, 19.2, 0.012),
            ("neptune.png", 0.285, 30.05, 0.006),
            ("pluto.png", 0.085, 39.48, 0.004),
        ]

        # Create planet objects
        self.planets = []
        for name, scale, au, rel_speed in planet_data:
            a = au * scale_factor
            b = a * 0.65   # Gives a smooth ellipse orbit. Make 'b' slightly smaller than 'a' (90-95%) to give a natural look
            speed = base_speed * rel_speed
            self.planets.append(Planet(f"planets/{name}", scale, (cx, cy), a, b, speed))

        # Create sprite list (sun + planets)
        self.sprites = arcade.SpriteList()
        self.sprites.append(self.sun)

        for planet in self.planets:
            planet.update_orbit(0)  # initialize position
            self.sprites.append(planet)


    def on_update(self, dt):
        # Called every frame
        # dt = time since last frame

        for planet in self.planets:
            planet.update_orbit(dt, zoom=self.zoom)
            planet.scale = planet.original_scale * self.zoom

        self.sun.scale = self.sun.original_scale * self.zoom


    def on_draw(self):
        self.clear()    # clear screen each frame
        # Draw background texture
        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
            alpha=100,
        )
        # Draw orbital paths as gray ellipses
        for planet in self.planets:
            arcade.draw_ellipse_outline(
                planet.orbit_center[0],
                planet.orbit_center[1],
                2 * planet.a * self.zoom,
                2 * planet.b * self.zoom,
                arcade.color.DARK_GRAY,
                1,
            )
        # Draw order matters! Draw ellipses first, then planets on top
        self.sprites.draw()
        

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        """Zoom in/out with mouse scroll wheel"""
        self.zoom += scroll_y * 0.1
        self.zoom = max(self.min_zoom, min(self.max_zoom, self.zoom))


def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(
        WINDOW_WIDTH,
        WINDOW_HEIGHT,
        WINDOW_TITLE,
        antialiasing=True,
        center_window=True,
    )
    # Create and setup the View
    view = SolarSystem()
    # Show View on screen
    window.show_view(view)
    # Start the arcade game loop
    arcade.run()


if __name__ == '__main__':
    main()