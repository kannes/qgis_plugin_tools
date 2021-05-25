import enum

__copyright__ = "Copyright 2020-2021, Gispo Ltd"
__license__ = "GPL version 3"
__email__ = "info@gispo.fi"
__revision__ = "$Format:%H$"

import logging
from typing import List, Optional, Set, Union

from qgis.core import (
    QgsExpression,
    QgsExpressionContext,
    QgsExpressionContextScope,
    QgsExpressionContextUtils,
    QgsFeature,
    QgsMapLayer,
    QgsVectorLayer,
    QgsWkbTypes,
)

from .custom_logging import bar_msg
from .exceptions import QgsPluginExpressionException
from .resources import plugin_name

try:
    from qgis.core import QgsUnitTypes, QgsVectorLayerTemporalProperties
except ImportError:
    QgsVectorLayerTemporalProperties = QgsUnitTypes = None

LOGGER = logging.getLogger(plugin_name())

POINT_TYPES = {
    QgsWkbTypes.Point,
    QgsWkbTypes.PointGeometry,
    QgsWkbTypes.PointM,
    QgsWkbTypes.Point25D,
    QgsWkbTypes.PointZ,
    QgsWkbTypes.PointZM,
    QgsWkbTypes.MultiPoint,
    QgsWkbTypes.MultiPoint25D,
    QgsWkbTypes.MultiPointM,
    QgsWkbTypes.MultiPointZ,
    QgsWkbTypes.MultiPointZM,
}

LINE_TYPES = {
    QgsWkbTypes.LineGeometry,
    QgsWkbTypes.LineString,
    QgsWkbTypes.LineString25D,
    QgsWkbTypes.LineStringM,
    QgsWkbTypes.LineStringZ,
    QgsWkbTypes.LineStringZM,
    QgsWkbTypes.MultiLineString,
    QgsWkbTypes.MultiLineString25D,
    QgsWkbTypes.MultiLineStringM,
    QgsWkbTypes.MultiLineStringZ,
    QgsWkbTypes.MultiLineStringZM,
}

POLYGON_TYPES = {
    QgsWkbTypes.Polygon,
    QgsWkbTypes.Polygon25D,
    QgsWkbTypes.PolygonGeometry,
    QgsWkbTypes.PolygonM,
    QgsWkbTypes.PolygonZ,
    QgsWkbTypes.PolygonZM,
    QgsWkbTypes.MultiPolygon,
    QgsWkbTypes.CurvePolygon,
}


@enum.unique
class LayerType(enum.Enum):
    Point = {"wkb_types": POINT_TYPES}
    Line = {"wkb_types": LINE_TYPES}
    Polygon = {"wkb_types": POLYGON_TYPES}
    Unknown = {}  # type: ignore

    @staticmethod
    def from_layer(layer: QgsVectorLayer) -> "LayerType":
        for l_type in LayerType:
            if layer.wkbType() in l_type.wkb_types:
                return l_type
        return LayerType.Unknown

    @property
    def wkb_types(self) -> Set[QgsWkbTypes.GeometryType]:
        return self.value["wkb_types"]


def set_temporal_settings(
    layer: QgsVectorLayer,
    dt_field: str,
    time_step: int,
    unit: "QgsUnitTypes.TemporalUnit" = None,
) -> None:
    """
    Set temporal settings for vector layer temporal range for raster layer
    :param layer: raster layer
    :param dt_field: name of the date time field
    :param time_step: time step in some QgsUnitTypes.TemporalUnit
    :param unit: QgsUnitTypes.TemporalUnit
    """
    if unit is None:
        unit = QgsUnitTypes.TemporalMinutes
    mode = QgsVectorLayerTemporalProperties.ModeFeatureDateTimeInstantFromField
    tprops: QgsVectorLayerTemporalProperties = layer.temporalProperties()
    tprops.setMode(mode)
    tprops.setStartField(dt_field)
    tprops.setFixedDuration(time_step)
    tprops.setDurationUnits(unit)
    tprops.setIsActive(True)


def evaluate_expressions(
    exp: QgsExpression,
    feature: Optional[QgsFeature] = None,
    layer: Optional[QgsMapLayer] = None,
    context_scopes: Optional[List[QgsExpressionContextScope]] = None,
) -> Union[bool, int, str, float, None]:
    """
    Evaluate a QGIS expression
    :param exp: QGIS expression
    :param feature: Optional QgsFeature
    :param layer: Optional QgsMapLayer
    :param context_scopes: Optional list of QgsExpressionContextScopes
    :return: evaluated value of the expression
    """
    context = QgsExpressionContext()
    scopes = context_scopes if context_scopes else []

    if layer:
        # noinspection PyArgumentList
        scopes.append(QgsExpressionContextUtils.layerScope(layer))
    context.appendScopes(scopes)
    if feature:
        context.setFeature(feature)

    value = exp.evaluate(context)
    if exp.hasParserError():
        LOGGER.error(exp.parserErrorString())
        raise QgsPluginExpressionException(bar_msg=bar_msg(exp.parserErrorString()))

    if exp.hasEvalError():
        raise QgsPluginExpressionException(bar_msg=bar_msg(exp.evalErrorString()))
    return value
