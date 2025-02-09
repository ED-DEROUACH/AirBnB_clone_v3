#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

# Ajoutez des objets à votre système de stockage ici
new_state = State(name="New State")
storage.new(new_state)
storage.save()

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

