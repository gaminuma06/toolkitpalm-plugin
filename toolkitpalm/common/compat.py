# -*- coding: utf-8 -*-
"""Tipos de geometría que sirven igual en QGIS 3 y QGIS 4 (Qt6)."""
from qgis.core import Qgis, QgsWkbTypes

if hasattr(Qgis, "GeometryType"):
    GEOM_PUNTO = Qgis.GeometryType.Point
    GEOM_POLIGONO = Qgis.GeometryType.Polygon
else:
    GEOM_PUNTO = QgsWkbTypes.PointGeometry
    GEOM_POLIGONO = QgsWkbTypes.PolygonGeometry
