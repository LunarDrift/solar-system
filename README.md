# The Solar System

Semi-basic representation of our Solar System made using the Arcade library in Python. The math may be off, I'm no astrophysicist. Just some guy trying to learn Python in my spare time. 

#### Current Features
- All 8 Planets and Pluto
- Planet orbital lines around the Sun
- Able to zoom in/out (Inner Planets can get tiny, just goes to show how massive the Solar System is)


#### To-Do (Maybe)
- Move camera view with mouse dragging (gave up on this one for now)
- Add moons
- Asteroids/Comets
- Better Planet images
  
![alt text](https://github.com/LunarDrift/solar-system/blob/main/'/Screenshot%20from%202025-11-13%2019-58-08.png "Example Image")
![alt text](https://github.com/LunarDrift/solar-system/blob/main/'/Peek%202025-11-13%2019-56.gif "Example Gif")

---

#### Planet Data Structure

```
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
```

Each entry is:
`("image_filename", sprite_scale, semi-major axis in AU, relative_speed`
- **Image filename** -> Which sprite to draw
- **Sprite scale** -> Visual size of the planet
- **Semi-major axis** -> Distance from the Sun along the horizontal axis
- **Relative speed** -> Angular speed relative to Earth

--------------------------------------------------------------------

#### Semi-Major Axis

Semi-major axis, `a`, is the main 'horizontal radius' of the orbit. Converted from astronomical units `AU`(distance between Sun and Earth)  to pixels with:

```
a = au * scale_factor
b = a * 0.95  # slight ellipse
```

Where:
 - `au` -> the distance from the Sun in astronomical units
 - `scale_factor` -> variable for how many pixels per AU
 - `b` -> semi-minor axis, slightly smaller than `a` to make an ellipse
	 - Can change what we multiply `a` by. Smaller value = more exaggerated ellipse along x-axis, Larger value = more exaggerated ellipse along y-axis
	 - Negative value will reverse orbit direction to counter-clockwise
	 
Example:
Mars -> 1.52 AU
`a = 1.52 * 100 = 152 pixels`
`b = 152 * 0.95 ≈ 144 pixels`

--------------------------------------------------------------------

#### Angular Speed

The relative speed for each planet is based on their orbital periods.

`speed = base_speed * rel_speed`

Where `base_speed` is an arbitrary value (currently set at 50 degrees/sec)
- Earth's relative speed = 1 -> full orbit takes 7.2 seconds at 50°/sec
- Mercury's relative speed = 4.15 -> faster orbit than Earth since it's closer to Sun
- Jupiter's relative speed = 0.084 -> slower orbit than Earth, further away from Sun

Relative speed is derived from the ratio of Earth's orbital period to that planet's period:
`relative speed = 1 Earth year / Planet orbital period (in Earth years)`

The orbital period of a planet can be calculated using Kepler's Third Law, which states that the square of the orbital period (T) of a planet is directly proportional to the cube of the semi-major axis (a) of its orbit
## $T^2 = a^3$

Where $T$ is the orbital period in Earth years and $a$ is the distance from the Sun in AU. 
For example, if a planet is 2 AU from the Sun, can find its orbital period like:
$T^2 = 2^3$   
$T^2 = 8$  
$T = √8$   
$T = 2.83$ years

Using these two formulas allows us to calculate each planet's orbital speed relative to Earth

| Planet  | Orbital Period (Earth years) | Relative Speed |
| :------ | :--------------------------- | :------------- |
| Mercury | 0.24                         | 4.15×          |
| Venus   | 0.62                         | 1.61×          |
| Earth   | 1.00                         | 1.00×          |
| Mars    | 1.88                         | 0.53×          |
| Jupiter | 11.86                        | 0.084×         |
| Saturn  | 29.46                        | 0.034×         |
| Uranus  | 84.13                        | 0.012x         |
| Neptune | 164.72                       | 0.006x         |
| Pluto   | 248.07                       | 0.004x         |
- Planets with shorter orbital periods move around the Sun **more often -> faster orbit**
- Planets with longer orbital periods move around the Sun **less often -> slower orbit**
##### How angle updates use speed

```
self.angle_deg = (self.angle_deg + self.speed * dt) % 360
```
-  Every frame, each planet adds `planet_speed * time_elapsed` degrees
-  Faster planets accumulate angle faster -> orbit faster
-  Slower planets barely change angle -> orbit slower
- `% 360` keeps the value between 0 and 359

#### Sprite Scale

Sprite scale is mostly visual. Roughly based on planet diameters relative to Earth. Scaling relative to the Sun results in the inner planets being far too small.
