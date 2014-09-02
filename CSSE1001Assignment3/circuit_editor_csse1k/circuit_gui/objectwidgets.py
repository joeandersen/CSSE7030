"""
This file contains the main classes of the GUI system, comprising the actual
circuit editing widget and its components. 

It also contains a set of 'Sleepy' classes, serialization and analysis adapter
classes used in tandem with the corresponding GUI widgets for saving/loading
of layouts, and for performing circuit analysis.
"""

# import that barge, tote that bale!
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
#from py.magic import greenlet
import circuit as analysis
from dialogs import AttributeDialog

class ObjectAttributeModel(QAbstractItemModel):
        """A Qt item model representing the attributes of a circuit component.
        
        C'tor: ObjectAttributeModel(ObjectWidget)
        """
        def __init__(self, object):
                QAbstractItemModel.__init__(self)
                self._object = object
                
        # all these methods' signatures and function are documented extensively in the Qt documentation
        # so there is no real need to duplicate that effort here in a subclass
                
        def index(self, row, column, parent):
                return self.createIndex(row, column)
                
        def flags(self, index):
                # only make the values column editable
                if index.column() == 0:
                        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
                elif index.column() == 1:
                        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
                      
        def headerData(self, section, orientation, role):
                if orientation == Qt.Horizontal:
                        if role == Qt.DisplayRole:
                                if section == 0:
                                        return QVariant("Attribute")
                                elif section == 1:
                                        return QVariant("Value")
                return QVariant()
                        
        def data(self, index, role):
                if role in [Qt.DisplayRole, Qt.EditRole]:
                        if index.column() == 0:
                                return QVariant(self._object.attributes()[index.row()])
                        elif index.column() == 1:
                                return QVariant(self._object[self._object.attributes()[index.row()]])
                else:
                        return QVariant()
                        
        def rowCount(self, index):
                return len(self._object.attributes())
                
        def columnCount(self, index):
                return 2
                
        def setData(self, index, value, role):
                if role == Qt.EditRole:
                        if index.column() == 1:
                                # set the attribute on the object
                                self._object[self._object.attributes()[index.row()]] = value.toString()
                                #self.emit(SIGNAL("dataChanged(QModelIndex,QModelIndex)"), index, index)
                                return True
                return False
                
class ObjectWidget(QWidget):
        """The base class for all circuit object widgets. It implements a lot of basic
        functionality, including selecting, dragging, connection/disconnection and attribute storage.
        
        Each widget has a number of anchor points where connections can be made. 
        Subclasses must set these up in their constructors, by changing the properties
        self._anchorPoints, self._connections (set it to empty lists initially)
        and self._maxConnections. See NodeWidget and friends below for examples of
        subclasses.
        
        SIGNALS:
                selected() - emitted when this object is selected
                unselected()
                connectionsChanged()
                clicked(int, QPoint) - emitted when the object is clicked,
                                       with distance from nearest anchor and which
                                       anchor it is.
                moved(QPoint) - emitted when the object moves.
                flipped() - emitted when the object flips orientation
        """
        def __init__(self, parent=None):
                QWidget.__init__(self, parent)
                self._orientation = 'h'
                self._isSelected = False
                self._isDragging = False
                self._anchorPoints = [(0,0)]
                self._connections = {self._anchorPoints[0]: []}
                self._maxConnections = {self._anchorPoints[0]: 0}
                self._attributes = {'nickname': ''}
                
                # attribute model
                self._attrmodel = ObjectAttributeModel(self)
                
                # slot connections
                QObject.connect(self, SIGNAL("selected()"), self, SLOT("update()"))
                QObject.connect(self, SIGNAL("unselected()"), self, SLOT("update()"))
                
        def __getitem__(self, attr):
                """Get an attribute of the object."""
                return self._attributes[attr]
                
        def __setitem__(self, attr, value):
                """Set an attribute of the object."""
                self._attributes[attr] = value
                
        def attributes(self):
                """Returns the list of available attributes.
                
                attributes() -> list<string>
                """
                return self._attributes.keys()
                
        def anchorPoints(self):
                """Returns the list of available anchorpoints.
                
                anchorPoints() -> list<tup>
                """
                return self._anchorPoints
                
        def connections(self, ancPoint=None):
                """If given an anchor point, this functionr returns a list of 
                connections associated with that anchor point. Otherwise, it will
                return all connections associated with this object.
                
                connections are of the form: list<tuple<object, anchor>, tuple<object,anchor>>
                
                connections([tup]) -> list<connections>
                """
                if ancPoint:
                        return [[(self, ancPoint), (other, other.anchorOf(self))] for other in self._connections[ancPoint]]
                else:
                        cons = []
                        for ap in self._anchorPoints:
                                cons = cons + self.connections(ap)
                        return cons
                
        def anchorOf(self, other):
                """Gets the anchor point that connects this object to other.
                anchorOf(object) -> QPoint
                """
                for x in self._connections:
                        if other in self._connections[x]:
                                return x
                return None
                
        def canConnect(self, ancPoint):
                """Is there space for another connection on the given anchor point?
                
                canConnect(QPoint) -> bool
                """
                return (len(self._connections[ancPoint]) < self._maxConnections[ancPoint] or self._maxConnections[ancPoint] == -1)
                
        def connectTo(self, ancPoint, object):
                """Connects this object to another via the given anchor point, if possible,
                in a one-way fashion.
                
                connectTo(QPoint, object) -> void
                """
                if self.canConnect(ancPoint):
                        self._connections[ancPoint].append(object)
                        self.emit(SIGNAL("connectionsChanged()"))
                        
        def connect(self, ancPoint, object, otherAncPoint):
                """Connects this object to another via the two given anchors, if possible,
                in a two-way fashion.
                
                connect(QPoint, object ,QPoint) -> void
                """
                if self.canConnect(ancPoint) and object.canConnect(otherAncPoint):
                        self.connectTo(ancPoint, object)
                        object.connectTo(otherAncPoint, self)
                        
        def disconnectFrom(self, ancPoint, object):
                """Destroys one end of a connection towards object via anchor point."""
                if object in self._connections[ancPoint]:
                        self._connections[ancPoint].remove(object)
                        self.emit(SIGNAL("connectionsChanged()"))
                        
        def disconnect(self, ancPoint, object, otherAncPoint):
                """Destroys an entire connection towards object's otherAncPoint 
                via this object's ancPoint."""
                self.disconnectFrom(ancPoint, object)
                object.disconnectFrom(otherAncPoint, self)
                
        def mouseDoubleClickEvent(self, event):
                """Handles a mouse double click by opening an attribute dialog"""
                self._attrdlg = AttributeDialog(self._attrmodel)
                self._attrdlg.show()
                
        def mousePressEvent(self, event):
                """Handles a mouse press event on the object widget. Prepares to
                start the drag-movement process, and attempts to select the widget."""
		self._isDragging = True
		self._dragLastPos = QPoint(event.globalX(), event.globalY())
		self._dragStartPos = QPoint(self.x(), self.y())
                
                # find nearest anchor point to where the user clicked
                anchorPoints = [QPoint(x,y) for x,y in self._anchorPoints]
                dragPoint = QPoint(event.x(), event.y())
                leastDist = (dragPoint - anchorPoints[0]).manhattanLength()
                leastPoint = anchorPoints[0]
                for p in anchorPoints:
                        dist = (dragPoint - p).manhattanLength()
                        if dist < leastDist:
                                leastDist = dist
                                leastPoint = p
                self._dragClosestAnchor = leastPoint
                
                # emit the Qt signal
                self.emit(SIGNAL("clicked(int,QPoint)"), leastDist, leastPoint)
		#self.parent().selectMe(self)
                
        def mouseMoveEvent(self, event):
                """Handles mouse movement on the widget. If we're in drag mode, ie
                a button is held down, the widget will move by snapped intervals."""
		if self._isDragging:
			curPos = QPoint(self.x(), self.y())
			newPos = self._dragStartPos + (event.globalPos() - self._dragLastPos)
                        snapPos = self.parent().snap(newPos)
			self.move(snapPos)
			self.emit(SIGNAL("moved(QPoint)"), snapPos)
			#self.lastPos = event.globalPos()
                        
        def mouseReleaseEvent(self, event):
		self._isDragging = False
                
        def flip(self):
                """Flips the object's orientation over."""
                self._orientation = {'h': 'v', 'v': 'h'}[self._orientation]
                self.update()
                self.emit(SIGNAL("flipped()"))
                
        def orientation(self):
                """Returns the object's present orientation.
        
                orientation() -> char (one of 'h' or 'v')
                """
                return self._orientation
                
        def selected(self):
                """Returns True if the object is selected, otherwise False."""
                return self._isSelected
                
        def select(self):
                """Sets this object as selected."""
                self._isSelected = True
                self.emit(SIGNAL("selected()"))
                
        def unselect(self):
                """Sets this object as unselected."""
                self._isSelected = False
                self.emit(SIGNAL("unselected()"))
                
        def drawSelectedOutline(self, painter):
                """A convenience function for subclasses to paint a red box around
                the widget when it is selected.
                
                drawSelectedOutline(QPainter) -> void
                """
                
                if self._isSelected:
			painter.setPen(Qt.red)
			painter.drawRect(QRect(0,0,self.width(), self.height()))

class CircuitWidget(QWidget):
        """The parent grid widget that holds circuit component widgets."""
        
        def __init__(self, parent=None):
                QWidget.__init__(self, parent)
                self.resize(600,600)
                self._grid = 30
                self.setAcceptDrops(True)
                
        def addWidget(self, widget):
                """Connects a child widget's signals appropriately to make sure
                everything works as expected (redrawing of connections etc)"""
                # connect signals on the child
                QObject.connect(widget, SIGNAL("flipped()"), self, SLOT("update()"))
                QObject.connect(widget, SIGNAL("clicked(int,QPoint)"), self._childClickedLambda(widget))
                QObject.connect(widget, SIGNAL("connectionsChanged()"), self, SLOT("update()"))
                QObject.connect(widget, SIGNAL("moved(QPoint)"), self, SLOT("update()"))
                
        def _childClickedLambda(self, child):
                """Generates a lambda for calling the _childClicked function for a given
                child.
                
                _childClickedLambda(object) -> lambda
                """
                return (lambda dist, point: self._childClicked(child, dist, (point.x(),point.y())))
                
        def _childClicked(self, child, dist, point):
                """Handles a child click event."""
                for c in self.children():
                        c.unselect()
                child.select()
                self.emit(SIGNAL("childClicked"), child, dist, point)
             
        def dragEnterEvent(self, event):
                event.acceptProposedAction()
                
        def dropEvent(self, event):
                """Circuit widget accepts drag-drops from a list widget
                with items carrying particular texts."""
                try:
                        wtype = event.source().selectedItems()[0].text(0)
                except:
                        print "Not from a source list, can't drop this."
                        return
                        
                if wtype == 'Normal node':
                        n = NodeWidget(self)
                        n.move(self.snap(event.pos()))
                        n.show()
                        self.addWidget(n)
                elif wtype == 'Voltage source':
                        vs = VoltageSourceWidget(self)
                        vs.move(self.snap(event.pos()))
                        vs.show()
                        self.addWidget(vs)
                elif wtype == 'Current source':
                        cs = CurrentSourceWidget(self)
                        cs.move(self.snap(event.pos()))
                        cs.show()
                        self.addWidget(cs)
                elif wtype == 'Shockley diode':
                        d = ShockleyWidget(self)
                        d.move(self.snap(event.pos()))
                        d.show()
                        self.addWidget(d)
                elif wtype == 'Resistor':
                        r = ResistorWidget(self)
                        r.move(self.snap(event.pos()))
                        r.show()
                        self.addWidget(r)
                else:
                        print "dropped mimedata:", wtype
                        return
                event.setDropAction(Qt.CopyAction)
                event.accept()
                self.update()
                
        def snap(self, point):
                """Takes a given point, and snaps it based on the grid configuration
                for this widget.
                
                snap(QPoint) -> QPoint
                """
                x = round(float(point.x()) / self._grid) * self._grid
                y = round(float(point.y()) / self._grid) * self._grid
                return QPoint(x,y)
                
        def grid(self):
                """Returns the grid unit size.
                
                grid() -> int
                """
                return self._grid
                
        def setGrid(self, size):
                """Sets the grid unit size.
                
                setGrid(int) -> void
                """
                self._grid = size
                
        def mousePressEvent(self, event):
		# when we see a mouse click event it's not hitting one of our children
		# so deselect anything selected
		for c in self.children():
			c.unselect()
			c.update()
		
		self.update()
                
        def findConnections(self):
                """Finds all unique connections between all child widgets of this
                circuit widget. Used in painting to determine which links should be
                drawn.
                
                findConnections() -> list<connection>
                (for the signature of a connection, see ObjectWidget.connections()
                """
                found = []
                for c in self.children():
                        for cn in c.connections():
                                if len(cn)>0:
                                        if [cn[0],cn[1]] not in found and [cn[1],cn[0]] not in found:
                                                found.append(cn)
                return found
                
        def makeSleepy(self):
                sleepies,cons = self.makeSleepyWithHash()
                return (sleepies.values(), cons)
                
        def makeSleepyWithHash(self):
                sleepies = {}
                for c in self.children():
                        sleepies[c] = c.makeSleepy()
                        
                cons = []
                
                for c in self.findConnections():
                        nc = [(sleepies[c[0][0]], c[0][1]), \
                                (sleepies[c[1][0]], c[1][1])]
                        cons.append(nc)
                        
                return (sleepies, cons)
                
        def killChildren(self):
                for c in self.children():
                        c.deleteLater()
                self.update()
                
        def wakeUp(self, sleeptup):
                sleepies,cons = sleeptup
                
                wakies = {}
                for s in sleepies:
                        wakies[s] = s.create(self)
                        
                for c in cons:
                        firstwidget = wakies[c[0][0]]
                        firstpoint = c[0][1]
                        secondwidget = wakies[c[1][0]]
                        secondpoint = c[1][1]
                        firstwidget.connect(firstpoint, secondwidget, secondpoint)
                        
                self.update()
                # now we are awake
                
	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
                
                # draw grid
                painter.setPen(Qt.gray)
                for y in range(0, self.height(), self._grid):
                        painter.drawLine(QPoint(0, y), QPoint(self.width(), y))
                        
                for x in range(0, self.width(), self._grid):
                        painter.drawLine(QPoint(x, 0), QPoint(x, self.height()))
                        
                # draw connections
                painter.setPen(Qt.black)
                cnx = self.findConnections()
                for c in cnx:
                        point_a = QPoint(c[0][1][0],c[0][1][1]) + c[0][0].pos()
                        point_b = QPoint(c[1][1][0],c[1][1][1])+c[1][0].pos()
                        diff = point_a - point_b
                        
                        if abs(diff.x()) <= abs(diff.y()):
                                painter.drawLine(point_a, QPoint(point_b.x(), point_a.y()))
                                painter.drawLine(QPoint(point_b.x(), point_a.y()), point_b)
                        else:
                                painter.drawLine(point_a, QPoint(point_a.x(), point_b.y()))
                                painter.drawLine(QPoint(point_a.x(), point_b.y()), point_b)
                        
                
                
class SleepyNodeWidget():
        """A 'sleepy' partner to the node widget. This partner contains all of the 
        necessary information needed to recreate the node widget, minus connections,
        it is serializable, and also knows how to turn itself into an analysis object.
        
        C'tor: SleepyNodeWidget(QPoint, dict)
        """

        def __init__(self, location, attributes):
                self._location = (location.x(), location.y())
                self._attributes = attributes
                
        def create(self, parent):
                n = NodeWidget(parent)
                parent.addWidget(n)
                n.show()
                n.move(QPoint(self._location[0], self._location[1]))
                for a in self._attributes:
                        n[a] = self._attributes[a]
                return n
                
        def analyse(self, circuit):
                if not self._attributes['reference']:
                        ref = None
                else:
                        ref = float(self._attributes['reference'])
                        
                n = analysis.Node(nickname=self._attributes['nickname'], reference=ref)
                circuit.nodes.append(n)
                return n
                
                
class NodeWidget(ObjectWidget):
        """ObjectWidget subclass representing a simple circuit node."""
        
        def __init__(self, parent=None):
                ObjectWidget.__init__(self, parent)
                self._midPoint = (15,15)
                self._anchorPoints = [self._midPoint]
                self._connections = {self._midPoint: []}
                self._maxConnections = {self._midPoint: -1}
                
                self['nickname'] = 'n'
                self['reference'] = ''
                
                self.resize(30,30)
                
        def makeSleepy(self):
                return SleepyNodeWidget(self.pos(), self._attributes)
                
        def paintEvent(self, pevent):
                painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
                
                if self._orientation == 'v':
                        painter.rotate(90.0)
                        painter.translate(0.0, -30.0)
		
		painter.drawEllipse(QRect(self.width()/2 - 10,self.height()/2 - 10,20,20))
                
                path = QPainterPath()
                path.addEllipse(QRectF(self.width()/2 - 10,self.height()/2 - 10,20,20))
                painter.fillPath(path, QColor(40,40,40))
		
		painter.setPen(Qt.white)
		painter.drawText(QRect(0,0,self.width(),self.height()), Qt.AlignCenter | Qt.AlignTop, self['nickname'])
		
		self.drawSelectedOutline(painter)

class SleepyVoltageSourceWidget():
        def __init__(self, location, attributes, orientation):
                self._location = (location.x(), location.y())
                self._attributes = attributes
                self._orientation = orientation
                
        def create(self, parent):
                vs = VoltageSourceWidget(parent)
                parent.addWidget(vs)
                vs.move(QPoint(self._location[0], self._location[1]))
                for a in self._attributes:
                        vs[a] = self._attributes[a]
                if vs.orientation() != self._orientation: vs.flip()
                vs.show()
                return vs
                
        def analyse(self, circuit):
                n = analysis.IdealVoltageSource(nickname=self._attributes['nickname'], voltage=float(self._attributes['voltage']))
                circuit.components.append(n)
                return n

class VoltageSourceWidget(ObjectWidget):
        """ObjectWidget subclass representing a simple independent voltage source.
        
        Attributes:
                voltage
        
        *Widget changes size based on orientation.
        """
        def __init__(self, parent=None):
                ObjectWidget.__init__(self, parent)
                self.resize(90,30)
                self._posTerminal = (90,15)
                self._negTerminal = (0,15)
                
                self['nickname'] = 'vs'
                self['voltage'] = '0'
                
                self._anchorPoints = [self._posTerminal, self._negTerminal]
                self._connections = {self._posTerminal: [], self._negTerminal: []}
                self._maxConnections = {self._posTerminal: 1, self._negTerminal: 1}
                
                # event handlers
                QObject.connect(self, SIGNAL("flipped()"), self._flipped)
                
        def makeSleepy(self):
                return SleepyVoltageSourceWidget(self.pos(), self._attributes, self._orientation)
                
        def paintEvent(self, pevent):
                """Paints the widget."""
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
                
                if self._orientation == 'v':
                        painter.rotate(90.0)
                        painter.translate(0.0, -30.0)
                
                painter.drawEllipse(QRect(34, 4, 22, 22))
                painter.setFont(QFont('Sans serif', 7))
                painter.drawText(QRect(0,0,90,30), Qt.AlignCenter | Qt.AlignTop, "%s\n%sV" % (self['nickname'], self['voltage']))
                painter.drawLine(QPoint(0,15), QPoint(34,15))
                painter.drawLine(QPoint(56, 15), QPoint(90,15))
                painter.setFont(QFont('Sans serif', 11))
                painter.drawText(QRect(3,15,30,15), Qt.AlignLeft | Qt.AlignTop, "-")
                painter.drawText(QRect(56,15,30,15), Qt.AlignRight | Qt.AlignTop, "+")
                        
                painter.resetMatrix()
                        
                self.drawSelectedOutline(painter)
                
        def _flipped(self):
                """Called after the object is flipped, to resize and reorient its terminals."""
                if self._orientation == 'h':
                        self.resize(90,30)
                        newpos = (90,15)
                        newneg = (0,15)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                elif self._orientation == 'v':
                        self.resize(30,90)
                        
                        newneg = (15,0)
                        newpos = (15,90)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                # emit the moved signal, this forces our parent to redraw connections
                # kind of a hack, but it works.
                self.emit(SIGNAL("moved(QPoint)"), self.pos())
                self.update()
                
class SleepyCurrentSourceWidget():
        """A 'sleepy' partner to the current source widget. This partner contains all of the 
        necessary information needed to recreate the current source widget, minus connections, and
        it is serializable, and also knows how to turn itself into an analysis object.
        
        C'tor: SleepyCurrentSourceWidget(QPoint, dict, char)
        """
        
        def __init__(self, location, attributes, orientation):
                self._location = (location.x(), location.y())
                self._attributes = attributes
                self._orientation = orientation
                
        def create(self, parent):
                vs = CurrentSourceWidget(parent)
                parent.addWidget(vs)
                vs.move(QPoint(self._location[0], self._location[1]))
                for a in self._attributes:
                        vs[a] = self._attributes[a]
                if vs.orientation() != self._orientation: vs.flip()
                vs.show()
                return vs
                
        def analyse(self, circuit):
                n = analysis.IdealCurrentSource(nickname=self._attributes['nickname'], current=float(self._attributes['current']))
                circuit.components.append(n)
                return n

class CurrentSourceWidget(ObjectWidget):
        """ObjectWidget subclass representing a simple independent current source.
        
        Attributes:
                current
        
        *Widget changes size based on orientation.
        """
        def __init__(self, parent=None):
                ObjectWidget.__init__(self, parent)
                self.resize(90,30)
                self._posTerminal = (90,15)
                self._negTerminal = (0,15)
                
                self['nickname'] = 'cs'
                self['current'] = '0'
                
                self._anchorPoints = [self._posTerminal, self._negTerminal]
                self._connections = {self._posTerminal: [], self._negTerminal: []}
                self._maxConnections = {self._posTerminal: 1, self._negTerminal: 1}
                
                # event handlers
                QObject.connect(self, SIGNAL("flipped()"), self._flipped)
                
        def makeSleepy(self):
                return SleepyCurrentSourceWidget(self.pos(), self._attributes, self._orientation)
                
        def paintEvent(self, pevent):
                """Paints the widget."""
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
                
                if self._orientation == 'v':
                        painter.rotate(90.0)
                        painter.translate(0.0, -30.0)
                
                painter.drawEllipse(QRect(34, 4, 22, 22))
                painter.setFont(QFont('Sans serif', 7))
                painter.drawText(QRect(0,0,90,30), Qt.AlignCenter | Qt.AlignTop, "%s\n%sA" % (self['nickname'], self['current']))
                painter.drawLine(QPoint(0,15), QPoint(34,15))
                painter.drawLine(QPoint(56, 15), QPoint(90,15))
                
                path = QPainterPath()
                path.moveTo(38, 15)
                path.lineTo(53, 15)
                path.lineTo(48, 10)
                path.moveTo(53, 15)
                path.lineTo(48, 20)
                painter.drawPath(path)
                        
                painter.resetMatrix()
                        
                self.drawSelectedOutline(painter)
                
        def _flipped(self):
                """Called after the object is flipped, to resize and reorient its terminals."""
                if self._orientation == 'h':
                        self.resize(90,30)
                        newpos = (90,15)
                        newneg = (0,15)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                elif self._orientation == 'v':
                        self.resize(30,90)
                        
                        newneg = (15,0)
                        newpos = (15,90)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                # emit the moved signal, this forces our parent to redraw connections
                # kind of a hack, but it works.
                self.emit(SIGNAL("moved(QPoint)"), self.pos())
                self.update()
                
class SleepyResistorWidget():
        def __init__(self, location, attributes, orientation):
                self._location = (location.x(), location.y())
                self._attributes = attributes
                self._orientation = orientation
                
        def create(self, parent):
                r = ResistorWidget(parent)
                parent.addWidget(r)
                r.move(QPoint(self._location[0], self._location[1]))
                for a in self._attributes:
                        r[a] = self._attributes[a]
                if r.orientation() != self._orientation: r.flip()
                r.show()
                return r
                
        def analyse(self, circuit):
                n = analysis.IdealResistor(nickname=self._attributes['nickname'], resistance=int(self._attributes['resistance']))
                circuit.components.append(n)
                return n

class ResistorWidget(ObjectWidget):
        def __init__(self, parent=None):
                ObjectWidget.__init__(self, parent)
                self.resize(90,30)
                self._firstTerminal = (90,15)
                self._secondTerminal = (0,15)
                
                self['nickname'] = 'r'
                self['resistance'] = '0'
                
                self._anchorPoints = [self._firstTerminal, self._secondTerminal]
                self._connections = {self._firstTerminal: [], self._secondTerminal: []}
                self._maxConnections = {self._firstTerminal: 1, self._secondTerminal: 1}
                
                # event handlers
                QObject.connect(self, SIGNAL("flipped()"), self._flipped)
                
        def makeSleepy(self):
                return SleepyResistorWidget(self.pos(), self._attributes, self._orientation)
                
        def paintEvent(self, pevent):
                """Paints the widget."""
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
                
                if self._orientation == 'v':
                        painter.rotate(90.0)
                        painter.translate(0.0, -30.0)
                
                path = QPainterPath()
                path.moveTo(0,15)
                path.lineTo(30,15)
                path.lineTo(34,5)
                path.lineTo(38,20)
                path.lineTo(42,5)
                path.lineTo(46,20)
                path.lineTo(50,5)
                path.lineTo(54,20)
                path.lineTo(58,5)
                path.lineTo(60,15)
                path.lineTo(90,15)
                painter.drawPath(path)
                        
                painter.setFont(QFont('Sans serif', 7))
                painter.drawText(QRect(0,0,90,30), Qt.AlignCenter | Qt.AlignBottom, "%s: %s" % (self['nickname'], self['resistance']))
                
                painter.resetMatrix()
                        
                self.drawSelectedOutline(painter)
                
        def _flipped(self):
                """Called after the object is flipped, to resize and reorient its terminals."""
                if self._orientation == 'h':
                        self.resize(90,30)
                        newfirst = (90,15)
                        newsecond = (0,15)
                        self._anchorPoints = [newsecond, newfirst]
                        self._connections = {newsecond: self._connections[self._secondTerminal], \
                                                newfirst: self._connections[self._firstTerminal]}
                        self._maxConnections = {newsecond: 1, newfirst: 1}
                        self._secondTerminal = newsecond
                        self._firstTerminal = newfirst
                        
                elif self._orientation == 'v':
                        self.resize(30,90)
                        
                        newsecond = (15,0)
                        newfirst = (15,90)
                        self._anchorPoints = [newsecond, newfirst]
                        self._connections = {newsecond: self._connections[self._secondTerminal], \
                                                newfirst: self._connections[self._firstTerminal]}
                        self._maxConnections = {newsecond: 1, newfirst: 1}
                        self._secondTerminal = newsecond
                        self._firstTerminal = newfirst
                        
                # emit the moved signal, this forces our parent to redraw connections
                # kind of a hack, but it works.
                self.emit(SIGNAL("moved(QPoint)"), self.pos())
                self.update()
                
class SleepyShockleyWidget():
        def __init__(self, location, attributes, orientation):
                self._location = (location.x(), location.y())
                self._attributes = attributes
                self._orientation = orientation
                
        def create(self, parent):
                vs = ShockleyWidget(parent)
                parent.addWidget(vs)
                vs.move(QPoint(self._location[0], self._location[1]))
                for a in self._attributes:
                        vs[a] = self._attributes[a]
                if vs.orientation() != self._orientation: vs.flip()
                vs.show()
                return vs
                
        def analyse(self, circuit):
                n = analysis.ShockleyDiode(nickname=self._attributes['nickname'],  \
                                        saturation_current=float(self._attributes['saturation_current']), \
                                        thermal_voltage=float(self._attributes['thermal_voltage']), \
                                        e_coeff=float(self._attributes['e_coeff']))
                circuit.components.append(n)
                return n

class ShockleyWidget(ObjectWidget):
        """ObjectWidget subclass representing a shockley diode.
        
        Attributes:
                saturation_current=1e-12, thermal_voltage=25.85e-03, e_coeff=1.00
        
        *Widget changes size based on orientation.
        """
        def __init__(self, parent=None):
                ObjectWidget.__init__(self, parent)
                self.resize(90,30)
                self._posTerminal = (90,15)
                self._negTerminal = (0,15)
                
                self['nickname'] = 'n'
                self['saturation_current'] = '1e-12'
                self['thermal_voltage'] = '25.85e-3'
                self['e_coeff'] = '1.00'
                
                self._anchorPoints = [self._posTerminal, self._negTerminal]
                self._connections = {self._posTerminal: [], self._negTerminal: []}
                self._maxConnections = {self._posTerminal: 1, self._negTerminal: 1}
                
                # event handlers
                QObject.connect(self, SIGNAL("flipped()"), self._flipped)
                
        def makeSleepy(self):
                return SleepyShockleyWidget(self.pos(), self._attributes, self._orientation)
                
        def paintEvent(self, pevent):
                """Paints the widget."""
                painter = QPainter(self)
                painter.setRenderHint(QPainter.Antialiasing)
		painter.setPen(Qt.black)
                
                if self._orientation == 'v':
                        painter.rotate(90.0)
                        painter.translate(0.0, -30.0)
                
                painter.setFont(QFont('Sans serif', 7))
                painter.drawText(QRect(0,0,90,30), Qt.AlignCenter | Qt.AlignTop, "%s" % (self['nickname']))
                
                path = QPainterPath()
                path.moveTo(0,15)
                path.lineTo(33,15)
                path.moveTo(33,5)
                path.lineTo(33,25)
                path.lineTo(55,15)
                path.lineTo(33,5)
                path.moveTo(55,5)
                path.lineTo(55,25)
                path.moveTo(55,15)
                path.lineTo(90,15)
                painter.drawPath(path)
                        
                painter.resetMatrix()
                        
                self.drawSelectedOutline(painter)
                
        def _flipped(self):
                """Called after the object is flipped, to resize and reorient its terminals."""
                if self._orientation == 'h':
                        self.resize(90,30)
                        newpos = (90,15)
                        newneg = (0,15)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                elif self._orientation == 'v':
                        self.resize(30,90)
                        
                        newneg = (15,0)
                        newpos = (15,90)
                        self._anchorPoints = [newpos, newneg]
                        self._connections = {newpos: self._connections[self._posTerminal], \
                                                newneg: self._connections[self._negTerminal]}
                        self._maxConnections = {newpos: 1, newneg: 1}
                        self._posTerminal = newpos
                        self._negTerminal = newneg
                        
                # emit the moved signal, this forces our parent to redraw connections
                # kind of a hack, but it works.
                self.emit(SIGNAL("moved(QPoint)"), self.pos())
                self.update()
