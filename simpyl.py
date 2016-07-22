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

# !!! Note: This class should only be invoked by the simpyl metaclass
# Make a proper Entity object which only stores an id and a list of component strings
class _Entity(object):
    def __init__(self, _id, *components):
        # _id should a unique value given by the simpyl metaclass
        self.id = _id
        
        # Create a list of components this entity posseses
        self.cs = [c for c in components]
        
    # Add a variable number of components
    def add(self, *components):
        self.cs.extend(components)
        
    # Delete a variable number of components
    def rm(self, *components):
        if self.has(*components):
            self.cs.remove(component)
            return True
        return False
            
    # Check if the entity has a variable number of components
    def has(self, *components):
        for component in components:
            if not component in self.cs:
                return False
        return True

# The only requirement of a system class is to implement an id
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg DrawSystem 
class System(object):
    # Ensure there is an initial ID to prevent errors
    self.id = None
        
    def process(self):
        # Children must declare a process method to be declared valid
        raise NotImplementedError
    
# The only requirement of a component class is to implement an id
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg Sprite
class Component(object):
    # Ensure there is an initial ID to prevent errors
    self.id = None

# Inherit from this with the main game class to access the ECS functions
class simpyl(object):
    def __init__(self):
        # Ensure every entity receives a unique id
        self.uid = 0
        
        # Create a container for all of the components and their respective entity ID's
        # This should be sent to the systems for parsing
        # This is the format: {component: ownerEntityID}
        self.cs = {}
        
        # Create a container for all of the entities, a set in this case
        # This can be utilized if a specific entity needs to be retrieved eg the player
        self.ents = set()
        
        # Create a container for the ID's of all the systems so they can be called in process
        # Systems are also accessible directly
        self.sys = set()
        
    def newID(self):
        self.uid += 1
        return self.uid
    
    # This function returns an entity object and also adds components to the database
    def Entity(self, *components):
        # Generate the entity's new unique id
        _id = newID()

        # Add components to database and get all the component ids
        _cids = self.addComponents(entityID = _id, *components)

        # Create an actual Entity object
        entity = _Entity(_id, *_cids)
        
        # Add it to the list of entities
        self.ents.add(entity)
        
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
            # Ensure we received a valid system object
            assert isinstance(system, System) and system.id is not None, "The addSystem function requires a valid input of instances of the included System class.\nReceived something of the wrong type or with an ID of None"
            # Add it to the set, which will reject duplicates
            self.sys.add(system.id)
            
            # Ensures that the system has not already been added
            assert system.id not in self.__dict__, "Invalid system name. Either received a duplicate system name or the system name clased with an internal python method. Rename the system.id to something else to fix."
            # Systems can be accessed by self.system in the child of this class if needed
            self.__dict__[system.id] = system
            
            # Give each system access to everything in this class and the child
            system.game = self
            
    # Import all components and add them to the component database
    # Can optionally provide this function with the entity object or just its ID
    def addComponent(self, entity = None, entityID = None, *components):
        _cids = []
        
        for component in components:
            # Make sure each object received is a component
            assert isinstance(component, Component) and component.id is not None, "Received an invalid component object. Make sure each component object inherits from the Component class."
            
            # Add the component to the database if it is the correct type
            if entityID is None:
                self.cs[component] = entity.id
            else:
                self.cs[component] = entityID
                
            _cids.append(component.id)
            
        # Returns a list of strings of the ID's of the components
        return _cids
    
    # Removes a variable number of components from the database
    def rmComponent(self, *components):
        for component in components:
            # Ensures each argument is a component
            assert isinstance(component, Component) and component.id is not None, "Received an invalid component object. Make sure each component object inherits from the Component class.
            
            # Checks if the component exists and self.cs and checks and removes from the entity as well
            if component in self.cs and list(filter(lambda x: x.id == self.cs[component.id], self.ents))[0].rm(component.id):
                # Removes the component string from the entity itself
                # And also from the main database
                del self.cs[component.id]
            else:
                # Couldn't find the component in the database
                return "Component not found in database or owner entity. Unable to remove."
            
    # Run this each loop iteration
    # Runs the process function of all systems
    # Takes any arguments passed and gives them to each system
    def process(self, *args, **kwargs):
        for sys in self.sys:
            # Ensures that each system is actually the proper type
            # Probably redundant, but prevents tampering
            assert sys in self.__dict__, "Invalid system found. Declare a system as a child of the System class and then use addSystem to register it before attempting process()."
            
            # Runs the process function of each system
            # If args are present, each system is responsible to handle them
            self.__dict__[sys].process(*args, **kwargs)
    