"""
This is the big fat MainWindow class. It does... well... everything except circuits. :D
"""

from ui_mainwindow import *
#from py.magic import greenlet
from greenlet import *
from dialogs import *
from objectwidgets import *
from analysis_gui import *
import pickle
import sys

anchorThresholdDistance = 10

class MainWindow(QMainWindow, Ui_MainWindow):
        """The main window of the GUI. We subclass the pyuic generated
        mainwindow for all of the gui components and layout.
        
        Flow control in this class makes use of greenlets for a kind of
        continuation structure.
        """
        def __init__(self):
                QMainWindow.__init__(self)
                self.setupUi(self)
                # hack: enable unified title/toolbar look on OSX
                #       makes it prettier. :)
                self.setUnifiedTitleAndToolBarOnMac(True)
                
                # set the click greenlet to none
                self._clickGreenlet = None
                
                # handle the childClicked event
                # we can't auto-slot this since it's not a properly declared signal (bloody PyQt)
                QObject.connect(self.circuitWidget, SIGNAL("childClicked"), self.circuit_child_clicked)
                
        # we need this decorator to avoid double-binding all these slots
        @QtCore.pyqtSignature("")
        def on_actionSave_activated(self):
                """Saves the current circuit layout to a file."""
                fname = QFileDialog.getSaveFileName(self, "Save circuit", ".", "Circuit files (*.cct)")
                if fname:
                        sleepy = self.circuitWidget.makeSleepy()
                        output = open(fname, "wb")
                        pickle.dump(sleepy, output)
                        output.close()
                        self.circuitWidget.update()
                
        @QtCore.pyqtSignature("")
        def on_actionOpen_activated(self):
                """Opens a saved circuit layout."""
                fname = QFileDialog.getOpenFileName(self, "Open circuit", ".", "Circuit Files (*.cct)")
                if fname:
                        input = open(fname, "rb")
                        sleepy = pickle.load(input)
                        self.circuitWidget.killChildren()
                        self.circuitWidget.wakeUp(sleepy)
                        input.close()
                
                
        def startClickAction(self, callable):
                """Starts the flow of a new click action.
                
                Creates a new greenlet calling the given callable, sets it
                as the greenlet to handle click events, and switches to it.
                Also enables the cancel button."""
                self.actionCancel.setEnabled(True)
                self._clickGreenlet = greenlet(callable)
                self._clickGreenlet.switch()
                
        def endClickAction(self):
                """Concludes the click action flow."""
                self.actionCancel.setEnabled(False)
                self._clickGreenlet = None
                
        @QtCore.pyqtSignature("")
        def on_actionCancel_activated(self):
                self.statusBar().clearMessage()
                self.endClickAction()
                
        @QtCore.pyqtSignature("")
        def on_actionConnect_activated(self):
                self.startClickAction(self.connectObjects)
                
        @QtCore.pyqtSignature("")
        def on_actionDisconnect_activated(self):
                self.startClickAction(self.disconnectObjects)
                
        @QtCore.pyqtSignature("")
        def on_actionFlip_activated(self):
                self.startClickAction(self.flipObject)
                
        @QtCore.pyqtSignature("")
        def on_actionDestroy_activated(self):
                self.startClickAction(self.destroyObject)
                
        def circuit_child_clicked(self, child, dist, anchor):
                """Handles a child click event from the circuitwidget. If a click flow
                action is in progress, this will switch to it with the selected child."""
                if self._clickGreenlet:
                        self._clickGreenlet.switch((child,dist,anchor))
                
        def connectObjects(self):
                """A greenlet click flow for connecting two objects."""
                # get first object
                self.statusBar().showMessage("Select first object anchor to connect...")
                obj1, dist, anchor1 = greenlet.getcurrent().parent.switch()
                if dist > anchorThresholdDistance:
                        self.statusBar().showMessage("Didn't click close enough to an anchor!")
                        return
                
                # get second object
                self.statusBar().showMessage("Select second object anchor to connect...")
                obj2, dist, anchor2 = greenlet.getcurrent().parent.switch()
                if dist > anchorThresholdDistance:
                        self.statusBar().showMessage("Didn't click close enough to an anchor!")
                        return
                        
                # connect the objects, and end the flow
                obj1.connect(anchor1, obj2, anchor2)
                self.statusBar().clearMessage()
                self.endClickAction()
                
        def disconnectObjects(self):
                """A greenlet click flow for disconnecting two objects."""
                
                # get first object
                self.statusBar().showMessage("Select first object anchor to disconnect...")
                obj1, dist, anchor1 = greenlet.getcurrent().parent.switch()
                if dist > anchorThresholdDistance:
                        self.statusBar().showMessage("Didn't click close enough to an anchor!")
                        return
                
                # get second object
                self.statusBar().showMessage("Select second object anchor to disconnect...")
                obj2, dist, anchor2 = greenlet.getcurrent().parent.switch()
                if dist > anchorThresholdDistance:
                        self.statusBar().showMessage("Didn't click close enough to an anchor!")
                        return
                        
                obj1.disconnect(anchor1, obj2, anchor2)
                self.statusBar().clearMessage()
                self.endClickAction()
                
        def flipObject(self):
                """A greenlet click flow for flipping an object. Note that this
                doesn't really need to be a click flow, but it makes life more pleasant
                if all actions can be handled the same way."""
        
                # get the object
                self.statusBar().showMessage("Select object to flip...")
                obj1, dist, anchor = greenlet.getcurrent().parent.switch()
                
                obj1.flip()
                self.statusBar().clearMessage()
                self.endClickAction()
                
        def destroyObject(self):
                """A greenlet click flow for destroying an object. Same applies here as
                for flipObject()."""
                
                # get the object
                self.statusBar().showMessage("Select object to destroy...")
                obj1, dist, anchor = greenlet.getcurrent().parent.switch()
                
                # clean up any connections
                for cn in obj1.connections():
                        obj1.disconnect(cn[0][1], cn[1][0], cn[1][1])
                        
                # schedule the object for deletion
                obj1.deleteLater()
                
                self.statusBar().clearMessage()
                self.endClickAction()
                
        @QtCore.pyqtSignature("")
        def on_beginButton_pressed(self):
                """Begins an analysis pattern."""
                opt = self.analysisCombo.currentText()
                if opt == 'Operating point':
                        sleepies,cons = self.circuitWidget.makeSleepyWithHash()
                        ac = AnalysisCircuit( (sleepies.values(),cons) )
                        try:
                                soln = ac.solve()
                                ps = ac.printableSolution()
                        except Exception,e:
                                self.tdd = TextDisplayDialog("Error", "The circuit could not be solved.\n\nTechnical details:\n"+str(e))
                                self.tdd.show()
                                return
                        
                        if self.doSummaryCheck.isChecked(): 
                                self.tdd = TextDisplayDialog("Solution", ps)
                                self.tdd.show()
                                
                        if self.setAttributesCheck.isChecked():
                                widgetMap = {}
                                for c in self.circuitWidget.children():
                                        circo = ac.wakies[sleepies[c]]
                                        widgetMap[circo] = c
                                
                                for k in soln.keys():
                                        widgetMap[k.owner][k.vartype] = str(round(soln[k],7))
                        
                elif opt == 'Thevenin equivalent':
                        self.startClickAction(self.theveninEquivalent)
                        
                elif opt == 'Norton equivalent':
                        self.startClickAction(self.nortonEquivalent)
                        
                        
        def theveninEquivalent(self):
                """A greenlet click flow for finding the details about a Thevenin equivalent circuit to the
                current circuit. Requires the user to select two nodes in order to perform analysis."""
                
                self.statusBar().showMessage("Select the two nodes to perform equivalence testing at...")
                sleepies,cons = self.circuitWidget.makeSleepyWithHash()
                ac = AnalysisCircuit( (sleepies.values(),cons) )
                
                # get first node
                while True:
                        obj1, dist, anchor1 = greenlet.getcurrent().parent.switch()
                        cn1 = ac.wakies[sleepies[obj1]]
                        if cn1 not in ac.nodes:
                                self.statusBar().showMessage("That's not a node! Select two nodes to perform the test.")
                        else:  
                                break
                        
                self.statusBar().showMessage("Select the second node...")
                        
                # get second node
                while True:
                        obj2, dist, anchor2 = greenlet.getcurrent().parent.switch()
                        cn2 = ac.wakies[sleepies[obj2]]
                        if cn2 not in ac.nodes:
                                self.statusBar().showMessage("That's not a node! Select two nodes to perform the test.")
                        else:  
                                break
                
                self.endClickAction()
                
                self.statusBar().showMessage("Processing.....")
                
                try:
                        vth,rth = ac.solveThevenin([cn1, cn2])
                except Exception,e:
                        self.tdd = TextDisplayDialog("Error", "The circuit could not be solved.\n\nTechnical details:\n"+str(e))
                        self.tdd.show()
                        return
                        
                if self.doSummaryCheck.isChecked(): 
                        self.tdd = TextDisplayDialog("Thevenin equivalence probe", "V_th = %f\nR_th = %f" % (vth, rth))
                        self.tdd.show()
                        
                self.statusBar().clearMessage()
                
        def nortonEquivalent(self):
                """A greenlet click flow for finding the details about a Norton equivalent circuit to the
                current circuit. Requires the user to select two nodes in order to perform analysis."""
        
                self.statusBar().showMessage("Select the two nodes to perform equivalence testing at...")
                sleepies,cons = self.circuitWidget.makeSleepyWithHash()
                ac = AnalysisCircuit( (sleepies.values(),cons) )
                
                # get first node
                while True:
                        obj1, dist, anchor1 = greenlet.getcurrent().parent.switch()
                        cn1 = ac.wakies[sleepies[obj1]]
                        if cn1 not in ac.nodes:
                                self.statusBar().showMessage("That's not a node! Select two nodes to perform the test.")
                        else:  
                                break
                        
                self.statusBar().showMessage("Select the second node...")
                        
                # get second node
                while True:
                        obj2, dist, anchor2 = greenlet.getcurrent().parent.switch()
                        cn2 = ac.wakies[sleepies[obj2]]
                        if cn2 not in ac.nodes:
                                self.statusBar().showMessage("That's not a node! Select two nodes to perform the test.")
                        else:  
                                break
                
                
                self.endClickAction()
                
                self.statusBar().showMessage("Processing.....")
                
                # attempt to solve
                try:
                        i_n,rn = ac.solveNorton([cn1, cn2])
                except Exception,e:
                        self.tdd = TextDisplayDialog("Error", "The circuit could not be solved.\n\nTechnical details:\n"+str(e))
                        self.tdd.show()
                        return
                        
                if self.doSummaryCheck.isChecked(): 
                        self.tdd = TextDisplayDialog("Norton equivalence probe", "I_n = %f\nR_n = %f" % (i_n, rn))
                        self.tdd.show()
                        
                self.statusBar().clearMessage()
