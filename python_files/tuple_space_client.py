import Pyro4

# Connect to the Pyro4 daemon
tuple_space = Pyro4.Proxy("PYRO:example.tuple_space@localhost:9090")

# Write some tuples
tuple_id1 = tuple_space.write(["INE1418", "Fulano", 8.5, 80])
tuple_id2 = tuple_space.write(["INE1419", "Beltrano", 7.0, 75])
print(f"Written tuples with IDs: {tuple_id1}, {tuple_id2}")

# Read a tuple
result = tuple_space.read(["*", "Fulano", "*", "*"])
print(f"Read tuple: {result}")

# Get a tuple
result = tuple_space.get(["*", "Beltrano", "*", "*"])
print(f"Got tuple: {result}")
