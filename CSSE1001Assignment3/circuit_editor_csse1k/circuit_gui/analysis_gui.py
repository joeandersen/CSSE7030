"""
Analysis support classes.
"""

from objectwidgets import *
from dialogs import *

class AnalysisCircuit(analysis.Circuit):
        """A subclass of Circuit that can wake a set of
        sleepy widget objects up for analysis as its children.
        
        C'tor: AnalysisCircuit(sleepypair)
        
        (a sleepypair is a tuple of a list of sleepywidgets and
        a list of connections between them)
        """
        
        def __init__(self, sleeptup):
                analysis.Circuit.__init__(self)
                sleepies, cons = sleeptup
                wakies = {}
                for s in sleepies:
                        wakies[s] = s.analyse(self)
                
                self.wakies = wakies
                
                for c in cons:
                        self.connectLoop([wakies[c[0][0]], wakies[c[1][0]]])