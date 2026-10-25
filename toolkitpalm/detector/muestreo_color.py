# -*- coding: utf-8 -*-
"""
Lectura del color medio de la ortofoto alrededor de unos puntos.

Es solo lectura de la imagen: qué puntos leer y qué hacer con los colores lo
decide el servidor de ToolkitPalm.
"""
import logging
import math

from osgeo import gdal, osr

logger = logging.getLogger(__name__)

LADO_LECTURA = 24      # píxeles del lado de la ventana leída (se reduce al leer)


def colores_medios(ruta, wkt_puntos, puntos, radio):
    """[r, g, b] medio en un círculo de `radio` metros alrededor de cada punto, o None."""
    ds = gdal.Open(ruta)
    if ds is None or ds.RasterCount < 3:
        return None
    bandas = [ds.GetRasterBand(i) for i in (1, 2, 3)]
    gt = ds.GetGeoTransform()
    ancho, alto = ds.RasterXSize, ds.RasterYSize
    transformar = None
    wkt_raster = ds.GetProjection()
    if wkt_puntos and wkt_raster:
        origen, destino = osr.SpatialReference(), osr.SpatialReference()
        origen.ImportFromWkt(wkt_puntos)
        destino.ImportFromWkt(wkt_raster)
        for sr in (origen, destino):
            if hasattr(sr, "SetAxisMappingStrategy"):
                sr.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        if not origen.IsSame(destino):
            transformar = osr.CoordinateTransformation(origen, destino)

    salida = []
    for x, y in puntos:
        if transformar is not None:
            x, y = transformar.TransformPoint(x, y)[:2]
        px, py = (x - gt[0]) / gt[1], (y - gt[3]) / gt[5]
        r = radio / abs(gt[1])
        x0, y0 = max(0, int(math.floor(px - r))), max(0, int(math.floor(py - r)))
        x1, y1 = min(ancho, int(math.ceil(px + r))), min(alto, int(math.ceil(py + r)))
        w, h = x1 - x0, y1 - y0
        if w <= 0 or h <= 0:
            salida.append(None)
            continue
        bw, bh = min(w, LADO_LECTURA), min(h, LADO_LECTURA)
        rgb = [b.ReadAsArray(x0, y0, w, h, buf_xsize=bw, buf_ysize=bh).astype("float64") for b in bandas]
        validos = (rgb[0] + rgb[1] + rgb[2]) > 0
        if not validos.any():
            salida.append(None)
            continue
        salida.append([float(c[validos].mean()) for c in rgb])
    return salida
