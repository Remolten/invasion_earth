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

# TODO Should implement id in addComponent and addSystem instead of requiring client to do it themselves

# !!! Note: This class should only be invoked by the simpyl metaclass
# Make a proper Entity object which only stores an id and a list of references to component objects
class _Entity(object):
    def __init__(self, _id, *components):
        # _id should a unique value given by the simpyl metaclass
        self.id = _id
        
        # A container for references to the components
        self.cs = []
        
        # Create a list of components this entity posseses
        for component in components:
            # Also allows direct access to components from an entity object
            self.__dict__[component.id] = component
        
    # Add a variable number of component objects
    def add(self, *components):
        self.cs.extend(components)
        
    # Delete a variable number of components by string
    def rm(self, *componentstrs):
        if self.has(*componentstrs):
            self.cs.remove(component)
            return True
        return False
            
    # Check if the entity has a variable number of components by string
    def has(self, *componentstrs):
        for componentstr in componentstrs:
            for component in self.cs:
                if component.id == componentstr:
                    break
            else:
                return False
            
        return True

# The only requirement of a system class is to implement an id
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg DrawSystem 
class System(object):
    # Ensure there is an initial ID to prevent errors
    # NOTE This is verry bad
    id = None
        
    def process(self):
        # Children must declare a process method to be declared valid
        raise NotImplementedError
    
# The only requirement of a component class is to implement an id
# TODO Component id should be set by parent not child
# Obviously it should be changed from None to an appropriate unique identifier for what it does eg Sprite
class Component(object):
    # Ensure there is an initial ID to prevent errors
    # NOTE next time don't use builtin types as variable names
    id = None

# Inherit from this with the main game class to access the ECS functions
class simpyl(object):
    def __init__(self):
        # Ensure every entity receives a unique id
        self.uid = 0
        
        # Create a container for all of the components and their respective entity ID's
        # This should be sent to the systems for parsing
        # This is the format: {componentTypeStr: {component: owningEntity}}
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
        _id = self.newID()
        
        # Create an actual Entity object
        entity = _Entity(_id, *components)

        # Add components to database
        self.addComponent(entity, *components)
        
        # Add component references to the entity itself
        entity.add(*components)
        
        # Add it to the list of entities
        self.ents.add(entity)
        
        # Return the entity object to be assigned
        return entity
    
    # Systems should be declared as functions in the child of this class
    # However this allows for functions to be modularized and imported from a different file
    def addSystem(self, *systems):
        for system in systems:
            # Ensure we received a valid system object
            assert isinstance(system, System) and system.id is not None, "The addSystem function requires a valid input of instances of the included System class.\nReceived something of the wrong type or with an ID of None"
            # Add it to the set, which will reject duplicates
            self.sys.add(system.id)
            
            # Ensures that the system has not already been added
            assert system.id not in self.__dict__, "Invalid system name. Either received a duplicate system name or the system name clashed with an internal python method. Rename the system.id to something else to fix."
            # Systems can be accessed by self.system in the child of this class if needed
            self.__dict__[system.id] = system
            
            # Give each system access to everything in this class and the child
            system.game = self
            
    # Import all components and add them to the component database
    
    def addComponent(self, entity, *components):
        for component in components:
            # Make sure each object received is a component
            assert isinstance(component, Component) and component.id is not None, "Received an invalid component object. Make sure each component object inherits from the Component class."
            
#            # See if there is a spot for the component already
#            for _component in self.cs.keys():
#                if _component.id == component.id:
#                    break
#            else:
#                #self.cs[component]
            
            # Add the component to the database if it is the correct type
            self.cs[component.id] = {component: entity}
    
    # Removes a variable number of components from the database
    # FUTURE Could resort self.cs just in case the removed component was the last of its type
    def rmComponent(self, *components):
        for component in components:
            # Ensures each argument is a component
            assert isinstance(component, Component) and component.id is not None, "Received an invalid component object. Make sure each component object inherits from the Component class."
            
            # Checks if the component exists and self.cs and checks and removes from the entity as well
            if component in self.cs and list(filter(lambda x: x.id == self.cs[component.id], self.ents))[0].rm(component.id):
                # Removes the component string from the entity itself
                # And also from the main database
                del self.cs[component.id]
            else:
                # Couldn't find the component in the database
                return "Component not found in database or owner entity. Unable to remove."
            
    # Return a dict of all components of the specified componentType
    # TODO Organize the components into sub groups containing only their type
    def getComponents(self, componentType):      
        # Returns a dict of all entities with the specified component type
        # return dict(filter(lambda x: x[0].id == componentType, self.cs.items()))
        
        # Get all components of a certain type in the form {componentType: {component: owningEntity}}
        cs = dict(filter(lambda x: x[0] == componentType, self.cs.items()))
        
        # Only return the internal dict with the actual components
        return list(cs.values())[0]
        # Above works as long as we don't allow user to get multiple componentTypes at once
    
    # Return all entities that contain the specified componentTypes
    def getEntitiesByComponents(self, *componentTypes):
        # Container to return the components
        _ents = []
        
        for entity in self.ents:
            if entity.has(*componentTypes):
                _ents.append(entity)
                
        return _ents
            
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
            # NOTE probably not wise to trust the user to be able to accidentally send args etc
            self.__dict__[sys].process(*args, **kwargs)
    