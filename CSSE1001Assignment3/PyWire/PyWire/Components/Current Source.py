
class CurrentSrcFactory(ComponentFactory):
    """A ideal current source."""

    def __init__(self):

        self.Csct_args = [["-i", ARG_FPN, 1.0]]

    class CurrentSrc(Component):

        def __init__(self, name, current):
            """create a curent source with a given current, and define args we can use to configre the resistor"""
            
            Component.__init__(self, name)
            self.Current = current
            self.Inst_args = [["-na", ARG_STR, "A"],["-nb",ARG_STR, "B"]]

        def Instance(self, args):
            """Create an instance of the current source from the given args"""
            
            Split_args = args.GetArgsWithSwitches(self.Inst_args)
            return ComponentInstance(self.GetName(), (Split_args["-na"], Split_args["-nb"]))

        def Info(self):

            return "Current = " + str(self.Current)

        def Type(self):

            return "Current source"

        def Configure(self, args):
            """Reconfigure the current source with the given args."""
            
            Split_args = args.GetArgsWithSwitches(self.Csct_args)
            self.Current = Split_args["-i"]

        def GetGMatContrib(self, gmat, ivec, instance):
            """return the current sources contribution to the conductance matrix and current vector."""

            Node_a, Node_b = instance.ListNodes()

            # CONTRIBUTION TO CURRENT MATRIX
            #
            #      I
            #   +----
            # A | +I
            # . |
            # . |
            # . |
            # B | -I
            #   |  

            if(Node_a in ivec):
                
                ivec[Node_a] += self.Current

            if(Node_b in ivec):

                ivec[Node_b] -= self.Current

            return gmat, ivec
            

    def Construct(self, name, args):
        """Construct a current source from this factory, using any valid args."""
        
        Def_args = args.GetArgsWithSwitches(self.Csct_args)
        return self.CurrentSrc(name, Def_args["-i"])

    def Summary(self):

        return "Represents an ideal current source."

    def Name(self):

        return "Current Source"

#Register the current source into the global component registry.
GLOBAL.RegisterComponent("CurrentSource", CurrentSrcFactory())
