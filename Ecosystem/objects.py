''''''''''''
import pygame
import random

"""
Intelligence and Empathy haven't been implemented fully yet
"""

# NO means 100% chance of mutation
NO = 0
LOW = 25
MID_LOW = 50
MID_HIGH = 75
HIGH = 100

FIT_COLOR, UNFIT_COLOR = 'green', 'orange'

min_min_res, max_min_res = 2, 8
min_rep_threshold, max_rep_threshold = 1, 5
min_rep_usage, max_rep_usage = 1, 5
min_lifespan, max_lifespan = 5, 180
min_speed, max_speed = 10, 250
min_hunger_incr, max_hunger_incr = 3, 25
min_rad, max_rad = 10, 30

class Unit:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.resource_count = 0
        self.minimum_resources = 4  # ATLEAST THESE RESOURCES ARE REQUIRED TO STAY HEALTHY
        self.group_id = 0
        
        self.replication_theshold = 3  # NEED ATLEAST N RESOURCES TO REPLICATE
        self.replication_cost = 1  # USES ONE RESOURCES WHEN REPLICATES

        self.lifespan = 8
        self.speed = max_speed
        self.resource_compatibility = MID_LOW

        self.empathy = NO # LOW, NO, HIGH
        self.intelligence = LOW # LOW, HIGH

        self.birth_time = pygame.time.get_ticks() // 1000
        self.last_consume_time = pygame.time.get_ticks()
        self.hunger_incr_time = 5
        
        self.wander_direction = self.__change_dir()
        self.target_direction = self.__change_dir()
        self.direction = self.wander_direction

        self.targ_res: Resource = None
        self.__elapsed_time = 0
        self.__mov_delay = self.__change_mov_delay()

        self.radius = 15

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

        self.color = "#000000"
        self.update_color()

    def update_color(self):
        self.color = (
                self.lifespan * 255 // max_lifespan, # R
                self.speed * 255 // max_speed, # G
                self.resource_compatibility * 255 // HIGH # B
            )

    def __change_dir(self): return pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
    def __change_mov_delay(self): return random.uniform(0.2 * 1000, 0.5 * 1000)

    def mutate(self) -> None:
        self.minimum_resources = random.randint(min_min_res, max_min_res)

        self.replication_theshold = random.randint(min_rep_threshold, max_rep_threshold)  # NEED ATLEAST 3 RESOURCES TO REPLICATE
        self.replication_usage = random.randint(min_rep_usage, max_rep_usage)  # USES ONE RESOURCES WHEN REPLICATES

        self.lifespan = random.randint(min_lifespan, max_lifespan)
        self.speed = random.randint(min_speed, max_speed)
        self.resource_compatibility = random.randrange(NO, HIGH + 25, 25)

        self.empathy = random.choice([NO, LOW, HIGH])
        self.intelligence = random.choice([LOW, HIGH])

        self.birth_time = pygame.time.get_ticks() // 1000
        self.hunger_incr_time = random.randint(min_hunger_incr, max_hunger_incr)
        
        self.radius = random.randint(min_rad, max_rad)
        self.group_id += 1

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        self.update_color()

    def replicate(self, units: list["Unit"]) -> None:
        new_unit = Unit(self.x + 100 + self.radius * 2 * random.randint(-1, 1), self.y + 100 + self.radius * 2 * random.randint(-1, 1))
        new_unit.resource_count = self.replication_cost

        new_unit.resource_count = self.replication_cost
        new_unit.minimum_resources = self.minimum_resources

        new_unit.replication_theshold = self.replication_theshold  # NEED ATLEAST N RESOURCES TO REPLICATE
        new_unit.replication_cost = self.replication_cost

        new_unit.lifespan = self.lifespan
        new_unit.speed = self.speed
        new_unit.resource_compatibility = self.resource_compatibility

        new_unit.birth_time = pygame.time.get_ticks() // 1000
        new_unit.last_consume_time = self.last_consume_time
        new_unit.hunger_incr_time = self.hunger_incr_time

        new_unit.intelligence = self.intelligence
        new_unit.empathy = self.empathy
        
        new_unit.radius = self.radius
        new_unit.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)
        new_unit.group_id = self.group_id

        new_unit.color = self.color
        
        self.resource_count -= self.replication_cost

        units.append(new_unit)

    def consume_resource(self, fit: bool) -> None:
        if not fit:
            if self.resource_compatibility == HIGH:
                pass
            elif self.resource_compatibility == NO or random.random() < (HIGH - self.resource_compatibility) * 10e-3:
                self.mutate()
                compat = "high" if self.resource_compatibility == HIGH else "no" if self.resource_compatibility == NO else "some"
                print("A Unit mutated with " + compat + " compatibility with resources")
        self.resource_count += 1
        self.last_consume_time = pygame.time.get_ticks() // 1000

    def ishungry(self) -> bool:
        return self.resource_count < self.minimum_resources

    def update(self, delta: float, WIDTH, HEIGHT, total_resources: int):
        current_time = pygame.time.get_ticks()
        if self.ishungry() and total_resources > 0:
            self.direction = self.target_direction + self.wander_direction * 0.5
        else:
            self.direction = self.wander_direction

        if current_time - self.__elapsed_time > self.__mov_delay:
            self.wander_direction = self.wander_direction.rotate(random.uniform(-45, 45))
            self.__elapsed_time = current_time
            self.__mov_delay = self.__change_mov_delay()

        # EDGE HANDLING
        if self.x < self.radius:
            self.x = self.radius
            self.direction.x *= -1
        elif self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.direction.x *= -1
        if self.y < self.radius:
            self.y = self.radius
            self.direction.y *= -1
        elif self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.direction.y *= -1

        dir_normal = self.direction.normalize()

        self.x += self.speed * dir_normal.x * delta
        self.y += self.speed * dir_normal.y * delta

        self.rect = pygame.Rect(self.x, self.y, self.radius, self.radius)

    def render(self, window: pygame.Surface) -> None:
        pygame.draw.circle(window, "#5F5E5E", (self.x, self.y), self.radius+3)
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

class Resource():
    def __init__(self, pos: tuple, fit: bool = True):
        self.isfit = fit
        self.color = FIT_COLOR if fit else UNFIT_COLOR
        self.width, self.height = 30, 30
        self.x, self.y = pos
        self.rect = [self.x, self.y, self.width, self.height]
    
    def render(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, self.rect, 0)