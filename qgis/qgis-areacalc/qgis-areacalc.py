
##Areacalc=name
##Vector=group

from qgis.core import *
from qgis.utils import *

from processing.tools.vector import VectorWriter
from math import sqrt

from PyQt4.QtCore import *
from PyQt4.QtGui import *


def tav(x1,y1,x2,y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )
    
# coordinate and distance precision
prec = 2  
    
# input reteg  

#inputLayer = processing.getObject(poly)
inputLayer = iface.activeLayer()

if inputLayer.wkbType()==QGis.WKBPolygon:


    # adding pint layer for the points
    fields = QgsFields()
    fields.append(QgsField("id", QVariant.Int))
    fields.append(QgsField("desc", QVariant.String))

    # only for the active layers seletion...

    selection = inputLayer.selectedFeatures()

    # if there are selected features...

    if len(selection) > 0:
        
        # create output layer
        outputLayer = QgsVectorLayer("Point?crs="+inputLayer.crs().authid()+"&field=ptid:string(80)&field=desc:string(80)","pontok","memory")

        # registering
        QgsMapLayerRegistry.instance().addMapLayer(outputLayer)

        # open for editing
        outputLayer.startEditing()    

        # this will be the new point feature
        outFeat = QgsFeature()

        numpts = 0

        for f in selection:
            
            print ""
            print "Are calculation:" , f.id()+1
            
            geom = f.geometry()
            
            x = geom.asPolygon()

            nring = 0
            for ring in x:
                nring += 1
                
                print ""
                print "  Ring:", nring
                print  "     #      PTID          X              Y          Dist"
                
                for i in range(0, len(ring)-1):
                    numpts += 1
                    dist = tav(ring[i].x(), ring[i].y(), ring[i+1].x(), ring[i+1].y() )
                    
                    fmt = "  %6d %6d %14."+str(prec)+"f %14."+str(prec)+"f %14."+str(prec)+"f"                    
                    
                    print fmt % (i+1, numpts, ring[i].x(), ring[i].y(), dist)
                    
                    # adding point to the output layer
                    outGeom = QgsGeometry.fromPoint(QgsPoint(ring[i].x(),ring[i].y()))
                    outFeat.setAttributes([str(numpts), ""])  # pontszam, jel
                    outFeat.setGeometry(outGeom)
                    outputLayer.dataProvider().addFeatures([outFeat])
                    
                    
                p = QgsGeometry.fromPolygon([ring])
                
                ter = p.area()
                                
                if nring > 1:
                    ter *= -1
                    
                fmt = "  Ring area = %0."+str(prec)+"f m2, %0."+str(prec)+"f ha"
                print fmt % (ter,ter/10000)
                fmt = "  Ring perimeter = %0."+str(prec)+"f m"
                print fmt % ( p.length() ) 
            
            print ""
            print "Summary:"    
            fmt = "Area = %0."+str(prec)+"f m2, %0."+str(prec)+"f ha"
            print fmt % (geom.area(),geom.area()/10000)
            fmt = "Perimeter = %0."+str(prec)+"f m"
            print fmt % ( geom.length() )
            
        # finish, save changes  
        outputLayer.commitChanges()
        
    else:
        QMessageBox.information(None, "Areacalc", "Nothing selected on the active layer!") 

else:
    QMessageBox.information(None, "Areacalc", "Layer type is not polygon!") 

QMessageBox.information(None, "Areacalc", "Finished") 
