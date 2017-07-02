##[falu]=group
##Lines to Points=name
##Line_layer=vector
##Point_layer=vector
##Lenght_field=field Point_layer
##Rotate_field=field Point_layer
##Empty_point_layer=boolean

from qgis.core import *
import qgis.utils
import qgis.gui
import math 

vlayer = processing.getObject(Line_layer)
player = processing.getObject(Point_layer)

length_field_index = player.fieldNameIndex(Lenght_field)
rotate_field_index = player.fieldNameIndex(Rotate_field)

#delete features from point layer
if Empty_point_layer == True:
    progress.setText('Delete features from point layer...')
    caps = player.dataProvider().capabilities()
    iter = player.getFeatures()
    for feat in iter:
        if caps & QgsVectorDataProvider.DeleteFeatures:
            res = player.dataProvider().deleteFeatures([ feat.id() ])

#iterator
progress.setText('Processing...')
iter = vlayer.getFeatures()
for feature in iter:

    geom = feature.geometry()

    if geom.type() == QGis.Line:
        lin = geom.asPolyline()
      
        if len(lin) != 2:
            progress.setText('Error: More than 2 vertex! ID: %d' % feature.id() )
      
        x1 = lin[0].x()
        y1 = lin[0].y()
      
        x2 = lin[1].x()
        y2 = lin[1].y()
      
        dx = x2 - x1
        dy = y2 - y1
      
        #calc lenght:
        #plength = math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
        plength = feature.geometry().length()

        #calc rotation:
        if dy == 0:
            #avoid divide by zero
            dy = 0.0000000001
          
        protate = 90 - math.atan2(dy, dx) * 180 / math.pi
        if (protate < 0):
            protate += 360
      
        caps = player.dataProvider().capabilities()
        if caps & QgsVectorDataProvider.AddFeatures:
            feat = QgsFeature()
            feat.initAttributes(256)
            feat.setAttribute(rotate_field_index, protate)
            feat.setAttribute(length_field_index, plength)
            feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(x1, y1)))
            (res, outFeats) = player.dataProvider().addFeatures( [ feat ] )
            if res == False:
                #something is wrong
                progress.setText('Error: Point adding failed!')

    else:
        progress.setText('Error: Not supported geometry! ID: %d' % feature.id() )

progress.setText('Finished.')
