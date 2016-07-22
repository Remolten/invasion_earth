from entity import *
from components import *
from systems import *

# Inherit from this with the main game class to access the ECS functions
class ecsGame():
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
    def Entity(*components):
        # Store the component ids
        _cids = []
        
        # Generate the entity's new unique id
        _id = newID()

        # Add components to database and get all the component ids
        for component in components:
            self.cs[component] = _id
            _cids.append(component.id)

        # Create an actual Entity object
        entity = _Entity(_id, *_cids)
        
        # Add it to the list of entities
        self.ents.append(entity)
        
        # Return the entity object to be assigned
        return entity