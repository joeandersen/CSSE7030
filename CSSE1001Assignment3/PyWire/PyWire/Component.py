"""Defines the general template for a component. All component plug-ins
should inerit from these classes, as they are to ensure (relatively) smooth
operation of PyWire, and graceful error handling."""

from Exceptions import *

class ComponentFactory:
    """The standard set of commands that an component factory is expected to
support."""
    
    def Construct(self, name, args):
        """Construct -> self, string, InterpCmd -> Analysis

Given the arguments args, construct and return a component object named "name".
Pure virtual, and as such throws an exception if undefined."""
        
        raise PURE_VIRTUAL_UNDEFINED, "ComponentFactory.Construct undefined."

    def Summary(self):
        """Summary -> self -> none

Print a summary of the component this factory constructs. Virtual."""


        return "No summary available."

    def Name(self):
        """Name -> self -> none

Print the name / type of the component this factory constructs. Virtual."""

        return "Unknown"

    def NonLinear():

        return False

class Component:

    def __init__(self, name):
        """__init__ -> self, name -> none

Initialises component and sets the name member to supplied value."""
        
        self.Name = name

    def GetName(self):
        """GetName -> self -> string

Return the name string of this component."""

        return self.Name

    def Instance(self, args):
        """Instance -> self, InterpCmd -> string

Construct an instance of this component, which can then be placed into a circuit.
The most importand property of the component."""

        raise PURE_VIRTUAL_UNDEFINED, "Component.Instance undefined."

    def Info(self):
        """Info -> self -> string

Returns string of information about this component. Virtual."""
        
        return "No information available."

    def Type(self):
        """Type -> self -> string

Returns string which contains the actual type of this analysis. Virtual."""
        
        return "unknown type"

    def Configure(self, args):
        """Configure -> self, InterpCmd -> string

Configures this component with the arguements supplied. This is an essential
property, the ability to reconfigure components, and as such is pure virtual."""
        
        raise PURE_VIRTUAL_UNDEFINED, "Component cannot be reconfigured."

    def GetGMatContrib(self, gmat, ivec, instance):
        """Configure -> self, dict, dict, ComponentInstance -> dict, dict

Given the conductance array and current vector, adds this components
contribution to its respective equations, as defined by Kirchoff's laws."""
        
        raise PURE_VIRTUAL_UNDEFINED, "Component cannot be represented in conductance matrix."

class ComponentInstance:
    """The 'parts' in a circuit. represents a component by the nodes its connected to."""

    def __init__(self, name, nodes):
        """__init__ -> self, string, list -> none

Initialises ComponentInstance. Takes a str of the name of the Component this is
an instance of, and a list of nodes this instance is connected to."""

        self.Name = name
        self.Nodes = nodes

    def GetName(self):
        """GetName -> self -> string

Returns the name of the object this nstance instances."""
        
        return self.Name

    def ListNodes(self):
        """GetName -> self -> list

Returns the list of nodes this instance is connected to."""
        

        return self.Nodes
