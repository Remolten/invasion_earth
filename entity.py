# 
# Copyright (C) Tue Jul 19 2016 Remington Thurber 
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

# Components must have unique string ids
# Components are accessed directly eg entity.component

#class Entity(object):
#    def __init__(self, id, *components):
#        self.id = id
#        self.cs = []
#        self.add(*components)
#
#    def add(self, *components):
#        for component in components:
#            self.__dict__[component.id] = component
#            self.cs.append(component.id)
#
#    def rem(self, *components):
#        for component in components:
#            del self.__dict__[component.id]
#            self.cs.remove(component.id) #probably syntax is incorrect
#
#    def has(self, *componentstrs):
#        for componentstr in componentstrs:
#            if not hasattr(self, componentstr):
#                return False
#        return True

# !!! Note: This class should only be invoked by the ecsGame metaclass
# Make a proper Entity object which only stores an id and a list of component strings
class _Entity(object):
    def __init__(self, _id, *components):
        # _id should a unique value given by the ecsGame metaclass
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
            
    # Check if the entity has a variable number of components
    def has(self, *components):
        for component in components:
            if not component in self.cs:
                return False
        return True