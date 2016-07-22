# 
# Copyright (C) Thu Jul 21 2016 Remington Thurber 
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 

from entity import *
from components import *
from systems import *

# TODO MOVE THESE TO THEIR RESPECTIVE FILES PROBABLY AND UTILIZE LIKE ENTITY IS

# The only requirement of a system class is to implement an id
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg DrawSystem 
class _System(object):
    # Ensure there is an initial ID to prevent errors
    self.id = None
    
    def __init__(self, _id):
        self.id = _id
    
# The only requirement of a component class is to implement an id
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg Sprite
class Component(object):
    # Ensure there is an initial ID to prevent errors
    self.id = None
    
    def __init__(self, _id):
        self.id = _id

# Inherit from this with the main game class to access the ECS functions
class ecsGame(object):
    def __init__(self):
        # Ensure every entity receives a unique id
        self.uid = 0
        
        # Create a container for all of the components and their respective entity ID's
        # This should be sent to the systems for parsing
        # This is the format: {component: ownerEntityID}
        self.cs = {}
        
        # Create a container for all of the entities
        # This can be utilized if a specific entity needs to be retrieved eg the player
        self.ents = []
        
    def newID(self):
        self.uid += 1
        return self.uid
    
    # This function returns an entity object and also adds components to the database
    def Entity(self, *components):
        # Store the component ids
        _cids = []
        
        # Generate the entity's new unique id
        _id = newID()

        # Add components to database and get all the component ids
        for component in components:
            if not isinstance(component, Component) or component.id is None:
                return("The Entity function requires a valid input of instances of the included Component class.\nReceived something of the wrong type or with an ID of None")
            self.cs[component] = _id
            _cids.append(component.id)

        # Create an actual Entity object
        entity = _Entity(_id, *_cids)
        
        # Add it to the list of entities
        self.ents.append(entity)
        
        # Return the entity object to be assigned
        return entity
    
    # Create a new system object and return it to the caller
    # The ID supplied should be a human readable descriptor and does not need to be unique
    def System(self, systemID):
        system = _System()
        return system
    
    # Systems should be declared as functions in the child of this class
    # However this allows for functions to be modularized and imported from a different file
    def addSystem(self, *systems):
        for system in systems:
            if not isinstance(system, System) or system.id is None:
                return("The addSystem function requires a valid input of instances of the included System class.\nReceived something of the wrong type or with an ID of None")
            self.__dict__[system.id] = system
            
    # Components should be declared as functions in the child of this class
    # However this allows for functions to be modularized and imported from a different file
    def addComponent(self, *components):
        for component in components:
            if not isinstance(component, Component) or component.id is None:
                return("The addComponent function requires a valid input of instances of the included Component class.\nReceived something of the wrong type or with an ID of None")
            self.__dict__[component.id] = component
            
    # Run this each loop iteration
    # Checks that each entity's component strings match the database
    # If not, remove the component from the database
    def updateComponents(self):
        pass