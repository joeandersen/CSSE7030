"""
PyWire.

INFO

June 1st, 2008.
Written by Liam Maruff.

DESCRIPTION

A circuit simulator, made to be used as a general framework through which plugin components may be used to extend functionality.

LICENSE

I, Liam Maruff, Hereby grant the rights to distribute, modify, and edit the source to PyWire, on the condition that this agreement, and my ownership of the code contained herewithin be maintained.

Furthmore, I grant the right to use excerpts from the source to PyWire without express permission, with exclusion of commercial application.
"""


import os
import time
import sys

#Import other modules
from Logging import *
from Exceptions import *
from Component import *
from Analysis import *

#Import Matrix math module.
from Matrix2D import *

#SCRIPTS-------------------------------------------------------------------------------------------------------------------------------------------------

def GetFileDataAsLines(filename):
    """GetFileDataAsLines -> str -> list or none

Opens file filename,  and reads content as lines into a list. If file not found, raise an exception."""

    ret = []

    try:
        
        for line in open(filename):

            ln = line

            if(ln[-1] == '\n'):
                ln = ln[:-1]
                
            ret.append(ln)

        return ret
    
    except IOError:

        raise NO_SUCH_FILE, "File not found."


def ExecScript(plugin_filename):
    """ExecScript -> str -> list or none

Opens file plugin_filename, and execute contents as python code. If file not found or code is erroneous, raise an exception."""
    
    execfile(plugin_filename)

#MWAH-------------------------------------------------------------------------------------------------------------------------------------------------

ARG_STR = "str"
ARG_INT = "int"
ARG_FPN = "float"

class InterpCmd:
    """This class encapsulates arguments to a command into one object."""

    def __init__(self, str_input, cmd_sep = " ", arg_sep = ","):
        """__init__ -> self, str -> str, str list or none
Creates the InterpCmd based on the input string, and the seperators deliming arguements from the command, and the arguements from each other."""

        #split the string to find the cdm and the 
        str_split = str_input.partition(cmd_sep)

        self.Command = str_split[0].lower()
        self.Arguments = str_split[2].rsplit(arg_sep)

        #get each argument
        for i in range(0, len(self.Arguments)):

            self.Arguments[i] = self.Arguments[i].strip()

    def ForgetArg(self, arg_no):
        """ForgetArg -> self, int -> none

forget an argument by its number; essentially deletes the arguement fro the object."""
        
        try:
            
            del(self.Arguments[arg_no])
            
        except:

            #if the arguement doesn't exist, just terminate.
            pass

    def ForgetArgs(self, arg_nos):
        """ForgetArg -> self, list -> none

forget an list of arguements by their numbers."""

        #sort the arguement numbers in reverse order, so we delete the furthest arguements first and end up deleting the wrong arguements thereafter.
        arg_nos.sort(reverse = True)

        for i in arg_nos:

            self.ForgetArg(i)
        
    def ArgCount(self):
        """ForgetArg -> self -> int

Return the number of arguments."""
    
        return len(self.Arguments)

    def GetArg(self, arg_no, arg_type, default_val = ",no: ;val,"):

        Ret_arg = None
        Raw_arg = None

        try:

            Raw_arg = self.Arguments[arg_no]

        except:

            if(default_val == ",no: ;val,"):

                raise INVALID_VALUE, "Missing command and no available default."

            else:

                Raw_arg = default_val

        if(arg_type == ARG_INT):

            Ret_arg = int(Raw_arg)

        elif(arg_type == ARG_FPN):

            Ret_arg = float(Raw_arg)

        else:

            Ret_arg = str(Raw_arg)

        return Ret_arg

    #arg_data = [ [num, type, def], ...]
    def GetArgs(self, arg_data):
        """GetArgs -> list -> list

Return args as defined in arg_data. Information is of format [[arg number, arg_type, default_type], ...]. Arg type cane be ARG_STR, ARG_INT or ARG_FPN."""

        Ret_args = []

        for l in arg_data:

            i = l[1] # the arg type
            j = l[0] # the arg number

            This_ret = None
            
            if(len(l)>2):

                This_ret = GetArg(i, j)

            else:

                This_ret = GetArg(i, j, l[2])

            Ret_args.append(This_ret)

        return Ret_args

    #arg_data = [ [switch, type, def], ...]
    def GetArgsWithSwitches(self, switch_data, on_fail_append_none = True):
        """GetArgsWithSwitches -> list, boolean -> dict

Return args which have matching switches (eg. -a 10, -t 6). switch_data is of format [[arg switch, arg_type, default_type], ...]. Arg type cane be ARG_STR, ARG_INT or ARG_FPN. In the evnt that the
arguement cannot be found and no default argument is supplied, the program amy be drected to append "none type", at the given switch. Returns a dictionary indexed by the switches."""

        Ret_args = {}

        for i in switch_data:

            Start_len = len(Ret_args)
            for j in self.Arguments:

                #get each arguement
                Arg_bits = j.partition(i[0])

                Key = Arg_bits[1]
                Data = Arg_bits[2]

                #if the arguement was passed, convert it to the correct data type, and then append it to the output.
                if(len(Key)):

                    Data_stripped = Data.strip()
                    Arg_type = i[1]

                    Ret_args[Key] = None

                    if(len(Data_stripped)):

                        if(Arg_type == ARG_INT):

                            Ret_args[Key] = int(Data_stripped)

                        elif(Arg_type == ARG_FPN):

                            Ret_args[Key] = float(Data_stripped)

                        else:

                            Ret_args[Key] = str(Data_stripped)

            #if arg was not found, either append none if directed so, otherwise do nothing
            if(len(Ret_args) == Start_len):

                if(on_fail_append_none):

                    Ret_args[Key] = None

                #No else, because we just don't do anything.

                    

        return Ret_args



#WORKSPACE---------------------------------------------------------------------------------------------------------------------------------------------------
class Circuit:
    """THe circuit class, represents an electronic circuit.

Members:

Parts - Dictionary ofthe parts in this circuit., indexed by their name.

Methods:

NodeCount(self) - Returns the number of nodes in this circuit
ListNodes(self) - Returns a list of the nodes in this circuit
AddPart(self, pt_name, part) - Adds a part to this circuit, under pt_name
DelPart(self, pt_name) - Deletes a part from this circuit, named pt_name
ListParts(self) - List the parts in this circuit; throws an exception if the circuit has no components
HasPart(self, pt_name) - Check if this circuit has agiven part, throws an exception if it doesnt.
HasPartInv(self, pt_name) - Checks if a circuit has a given part; throws an exception is it does.
DelPartType(self, pt_type) - Delete all parts of a given type.
CountPartType(self, pt_type) - Return thenumber of parts in this circuit, of a given type.

"""

    def __init__(self):

        self.Parts = {}

    def NodeCount(self):

        Nodes = []

        for i in self.Parts:

            Nodes += self.Parts[i].ListNodes()

        Unique_nodes = []

        for i in Nodes:

            if i not in Unique_nodes:

                Unique_nodes.append(i)

        return len(Unique_nodes)

    def ListNodes(self):

        Nodes = []

        for i in self.Parts:

            Nodes += self.Parts[i].ListNodes()

        Unique_nodes = []

        for i in Nodes:

            if i not in Unique_nodes:

                Unique_nodes.append(i)

        return Unique_nodes
            

            
    def AddPart(self, pt_name, part):
        
        if(self.HasPartInv(pt_name)):

           self.Parts[pt_name] = part

    def DelPart(self, pt_name):

        if(self.HasPart(pt_name)):
            
            del(self.Parts[pt_name])

    def ListParts(self):

        if(len(self.Parts)):

           return self.Parts.keys()

        else:
           
            raise INVALID_VALUE, "No parts have been added."

    def HasPart(self, pt_name):
        
        if(pt_name in self.Parts):

            return True

        else:
            
            raise INVALID_VALUE, "Part '" + pt_name + "' does not exist."
            
    def HasPartInv(self, pt_name):
        
        if(pt_name in self.Parts):

            raise INVALID_VALUE, "Part '" + pt_name + "' already exists."

        else:

            return True

    def DelPartType(self, pt_type):

        Del_instnces = 0
           
        if(self.ListParts()):
           
            for i in self.Parts:

                if(self.Parts[i].GetName() == pt_type):

                    self.DelPart(i)
                    Del_instnces += 1

        return Del_instnces


    def CountPartType(self, pt_type):

        Inst_count = 0
           
        for i in self.Parts:

            if(self.Parts[i].GetName() == pt_type):

                Inst_count += 1

        return Inst_count

class Workspace:
    """Te Workspace class, a singleton which holds all of our run-time variables, inclduing our circuits, components, and analysis methods.

Members:

Circuits - The circuits weve made so far
Components - The components we've made from factories
Analyses - The analyses weve made from factories

COMPONENT_REGISTRY - The dictionary of component factories, indexed by name
SCRIPTS_LOADED - The scripts we've loaded from file
CURRENT_CT - The currently selected circuit
ANALYSIS_REGISTRY - The  dictionary of analysis factories, indexed by name
DIRECTORY - The current directory were in, used for file i/o.
        
Methods:

PerformAnalysis(self, as_name, ct_name, args) - Perform a given analysis on a circuit.
DelAnalysis(self, as_name) - Delete an analysis. 
ListAnalyses(self) - list analysis currently available. Throws exception if none exist.
AddAnalysis(self, reg_str, as_name, args) - add a new analysis made from factory reg_str.
ConfigureAnalysis(self, as_name, args) - change settings for an analysis.
GetAnalysisName(self, reg_str) - getht ename of an analysis.
GetAnalysisSummary(self, reg_str) - Get a brief summary of an analysis.
HasAnalysis(self, as_name) - Check if analysis exists, if not, throw exception.
HasAnalysisInv(self, as_name) - Check if analysis exists, if so, throw an exception.

AddPart(self, pt_name, cp_name, ct_name, args) - Add a part from a given component
DelPart(self, pt_name, ct_name) - delete a part by name
CountParts(self, cp_name) - Count how many instances of a part there are
ListParts(self, ct_name) - List the parts in a circuit, throw exception if none.

DelComponent(self, cp_name) - Delete a component
ListComponents(self) - List components, throw an exception if none.
AddComponent(self, reg_str, cp_name, args) - Add a component, throw an exception on error.
ConfigureComponent(self, cp_name, args) - Configure a componenet.
GetComponentName(self, reg_str) - Get the name of a component.
GetComponentSummary(self, reg_str) - Get a summary of a component
HasComponent(self, cp_name) - Check if component exists, if not, throw exception
HasComponentInv(self, cp_name) - check if component exists, if so, throw exception

AddCircuit(self, ct_name) - add a circuit to the workspace
DelCircuit(self, ct_name) - delete a circuit from the worksapce
ListCircuits(self) - list circuits in workspace, throw exception if there are none
HasCircuit(self, ct_name) - Check if workspace has circuit, if not, throw exception
SetCurrentCt(self, ct_name) - Set the currently selected circuit.
GetCurrentCt(self) - Get the currently selected circuit.
DeselectCurrentCt(self) - Deselect currently selected circuit.

ListAnalysisRegistry(self) - List the analysis factories in the registry.
ListComponentRegistry(self) - List the componenet factories in the registry

CompIsInRegistry(self, reg_str) - Check if componenet is in registry, throw excpeption if it isnt
AnalIsInRegistry(self, reg_str) - Check if analysis is in registry, throw excpeption if it isnt

RegisterComponent(self, reg_str, component_factory) - Add a componenet factory to the registry
RegisterAnalysis(self, reg_str, analysis_method) - Add an analysis factory to the registry.

GetDir(self) - Get the current directory we're in.
SetDir(self, str_path) - set the current directory.

"""
    def __init__(self):
        
        self.Circuits = {}
        self.Components = {}
        self.Analyses = {}

        self.COMPONENT_REGISTRY = {}
        self.CURRENT_WS = None
        self.CURRENT_CT = None
        self.ANALYSIS_REGISTRY = {}
        self.DIRECTORY = os.getcwd()
        

    def PerformAnalysis(self, as_name, ct_name, args):

        if(self.HasAnalysis(as_name)):

            if(self.HasCircuit(ct_name)):
            
                self.Analyses[as_name].Analyse(self.Circuits[ct_name], self.Components, args)


    def DelAnalysis(self, as_name):

        if(self.HasAnalysis(as_name)):
            
            del(self.Analyses[as_name])


    def ListAnalyses(self):

        if(len(self.Analyses.keys())):

           return self.Analyses.keys()

        else:
           
            raise INVALID_VALUE, "No analyses have been created."

    def AddAnalysis(self, reg_str, as_name, args):

        if(self.AnalIsInRegistry(reg_str)):

            if(self.HasAnalysisInv(as_name)):

                Cp_cstd = self.ANALYSIS_REGISTRY[reg_str].Construct(as_name, args)
                self.Analyses[as_name] = Cp_cstd

    def ConfigureAnalysis(self, as_name, args):

            if(self.HasAnalysis(as_name)):

                self.Analyses[as_name].Configure(args)

    def GetAnalysisName(self, reg_str):

        if(self.AnalIsInRegistry(reg_str)):

            return self.ANALYSIS_REGISTRY[reg_str].Name()

    def GetAnalysisSummary(self, reg_str):

        if(self.AnalIsInRegistry(reg_str)):

            return self.ANALYSIS_REGISTRY[reg_str].Summary()

    def HasAnalysis(self, as_name):

        if(as_name in self.Analyses):

           return True

        else:

           raise INVALID_VALUE, "Analysis '" + as_name + "' does not exist."

    def HasAnalysisInv(self, as_name):

        if(as_name in self.Analyses):

           raise INVALID_VALUE, "Analysis '" + as_name + "' already exist."

        else:

            return True
        
#-----------------------------------------------------------PARTS



    def AddPart(self, pt_name, cp_name, ct_name, args):

        if(self.HasComponent(cp_name)):     

            self.Circuits[ct_name].AddPart(pt_name, self.Components[cp_name].Instance(args))

    def DelPart(self, pt_name, ct_name):

        if(self.HasCircuit(ct_name)):     

            self.Circuits[ct_name].DelPart(pt_name)

    def CountParts(self, cp_name):

        Instance_count = 0

        for i in self.Circuits:

            Instance_count += self.Circuits[i].CountPartType(cp_name)

        return Instance_count
           
    def ListParts(self, ct_name):

        if(self.HasCircuit(ct_name)):
           
           return self.Circuits[ct_name].ListParts()

        else:
           
            raise INVALID_VALUE, "Circuit '" + ct_name + "' doesn't exists."

        
#-----------------------------------------------------------COMPONENTS

    def DelComponent(self, cp_name):

        Instances_deleted = 0

        if(self.HasComponent(cp_name)):
            
            del(self.Components[cp_name])

        for i in self.Circuits:

            Instances_deleted += self.Circuits[i].DelPartType(cp_name)

        return Instances_deleted

    def ListComponents(self):

        if(len(self.Components.keys())):

           return self.Components.keys()

        else:
           
            raise INVALID_VALUE, "No components have been created."

    def AddComponent(self, reg_str, cp_name, args):

        if(self.CompIsInRegistry(reg_str)):

            if(self.HasComponentInv(cp_name)):

                Cp_cstd = self.COMPONENT_REGISTRY[reg_str].Construct(cp_name, args)
                self.Components[cp_name] = Cp_cstd

    def ConfigureComponent(self, cp_name, args):

            if(self.HasComponent(cp_name)):

                self.Components[cp_name].Configure(args)

    def GetComponentName(self, reg_str):

        if(self.CompIsInRegistry(reg_str)):

            return self.COMPONENT_REGISTRY[reg_str].Name()

    def GetComponentSummary(self, reg_str):

        if(self.CompIsInRegistry(reg_str)):

            return self.COMPONENT_REGISTRY[reg_str].Summary()

    def HasComponent(self, cp_name):

        if(cp_name in self.Components):

           return True

        else:

           raise INVALID_VALUE, "Component '" + cp_name + "' does not exist."

    def HasComponentInv(self, cp_name):

        if(cp_name in self.Components):

           raise INVALID_VALUE, "Component '" + cp_name + "' already exist."

        else:

            return True


#-----------------------------------------------------------CIRCUITS
        
    def AddCircuit(self, ct_name):

        if(ct_name not in self.Circuits):

           self.Circuits[ct_name] = Circuit()

        else:
        
            raise INVALID_VALUE, "Circuit '" + ct_name + "' already exists."

    def DelCircuit(self, ct_name):

        if(self.HasCircuit(ct_name)):
            
            del(self.Circuits[ct_name])

        else:

           raise INVALID_VALUE, "Circuit \'" + ct_name + "\' does not exist."            


    def ListCircuits(self):

        if(len(self.Circuits)):

           return self.Circuits.keys()

        else:

            raise INVALID_VALUE, "No circuits exist."

    def HasCircuit(self, ct_name):

        if(ct_name in self.Circuits):

           return True

        else:

           raise INVALID_VALUE, "Circuit '" + ct_name + "' does not exist."

    def SetCurrentCt(self, ct_name):

        if(self.HasCircuit(ct_name)):

           self.CURRENT_CT = ct_name

        else:

           raise INVALID_VALUE, "Circuit \'" + ct_name + "\' does not exist."

    def GetCurrentCt(self):

        if(self.CURRENT_CT == None):

            raise INVALID_VALUE, "No circuit currently selected."

        else:

            return self.CURRENT_CT

    def DeselectCurrentCt(self):

            self.CURRENT_CT = None

#-----------------------------------------------------------REGISTRY 


    def ListAnalysisRegistry(self):

        if(len(self.ANALYSIS_REGISTRY)):

           return self.ANALYSIS_REGISTRY.keys()

        else:

            raise INVALID_VALUE, "No analyses have been loaded. Not a lot you can do!"


    def ListComponentRegistry(self):

        if(len(self.COMPONENT_REGISTRY)):

           return self.COMPONENT_REGISTRY.keys()

        else:

            raise INVALID_VALUE, "No components have been loaded. Not a lot you can do!"


    def CompIsInRegistry(self, reg_str):

        if(reg_str in self.COMPONENT_REGISTRY):

           return True

        else:

            raise INVALID_VALUE, "Component '" + reg_str + "' not found in registry."
                   

    def AnalIsInRegistry(self, reg_str):

        if(reg_str in self.ANALYSIS_REGISTRY):

           return True

        else:

            raise INVALID_VALUE, "Component '" + reg_str + "' not found in registry."
          
    def RegisterComponent(self, reg_str, component_factory):

        if(reg_str in self.COMPONENT_REGISTRY):

            raise INVALID_VALUE, "Component '" + reg_str + "' already exists in component registry."

        else:

            self.COMPONENT_REGISTRY[reg_str] = component_factory


    def RegisterAnalysis(self, reg_str, analysis_method):

        if(reg_str in self.COMPONENT_REGISTRY):

            raise INVALID_VALUE, "Analysis '" + reg_str + "' already exists in Analysis registry."

        else:

            self.ANALYSIS_REGISTRY[reg_str] = analysis_method


#-----------------------------------------------------------FILES 

    def GetDir(self):

        return self.DIRECTORY

    def SetDir(self, str_path):

        try:

            SELF.directory = os.path.abspath(str_path)

        except:

            raise INVALID_VALUE, "Invalid directory '" + str_path + "'."
        
# The workspace singleton, contains what we would call our 'global' variables, even thought theyre techincally not global; just a convineient namespace name.         
GLOBAL = Workspace()

# NOTE
#
##
##The functions below are linked to commands. for brevity, they are each described here.
##
##To ensure maximum communication, the e fucnctions will throw excetions if an error occurs, such as a missing file, circuit, component, etc, and this error will be printed to the console to
##communicate the failure to the user.
##
##They all take an intermediate command, of type InterpCmd.
##
##Interp_ct_select(int_cmd) - select a circuit
##Interp_ct_destroy(int_cmd) - destroy a circuit
##Interp_ct_deselect(int_cmd) - deselect a circuit
##Interp_ct_create(int_cmd) - create a circuit
##Interp_ct_list(int_cmd) - list currently circuits
##
##Interp_sel_current(int_cmd) - return currently selected circuit
##
##Interp_fl_setdir(int_cmd) - set the curent directory
##Interp_fl_getdir(int_cmd) - get the current directory
##
##Interp_fl_exec_raw(int_cmd) - execute a script as raw python code
##Interp_fl_exec_cmds(int_cmd) - execute a script as a list of PyWire commands
##Interp_as_create(int_cmd) - create a new analysis
##Interp_as_analyse(int_cmd) - perform an analysis
##Interp_as_config(int_cmd) - configgure an analysis
##Interp_as_delete(int_cmd) - delete an analysis
##Interp_as_inventory(int_cmd) - get inventory of analysis factories
##Interp_as_list(int_cmd) - list the currently avaialabe analyses
##Interp_cp_create(int_cmd) - create a componenet
##Interp_cp_config(int_cmd) - configure a componenent
##Interp_cp_delete(int_cmd) - delete a component
##Interp_cp_inventory(int_cmd) - list componenet factories loaded.
##Interp_cp_list(int_cmd) - list th components currently avaialable
##Interp_cp_countinstances(int_cmd) - count the numbe rof instances of a given component
##Interp_pt_add(int_cmd) - add a new part to a circuit
##Interp_pt_list(int_cmd) - list the parts in a circuit
##Interp_pt_delete(int_cmd) - delete a part from a circuit


#-----------------------------------------------------------CIRCUITS 
def Interp_ct_select(int_cmd):

    try:

        Ct_name = int_cmd.GetArg(0, ARG_STR)
        GLOBAL.SetCurrentCt(Ct_name)
        PrintAndLogG("Current workspace changed to '" + Ct_name + "'.")
        
    except:

        PrintAndLogGExcept()
        return


def Interp_ct_destroy(int_cmd):

    try:
        
        Ct_name = int_cmd.GetArg(0, ARG_STR)
        GLOBAL.DelCircuit(Ct_name)
        
    except:

        PrintAndLogGExcept()
        return

    PrintAndLogG("Circuit '" + Ct_name + "' deleted.")

def Interp_ct_deselect(int_cmd):

    GLOBAL.DeselectCurrentCt()
       
    PrintAndLogG("Current circuit deselected.")

def Interp_ct_create(int_cmd):

    try:

        Ct_name = int_cmd.GetArg(0, ARG_STR)

        GLOBAL.AddCircuit(Ct_name)

        PrintAndLogG("Circuit '" + Ct_name + "' created.")
        
    except:

        PrintAndLogGExcept()
        return


def Interp_ct_list(int_cmd):

    try:

        Ct_list = GLOBAL.ListCircuits()

        PrintAndLogG("Existing circuits are:")

        for i in Ct_list:

            PrintAndLogG("- " + i, 2)
            
    except:

        PrintAndLogGExcept() 

#-----------------------------------------------------------MISC 

def Interp_sel_current(int_cmd):

    try:
        
        Ct_name = GLOBAL.GetCurrentCt()
        PrintAndLogG("Current circuit is '" + Ct_name + "'.")
        
    except:

        PrintAndLogGExcept()

def Interp_fl_setdir(int_cmd):

    Name = int_cmd.GetArg(0, ARG_STR)

    try:

        GLOBAL.SetDir(Name)            
        PrintAndLogG("Current directory changed to '" + GLOBAL.GetDir() + "'.")

    except:
  
        PrintAndLogGExcept()

def Interp_fl_getdir(int_cmd):

    PrintAndLogG("Current directory: " + GLOBAL.GetDir() + ".")



def Interp_fl_exec_raw(int_cmd):

    File = int_cmd.GetArg(0, ARG_STR)

    try:

        PrintAndLogG("Opening '" + File + "', and running contents as python code...")
        ExecScript(GLOBAL.GetDir() + File)            
        PrintAndLogG("File \"" + File + "\" successfully run.")

    except:
  
        PrintAndLogGExcept()

        
def Interp_fl_exec_cmds(int_cmd):


    try:
        
        File = int_cmd.GetArg(0, ARG_STR)
        Cmds = GetFileDataAsLines(GLOBAL.GetDir() + File)

        I = map(InterpCmd, Cmds)

        for j in I:

            Interpret(j)
        
        PrintAndLogG("Finished executing commands from file '" + File + "'.")

    except:
  
        PrintAndLogGExcept()

        

#-----------------------------------------------------------ANALYSIS






def Interp_as_create(int_cmd):

    try:

        Reg_str = int_cmd.GetArg(0, ARG_STR)
        as_name = int_cmd.GetArg(1, ARG_STR)
    
        int_cmd.ForgetArgs([0,1])

        GLOBAL.AddAnalysis(Reg_str, as_name, int_cmd)
        PrintAndLogG("Analysis '" + as_name + "' created.")
           
    except:

        PrintAndLogGExcept()

def Interp_as_analyse(int_cmd):

    #try:

    As_name = int_cmd.GetArg(0, ARG_STR)
    Ct_name = int_cmd.GetArg(1, ARG_STR)

    int_cmd.ForgetArgs([0,1])

    GLOBAL.PerformAnalysis(As_name, Ct_name, int_cmd)
       
  #  except:

    #    PrintAndLogGExcept()


def Interp_as_config(int_cmd):

    try:

        as_name = int_cmd.GetArg(0, ARG_STR)
    
        int_cmd.ForgetArg(0)

        GLOBAL.ConfigureAnalysis(as_name, int_cmd)
        PrintAndLogG("Analysis '" + as_name + "' successfully reconfigured.")
           
    except:

        PrintAndLogGExcept()

def Interp_as_delete(int_cmd):
    

    try:

        as_name = int_cmd.GetArg(0, ARG_STR)
        int_cmd.ForgetArgs([0,1])

        GLOBAL.DelAnalysis(as_name)
        PrintAndLogG("Analysis '" + as_name + "' deleted.")
      
    except:

        PrintAndLogGExcept()


def Interp_as_inventory(int_cmd):

    try:

        Cp_list = GLOBAL.ListAnalysisRegistry()

        PrintAndLogG("Analyses listed in Analysis inventory:")

        for i in Cp_list:
            
            PrintAndLogG(GLOBAL.GetAnalysisName(i) +" (" + i + ") - " + GLOBAL.GetAnalysisSummary(i))     

    except:

        PrintAndLogGExcept()

def Interp_as_list(int_cmd):

    try:

        Cp_list = GLOBAL.ListAnalyses()

        PrintAndLogG("Analyses currently created:")

        for i in Cp_list:
            
            PrintAndLogG(i +" (" + GLOBAL.Analyses[i].Type() + ") : " + GLOBAL.Analyses[i].Info())     

    except:

        PrintAndLogGExcept()

#-----------------------------------------------------------COMPONENTS 

def Interp_cp_create(int_cmd):

    try:

        Reg_str = int_cmd.GetArg(0, ARG_STR)
        Cp_name = int_cmd.GetArg(1, ARG_STR)
    
        int_cmd.ForgetArgs([0,1])

        GLOBAL.AddComponent(Reg_str, Cp_name, int_cmd)
        PrintAndLogG("Component '" + Cp_name + "' created.")
           
    except:

        PrintAndLogGExcept()


def Interp_cp_config(int_cmd):

    try:

        Cp_name = int_cmd.GetArg(0, ARG_STR)
    
        int_cmd.ForgetArg(0)

        GLOBAL.ConfigureComponent(Cp_name, int_cmd)
        PrintAndLogG("Component '" + Cp_name + "' successfully reconfigured.")
           
    except:

        PrintAndLogGExcept()

def Interp_cp_delete(int_cmd):
    

    try:

        Cp_name = int_cmd.GetArg(0, ARG_STR)
        int_cmd.ForgetArgs([0,1])

        GLOBAL.DelComponent(Cp_name)
        PrintAndLogG("Component '" + Cp_name + "' deleted.")
      
    except:

        PrintAndLogGExcept()


def Interp_cp_inventory(int_cmd):

    try:

        Cp_list = GLOBAL.ListComponentRegistry()

        PrintAndLogG("Components listed in component inventory:")

        for i in Cp_list:
            
            PrintAndLogG(GLOBAL.GetComponentName(i) +" (" + i + ") - " + GLOBAL.GetComponentSummary(i))     

    except:

        PrintAndLogGExcept()

def Interp_cp_list(int_cmd):

    try:

        Cp_list = GLOBAL.ListComponents()

        PrintAndLogG("Components currently created:")

        for i in Cp_list:
            
            PrintAndLogG(i +" (" + GLOBAL.Components[i].Type() + ") : " + GLOBAL.Components[i].Info())     

    except:

        PrintAndLogGExcept()



def Interp_cp_countinstances(int_cmd):

    try:

        Cp_name = int_cmd.GetArg(0, ARG_STR)
        PrintAndLogG(str(GLOBAL.CountParts(Cp_name)) + " occurences of component '" + Cp_name + "'.")

    except:

        PrintAndLogGExcept()

#-----------------------------------------------------------PARTS 

def Interp_pt_add(int_cmd):
    

    try:

        Ct_name = GLOBAL.GetCurrentCt()
        Cp_name = int_cmd.GetArg(0, ARG_STR)
        Pt_name = int_cmd.GetArg(1, ARG_STR)

        int_cmd.ForgetArgs([0,1])
        
        GLOBAL.AddPart(Pt_name, Cp_name, Ct_name, int_cmd)

        PrintAndLogG("Part '" + Pt_name + "' added to circuit '" + Ct_name + "'.")
           
    except:

        PrintAndLogGExcept()

def Interp_pt_list(int_cmd):

    try:

        Ct_name = GLOBAL.GetCurrentCt()
        Parts_list = GLOBAL.ListParts(Ct_name)


        PrintAndLogG("Parts in circuit '" + Ct_name + "' are:")

        for i in Parts_list:

           PrintAndLogG("- " + i)

    
    except:

        PrintAndLogGExcept()


def Interp_pt_delete(int_cmd):

    try:

        Ct_name = GLOBAL.GetCurrentCt()
        Pt_name = int_cmd.GetArg(0, ARG_STR)

        GLOBAL.DelPart(Pt_name, Ct_name)
        PrintAndLogG("Part '" + Pt_name + "' deleted from circuit '" + Ct_name + ".")  
           
    
    except:

        PrintAndLogGExcept()

#Match all the command functions to their givn commands, ina  big dictionary.

CMD_TABLE = {"sel_current":Interp_sel_current,
             "ct_deselect":Interp_ct_deselect,
             "ct_select":Interp_ct_select,
             "pt_delete":Interp_pt_delete,
             "pt_add":Interp_pt_add,
             "pt_list":Interp_pt_list,
             "ct_create":Interp_ct_create,
             "ct_destroy":Interp_ct_destroy,
             "ct_list":Interp_ct_list,
             "cp_inventory": Interp_cp_inventory,
             "cp_create": Interp_cp_create,
             "cp_delete": Interp_cp_delete,
             "cp_config": Interp_cp_config,
             "cp_list": Interp_cp_list,
             "as_inventory": Interp_as_inventory,
             "as_create": Interp_as_create,
             "as_delete": Interp_as_delete,
             "as_config": Interp_as_config,
             "as_list": Interp_as_list,
             "fl_exec_raw": Interp_fl_exec_raw,
             "fl_exec_cmds": Interp_fl_exec_cmds,             
             "fl_getdir": Interp_fl_getdir,
             "fl_setdir": Interp_fl_setdir,
             "cp_countinstances" : Interp_cp_countinstances,
             "as_analyse" : Interp_as_analyse}             
                                     
def Interpret(int_cmd):
    """Interpret commands entered via console"""

    #If the command is an exit, then return false, thus breaking out of the intepreter cycle
    if(int_cmd.Command == "exit"):

        return False
    
    else:

        #otherwise, execute the corresponding funtion in the  command table. If there is none, an exception will be thrown and the user will be notified.
        try:

            return CMD_TABLE[int_cmd.Command](int_cmd)

        except:

            PrintAndLogG("Unrecognised command \"" + int_cmd.Command + "\".")

    return

def AppRun():
    """The application itself"""

    #While the interpret method isn't telling us to exit, continue to pass input to it.
    while(Interpret(InterpCmd(raw_input("Command:"))) == None):

        pass

def AppEntry(ini_fn = "init.ini"):
    """Defines the application entry point; loads ini file and the files listed inside it."""

    #Get a list of scripts to load from file.
    Script_load = GetFileDataAsLines(ini_fn)
    LogGWriteSeperator()
    PrintAndLogG("INI file \"" + ini_fn + "\" loaded successfully; loading contents...", 0)

    #load each script.
    for i in Script_load:

        try:

            Script_fn = os.getcwd() + "\\" + i
            ExecScript(Script_fn)
            PrintAndLogG(" - Script \"" + Script_fn + "\" loaded.", 0)

        except:

            PrintAndLogGExcept()

    PrintAndLogG("Application entry successful, PyWire is ready!", 0)
    LogGWriteSeperator()

def AppExit():
    """Defines application exit point. Dump logs, and reach end of  Main.py file."""

    #get the current time
    Time_str = time.asctime();
    Time_str = Time_str.replace(":",";")

    G_log_fn = "Logs"+"\\"+"General "+Time_str+".txt"
    C_log_fn = "Logs"+"\\"+"Commands "+Time_str+".txt"

    #Dump the logs
    DumpLogs(G_log_fn, C_log_fn)
    LogGWriteSeperator()
    PrintAndLogG("General log dumped to \"" + G_log_fn + "\".", 0)
    PrintAndLogG("Command log dumped to \"" + C_log_fn + "\".", 0)
    PrintAndLogG("Application termination successful, PyWire terminated.", 0)

    LogGWriteSeperator()

#Start the program
AppEntry("Default.ini")

#Run the program
AppRun()

#Exit the program
AppExit()

