# **ECOSYSTEM**
A tiny ecosystem I was working on, with *UNITS* and *RESOURCES*.

## Units
A unit is spawned and it has the ability to move freely in the 2D plane. If there is a resource, the unit moves towards it if it's hungry and consumes it.

## Resources
Basically, two types of resources can be placed. **Fit** (Represented by Green) and **Unfit** (Represented by Orange). Fit resources can be consumed by the units normally but unfit resources *MAY* cause mutation.

## **Parameters of a Unit**
There are several parameters a unit has that decide its behavior. Like,

`x, y` Coordinates of the unit on the plain. <br>
`resource_count` Total number of resources a unit has acquired. <br>
`minimum_resources` Minimum resources required to stay healthy (not look for more resources)<br>
`group_id` What group does the unit belong to. *Not fully implemented* <br>
`replication_threshold` Minimum resources required to *replicate*. <br>
`replication_cost` Resources used when *replicated*. <br>
`lifespan` Self explanatory. <br>
`speed` Self explanatory. <br>
`resource_compatibility` How compatible the unit is with unfit resources. *(It could be, NO, LOW, MID_LOW, MID_HIGH, HIGH.)* <br>
`empathy` How much the unit is hostile towards others when resources are scarce. *Not implemented* <br>
`intelligence` *Not implemented* <br>
`birth_time` A constant recorded at the time of birth of unit to calculate its lifespan. <br>
`last_consume_time` Tells in seconds, the time the unit cosumed a resource. <br>
`hunger_incr_time` A constant through which unit's hunger increases. i.e the units get consumed. <br>
`direction` Which direction the unit moves. <br>
`targ_res` The resource the unit follows. <br>
`radius` Self explanatory. <br>
`color` Self explanatory. Decided by *lifespan*, *speed* and *resource_compatibilty* of the unit. <br>

## **Processes**
A unit can go through some processes. Like,

### - Replication
A unit replicates when its *resource_count* become greater than its *replication_threshold*. It creates a new copy of itself with same traits. Upon replication a unit's *resource_count* decreases by its *replication_cost*.

### - Mutation
A unit mutates when it consumes an unfit resource and its *resource_compatibility* is not *HIGH*. Some units have more chance to mutate and some never mutate. Upon mutation, most parameters get a new random value. Therefore, units completely change themselves either positively or negatively. A speedy unit may become slow but have a longer lifespan. It is completely random.
**Future of Mutation**: I want to change this approach, and introduce a new number that will be divided amongst the unit's traits. Hence, to some extent reduce the randomness. That is why I have introduced *intelligence* which would eventually decide the ability of a unit to decide which of its traits to increase based on its present state.

### - Death
Death can either occur due to starvation (a unit remains hungry for too long, i.e the resources become 0) or the end of its lifespan. Upon death a unit leaves a fit resource if it had a *resource_count* greater than *minimum_resources*, meaning it was healthy. Otherwise, it leaves an unfit resource.
**Future of Death**: These deaths would remain as they are. But, I want to add one more type of death: Being killed by another unit. A unit, of lower *empathy* can become hostile towards other units if resources are not enough. It would prefer killing over starvation.

## **SET-UP**
First of all, navigate to the folder and open it in terminal. Then run,

```bash
.venv\Scripts\Activate.ps1
```

Make sure you have python installed and then run,
```bash
python main.py
```
Or,
```bash
py main.py
```

There should be a window open now.

## **How to use?**
Following key binds can be used,

`U` Places the default unit in the scene at position of the cursor. <br>
`R` Places an unfit resource in the scene at position of the cursor. <br>
`F` Places a fit resource in the scene at position of the cursor. <br>
`Space` Adds a lot of resources in the scene at random postions.