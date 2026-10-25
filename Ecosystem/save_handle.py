from objects import Unit, Resource
import os
import pygame
import json

appdata_path = os.getenv("APPDATA")
abs_path = os.path.join(appdata_path, "Ecosystem")
os.makedirs(abs_path, exist_ok=True)
units_save_path =  os.path.join(abs_path, 'units.json')
resource_save_path = os.path.join(abs_path, 'resources.json')

X, Y = 'x', 'y'
RES_CNT, MIN_RES = "resource_count", 'minimum_resources'
GROUP_ID = "group_id"
REPL_THRESH = "replication_threshold"
REPL_COST = "replication_cost"
LIFE_SPAN = 'life_span'
SPEED = "speed"
RES_COMP  = "resource_compatibility"
BIRTH = "birth_time"
LAST_CONS = 'last_consume_time'
HUNGER_INCR = 'hunger_incr_time'
RADIUS = "radius"
COLOR = "color"
FIT = 'isfit'
EMPATHY = 'empathy'
INTELLIGENCE = 'intelligence'

def dump_unit(unit: Unit) -> dict:
    u_dct = {}
    u_dct[X], u_dct[Y] = unit.x, unit.y
    u_dct[RES_CNT], u_dct[MIN_RES] = unit.resource_count, unit.minimum_resources
    u_dct[GROUP_ID] = unit.group_id
    u_dct[REPL_THRESH] = unit.replication_theshold
    u_dct[REPL_COST] = unit.replication_cost
    u_dct[LIFE_SPAN] = unit.lifespan
    u_dct[SPEED] = unit.speed
    u_dct[RES_COMP] = unit.resource_compatibility
    u_dct[BIRTH] = unit.birth_time
    u_dct[LAST_CONS] = unit.last_consume_time
    u_dct[HUNGER_INCR] = unit.hunger_incr_time
    u_dct[RADIUS] = unit.radius
    u_dct[COLOR] = unit.color
    u_dct[EMPATHY] = unit.empathy
    u_dct[INTELLIGENCE] = unit.intelligence

    return u_dct

def load_unit(u_dct: dict[str]) -> Unit:
    unit = Unit(u_dct[X], u_dct[Y])
    unit.resource_count, unit.minimum_resources = u_dct[RES_CNT], u_dct[MIN_RES]
    unit.group_id = u_dct[GROUP_ID]
    unit.replication_theshold = u_dct[REPL_THRESH]
    unit.replication_cost = u_dct[REPL_COST]
    unit.lifespan = u_dct[LIFE_SPAN]
    unit.speed = u_dct[SPEED]
    unit.resource_compatibility = u_dct[RES_COMP]
    unit.birth_time = u_dct[BIRTH]
    unit.last_consume_time = u_dct[LAST_CONS]
    unit.hunger_incr_time = u_dct[HUNGER_INCR]
    unit.radius = u_dct[RADIUS]
    unit.color = u_dct[COLOR]
    unit.empathy = u_dct[EMPATHY]
    unit.intelligences = u_dct[INTELLIGENCE]
    unit.rect = pygame.Rect(unit.x, unit.y, unit.radius, unit.radius)

    return unit

def dump_resource(resource: Resource) -> dict:
    d_dct = {}
    d_dct[X], d_dct[Y] = resource.x, resource.y
    d_dct[FIT] = resource.isfit

    return d_dct

def load_resource(d_dct: dict) -> Resource:
    return Resource((d_dct[X], d_dct[Y]), d_dct[FIT])

def save(units: list[Unit], resources: list[Resource]):
    save_unit_list = []
    save_resource_list = []

    for unit in units:
        save_unit_list.append(dump_unit(unit))
    for resource in resources:
        save_resource_list.append(dump_resource(resource))

    with open(units_save_path, 'w') as file:
        file.write(json.dumps(save_unit_list))
    with open(resource_save_path, 'w') as file:
        file.write(json.dumps(save_resource_list))

def load(units: list[Unit], resources: list[Resource]):
    with open(units_save_path, 'r') as file:
        save_unit_list = json.load(file)
    with open(resource_save_path, 'r') as file:
        save_resource_list = json.load(file)
        
    for unit in save_unit_list:
        units.append(load_unit(unit))
    for resource in save_resource_list:
        resources.append(load_resource(resource))

def reset():
    os.remove(resource_save_path)
    os.remove(units_save_path)