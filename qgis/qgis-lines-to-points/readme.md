qgis-lines-to-points
====================

QGIS Creating points from lines with length and rotation fields

How it works?
-------------

It needs two layers:
- lines: vector layer with lines
- points: vector layer with points
  - fields:
    - length: decimal, the length of the line
    - rotate: decimal, clockwise rotation from north in degrees

The script creates points on points layer at the first vertex of the lines and fills the specified length and rotation fields.

Please refresh after processing!

Install
-------

Just copy to the ~/.qgis2/processing/scripts directory and restart QGIS

More info at: http://falu.me
