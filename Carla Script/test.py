import carla
import random

# Connect to the client and retrieve the world object
client = carla.Client('localhost', 3000)
world = client.get_world()

client.load_world('Town05')

# Get the blueprint library and filter for the vehicle blueprints
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')  # get list of vehicles
vehicle_blueprint = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')  # get specific vehicle

# Get the map's spawn points
spawn_points = world.get_map().get_spawn_points()


# spawn ego vehicle
ego_vehicle_loc = random.choice(spawn_points)
ego_vehicle = world.spawn_actor(vehicle_blueprint, ego_vehicle_loc)

# move spec to ego vehicle
spectator = world.get_spectator()
transform = carla.Transform(ego_vehicle.get_transform().transform(carla.Location(x=-10, z=2.5)), ego_vehicle.get_transform().rotation)
spectator.set_transform(transform)

# spawn 50 random vehicles in random spot in the map
for i in range(0, 50):
    world.try_spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))


while True:
    world.tick()
    
    for vehicle in world.get_actors().filter('*vehicle*'):
        vehicle.set_autopilot(True)
