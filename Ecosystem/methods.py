from objects import *
from random import randint
import pygame
import save_handle

units: list[Unit] = []

resources, fit_resources, unfit_resources = [], [], []

save_handle.reset()

def save_data():
    save_handle.save(units, resources)
def load_data():
    try:
        save_handle.load(units, resources)
    except FileNotFoundError:
        pass

def add_unit(x: int, y: int):
    units.append(u:=Unit(x, y))
    print(f"Spawned a unit at {u.x}, {u.y}")

def add_resource(x: int, y: int, fit: bool) -> None:
    resources.append(r:=Resource((x, y), fit))
    print(f"Spawned a resource at {r.x}, {r.y}")

def add_resources(scr_width: int, scr_height: int, count: int = 40):
    dummy = Resource((0, 0))
    wid, hei = scr_width - dummy.width, scr_height - dummy.height
    for _ in range(count):
        resources.append(Resource(
            (randint(0, i) for i in [wid, hei]), 
            randint(0, 1)
            )
        )

def unit_death(unit: Unit):
    resources.append(Resource((unit.x + 5, unit.y + 5), not unit.ishungry()))
    units.remove(unit)

def render_objects(window: pygame.Surface):
    for obj in [*units, *resources]:
        obj.render(window)

def update_objects(delta: float, WIDTH, HEIGHT):
    global fit_resources, unfit_resources
    
    fit_resources = [res for res in resources if res.isfit]
    unfit_resources = [res for res in resources if not res.isfit]

    fit_scarcity = len(fit_resources) < 2
    res_scarcity = len(resources) < 2

    targ_resources = resources if fit_scarcity else fit_resources

    if units == []:
        return

    i = 0
    while i < len(units):
        unit = units[i]
        targ_units = [u for u in units if u is not unit]
        dists_from_res = []
        dists_from_unit = []
        current_time = pygame.time.get_ticks() // 1000

        #  REDUCE RESOURCES WITH TIME
        if current_time - unit.last_consume_time > unit.hunger_incr_time:
            unit.resource_count -= 1
            unit.last_consume_time = current_time
            continue
        
        # DEATH
        if current_time - unit.birth_time > unit.lifespan:
            unit_death(unit)
            print("Death because the life span ended")
            continue
        if unit.resource_count < 0:
            unit_death(unit)
            print("Death due to starvation")
            continue

        ## FIND DISTANCES CHOOSE MINIMUM AND SEE WHAT THAT RESOURCE IT AND THEN 
        ## CHANGE UNIT'S DIRECTION TO POINT TO IT
        if unit.ishungry() and resources:
            if unit.targ_res == None:
                for resource in targ_resources:
                    dists_from_res.append((resource.x - unit.x) ** 2 + (resource.y - unit.y) ** 2) # DIST FORMULA

                unit.targ_res = targ_resources[dists_from_res.index(min(dists_from_res))]
                unit.target_direction = pygame.Vector2(unit.targ_res.x, unit.targ_res.y) - pygame.Vector2(unit.x, unit.y)
                
                try:
                    unit.target_direction = unit.target_direction.normalize()
                except ValueError:
                    pass
        elif unit.ishungry() and targ_units:
            ...
            # print("No resources and the unit is hungry af and hell other units roaming free")

        # RES COLLISION
        for resource in targ_resources:
            if unit.rect.colliderect(resource.rect):
                try:
                    resources.remove(resource)
                    unit.consume_resource(resource.isfit)
                except ValueError:
                    pass
            unit.targ_res = None

        # Unit Collision (To be implemented)

        ## REPLICAION
        if unit.resource_count > unit.replication_theshold:
            unit.replicate(units)
            print(f"A unit replicated")

        i += 1
        unit.update(delta, WIDTH, HEIGHT, len(resources))