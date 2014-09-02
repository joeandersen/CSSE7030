"""Defines the general template for an analysis method. All analysis plug-ins
should inerit from these classes, as they are to ensure (relatively) smooth
operation of PyWire, and graceful error handling."""


from Exceptions import *

class AnalysisFactory:
    """The standard set of commands that an analysis factory is expected to
support."""

    def Construct(self, name, args):
        """Construct -> self, string, InterpCmd -> Analysis

Given the arguments args, construct and return an analysis object named "name".
Pure virtual, and as such throws an exception if undefined."""

        raise PURE_VIRTUAL_UNDEFINED, "AnalysisFactory.Construct undefined."

    def Summary(self):
        """Summary -> self -> none

Print a summary of the Analysis this factory constructs. Virtual."""

        return "No summary available."

    def Name(self):
        """Name -> self -> none

Print the name / type of the Analysis this factory constructs. Virtual."""

        return "Unknown"

class Analysis:
    """The actual analysis object, in charge of analysing circuits."""

    
    def __init__(self, name):
        """__init__ -> self, name -> none

Initialises analysis and sets the name member to supplied value."""

        self.Name = name

    def GetName(self):
        """GetName -> self -> string

Return the name string of this analysis."""

        return self.Name

    def Info(self):
        """Info -> self -> string

Returns string of information about this analysis. Virtual."""

        return "No information available."

    def Type(self):
        """Type -> self -> string

Returns string which contains the actual type of this analysis. Virtual."""

        return "unknown type"

    def Configure(self, args):
        """Info -> self, InterpCmd -> string

Configures this analysis with the arguements supplied. This is an essential
property, the ability to reconfigure analuses, and as such is pure virtual."""

        raise PURE_VIRTUAL_UNDEFINED, "Component cannot be reconfigured."

    #[lhs contrib, rhs contrib]
    def Analyse(self, circuit, components, args):
        
        """Analyse -> circuit, components, InterpCmd -> string

Performs this analysis on a circuit, which is constructed of parts from
components. Pure virtual, because this method is essentially why the class
exists."""
        raise PURE_VIRTUAL_UNDEFINED, "Analysis.Analyse undefined."
