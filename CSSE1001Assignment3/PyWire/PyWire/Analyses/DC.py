class DCFactory(AnalysisFactory):
    """DC Circuit Analysis"""

    class DC(Analysis):

        def __init__(self, name, args):
            """Create a DC analysis, can specify a ground node."""

            Analysis.__init__(self, name)
            
            self.Inst_args = [["-g", ARG_STR, " "]]
            Split_args = args.GetArgsWithSwitches(self.Inst_args)
            self.Reference = Split_args["-g"]

        def Info(self):

            return "No information available."

        def Type(self):

            return "DC Analysis"

        def Configure(self, args):
            """Reconfigure DC analysis, can change ground node"""

            Split_args = args.GetArgsWithSwitches(self.Inst_args)
            self.Reference = Split_args["-g"]

        def Analyse(self, circuit, components, args):
            """Perform this analysis on the given circuit, with the given componenets under the given args."""


            Nodes = circuit.ListNodes()
            Nodes.sort()

            #delete the reference node from the nodes list
            
            if(self.Reference in Nodes):

                for i in range(0, len(Nodes)):

                    if(Nodes[i] == self.Reference):

                        del(Nodes[i])
                
            No_Nodes = len(Nodes)

            #Construct conductance matrix and current vector, which is a dictionary of dictionaries.

            G = {}
            I = {}

            for i in range(0, No_Nodes):

                G[Nodes[i]] = dict()
                I[Nodes[i]] = 0
                
                for j in range(0, No_Nodes):

                    G[Nodes[i]][Nodes[j]] = 0

            #we have our conductance matrix. Now we gotta pass it round, and fill it out.

            for i in circuit.Parts:

                G, I = components[circuit.Parts[i].GetName()].GetGMatContrib(G, I, circuit.Parts[i])

            #Now we have the matrix and the vectors we need. just need to make them into a form we can pass to Mat2D.

            #unpack matrice
            Voltage_labels = I.keys()
            
            G_unpack = []
            I_unpack = []

            for i in Voltage_labels:

                I_unpack.append(I[i])

                for j in Voltage_labels:

                    G_unpack.append(G[i][j])

            #if I is the zero matrix, we can skip right ahead and say all our voltages must be zero.

            All_zero = True
            
            for i in I_unpack:

                if i != 0:

                    All_zero = False
                    break

            V = None

            if(All_zero):

               V = I_unpack

            else:

                #...If they werent all zero, we need to solve the system of linear equations.

                G = Matrix2D.fromlist(No_Nodes, G_unpack)
                I = Matrix2D.fromlist(1, I_unpack)

                try:

                    V = G.inverse() * I
                    V = V.tovector()

                except:

                    raise INVALID_VALUE, "DC circuit solver failed. Please check input circuit."

            #print the results.

            PrintAndLogG("Analysis of circuit complete. Results are as follows:")

            V_format = dict(zip(Voltage_labels, V))
            Voltage_labels.sort()
            
            for i in Voltage_labels:

                if(i[0] != "_"):
                    
                    PrintAndLogG("Voltage at node " + i + ": " + str(V_format[i]))

            

    def Construct(self, name, args):
        """Constrct a new DC analysis with the given args"""

        return self.DC(name, args)
    
    def Summary(self):

        return "Performs DC analysis on a Circuit."

    def Name(self):

        return "DC Analysis"

#Register this analysis into the global Analysis registry.
GLOBAL.RegisterAnalysis("DC Analysis", DCFactory())
