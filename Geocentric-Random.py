Web VPython 3.2
from vpython import *
import random
class Planet:
    def toggle_display(self, checkbox):
        self.display = checkbox.checked
        self.obj.clear_trail()
        
    def __init__(self, name, mass, radius, color, pos, vel):
        self.name = name
        self.mass = mass
        self.radius = radius
        self.color = color
        self.pos = pos
        self.vel = vel
        self.obj = sphere(pos=self.pos, radius=self.radius, color=self.color, make_trail=True)
    #    self.obj.trail = curve(color=self.color, radius=self.radius/100, visible=True)
        self.display = True
        self.checkbox = checkbox(bind=self.toggle_display, text=self.name, checked=True)    
    
custom_colora = vector(0.7, 0.4, 0.25)

# Define the planets
sun = Planet('Sun', 1.989e30, 6.96e9, color.yellow, vec(0, 0, 0), vec(0, 0, 0))
mercury = Planet('Mercury', 3.3e23, 2.44e7, color.gray(0.5), vec(0, -5.7e10, 0), vec(4.7e4, 0, 0))
venus = Planet('Venus', 4.87e24, 6.05e7, color.orange, vec(0, -1.1e11, 0), vec(3.5e4, 0, 0))
earth = Planet('Earth', 5.97e24, 6.37e7, color.blue, vec(0, -1.5e11, 0), vec(3e4, 0, 0))
moon = Planet('Moon', 7.342e22, 1.737e7, color.white, earth.pos + vec(0, 3.84e8,0), earth.vel + vec(1022, 0, 0))
mars = Planet('Mars', 6.39e23, 3.39e7, color.red, vec(0, -2.2e11, 0), vec(2.4e4, 0, 0))
jupiter = Planet('Jupiter', 1.898e27, 6.99e8, color.magenta, vec(0, -7.8e11, 0), vec(1.3e4, 0, 0))
saturn = Planet('Saturn', 5.68e26, 5.82e8, custom_colora, vec(0, -1.4e12, 0), vec(9.6e3, 0, 0))
uranus = Planet('Uranus', 8.68e25, 2.54e8, color.cyan, vec(0, -2.8e12, 0), vec(6.8e3, 0, 0))
neptune = Planet('Neptune', 1.02e26, 2.46e8, color.blue, vec(0, -4.5e12, 0), vec(5.4e3, 0, 0))

# Add the planets to a list
planets = [sun, mercury, venus, earth, moon, mars, jupiter, saturn, uranus, neptune]

for planet in planets:
    angle = random.randint(0, 314)
    if planet == moon:
        continue
    planet.pos = vec(mag(planet.pos) * cos(angle), mag(planet.pos) * sin(angle), 0)
    planet.vel = vec(mag(planet.vel) * -sin(angle), mag(planet.vel) * cos(angle), 0)
    planet.obj.clear_trail()
    
angle = random.randint(0, 314)
moon.pos = earth.pos + vec(3.84e8 * cos(angle), 3.84e8 * sin(angle), 0)
moon.vel = earth.vel + vec(1022 * -sin(angle), 1022 * cos(angle), 0)
moon.obj.clear_trail()

# Simulation loop
t = 0
dt = 500
G = 6.67e-11
scene.center = earth.pos
# create a cylinder between Earth and Jupiter
cyl = cylinder(pos=earth.pos, axis=(jupiter.pos - earth.pos), radius=earth.radius, emissive=True)

while True:
    rate(8.64e20)
    
    # Update the position of the cylinder to track the position of the planets
    cyl.pos = earth.pos
    cyl.axis = jupiter.pos - earth.pos

    for planet in planets:
        F_gravity = vec(0, 0, 0)
        for other_planet in planets:
            if other_planet != planet:
                r = other_planet.obj.pos - planet.obj.pos
                r_hat = norm(r)
                F_mag = G * planet.mass * other_planet.mass / mag2(r)
                F_vec = F_mag * r_hat
                F_gravity += F_vec
        planet.vel += F_gravity / planet.mass * dt
    tmpvel = earth.vel
    for planet in planets:
        planet.vel -= tmpvel
        planet.pos += planet.vel * dt
        planet.obj.pos = planet.pos
        # Update display based on checkbox state
        if planet.display:
            planet.obj.visible = True
        else:
            planet.obj.visible = False
    t += dt
