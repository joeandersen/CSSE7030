
class ResistorFactory(ComponentFactory):
    """A Basic resistor."""

    def __init__(self):
        
        self.Csct_args = [["-r", ARG_FPN, 1.0]]

    class Resistor(Component):

        def __init__(self, name, resistance):
            """create a resistor with a given resistance, and define args we can use to configre the resistor"""

            Component.__init__(self, name)
            self.Resistance = resistance
            self.Inst_args = [["-na", ARG_STR, "A"],["-nb",ARG_STR, "B"]]

        def Instance(self, args):
            """Create an instance of the resistor from the given args"""

            Split_args = args.GetArgsWithSwitches(self.Inst_args)
            return ComponentInstance(self.GetName(), (Split_args["-na"], Split_args["-nb"]))

        def Info(self):

            return "Resistance = " + str(self.Resistance)

        def Type(self):

            return "Resistor"

        def Configure(self, args):
            """Reconfigure the resistor with the given args."""

            Split_args = args.GetArgsWithSwitches(self.Csct_args)
            self.Resistance = Split_args["-r"]

        def GetGMatContrib(self, gmat, ivec, instance):
            """return the resistors contribution to the conductance matrix and current vector."""

            Node_a, Node_b = instance.ListNodes()

            # CONTRIBUTION TO CONDUCTANCE MATRIX
            #
            #      A ...  B
            #   +------------
            # A | +G      -G
            # . |
            # . |
            # . |
            # B | +G      -G
            #   |  

            if(Node_a in gmat):
                
                gmat[Node_a][Node_a] += 1 / self.Resistance

            if(Node_b in gmat):

                gmat[Node_b][Node_b] += 1 / self.Resistance

            if(Node_a in gmat and Node_b in gmat):

                gmat[Node_a][Node_b] -= 1 / self.Resistance
                gmat[Node_b][Node_a] -= 1 / self.Resistance

            return gmat, ivec
            

    def Construct(self, name, args):
        """Construct a componenet from this factory, using any valid args."""

        Def_args = args.GetArgsWithSwitches(self.Csct_args)
        return self.Resistor(name, Def_args["-r"])

    def Summary(self):

        return "Represents a simple resistor across a set of nodes."

    def Name(self):

        return "Resistor"


#Register the component into the global component registry.
GLOBAL.RegisterComponent("Resistor", ResistorFactory())
