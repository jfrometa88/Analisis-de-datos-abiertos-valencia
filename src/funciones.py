import geopandas
import pandas as pd
import matplotlib.pyplot as plt
import ast
from shapely.geometry import Polygon,Point
import numpy as np

def convert_to_dict(dict_string):
    """
    Converts a string representation of a dictionary into an actual Python dictionary.
    
    Parameters
    ----------
    dict_string : str
        A string containing a dictionary in Python syntax (e.g., '{"key": "value"}').
    
    Returns
    -------
    dict
        A Python dictionary parsed from the input string.
    
    Raises
    ------
    ValueError
        If the input string is not a valid dictionary representation.
    SyntaxError
        If the input string has invalid syntax.
    
    Examples
    --------
    >>> dict_str = '{"name": "Alice", "age": 30}'
    >>> convert_to_dict(dict_str)
    {'name': 'Alice', 'age': 30}
    
    >>> invalid_str = '{"name": "Alice", "age": 30'  # Missing closing brace
    >>> convert_to_dict(invalid_str)
    Traceback (most recent call last):
        ...
    SyntaxError: unexpected EOF while parsing
    """
    dict_converted = ast.literal_eval(dict_string)
    return dict_converted

def convert_to_list_Polygon_type(geo_dict_serie):
    """
    Converts a series of GeoJSON-like dictionary objects into a list of Shapely Polygon objects.
    
    Parameters
    ----------
    geo_dict_serie : iterable
        An iterable (e.g., list, Pandas Series) containing dictionary objects in GeoJSON format.
        Each dictionary must have a key 'coordinates' with a list of coordinate pairs defining
        a polygon (e.g., {'type': 'Polygon', 'coordinates': [[[x1, y1], [x2, y2], ...]]}).
    
    Returns
    -------
    list
        A list of Shapely Polygon objects created from the input dictionaries.
    
    Raises
    ------
    KeyError
        If a dictionary in the input does not contain the key 'coordinates'.
    ValueError
        If the 'coordinates' key does not contain valid data for constructing a Polygon.
    
    Examples
    --------
    >>> from shapely.geometry import Polygon
    >>> geo_dict_serie = [
    ...     {'type': 'Polygon', 'coordinates': [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
    ...     {'type': 'Polygon', 'coordinates': [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]]}
    ... ]
    >>> convert_to_list_Polygon_type(geo_dict_serie)
    [<shapely.geometry.polygon.Polygon object at 0x...>, 
     <shapely.geometry.polygon.Polygon object at 0x...>]
    
    >>> invalid_geo_dict_serie = [{'type': 'Polygon', 'coordinates': 'invalid_data'}]
    >>> convert_to_list_Polygon_type(invalid_geo_dict_serie)
    Traceback (most recent call last):
        ...
    ValueError: The coordinates data is not valid for constructing a Polygon.
    """
    geo_info_poly_list = []
    for i in geo_dict_serie:
        # Construct a Shapely Polygon from the coordinates
        polygon = Polygon(i['coordinates'][0])
        geo_info_poly_list.append(polygon)
    return geo_info_poly_list

def convert_to_list_Point_type(lat_long_serie):
    """
    Convert a series of geographic data (list, tuple, or dict) into a list of Shapely Point objects.
    
    Parameters:
        lat_long_serie (list): A list containing geographic data. Each element should be:
            - A list or tuple of coordinates (e.g., [longitude, latitude] or (longitude, latitude)).
            - A dictionary with a 'coordinates' key (e.g., {'coordinates': [longitude, latitude]}).
            
    Returns:
        list: A list of Shapely Point objects created from the input geographic data.
        
    Raises:
        ValueError: If the input data is empty or contains unsupported types.
    """
    if len(lat_long_serie)==0 :
        raise ValueError("The input data is empty. Please provide a valid list of geographic data.")
    
    geo_info_point_list = []
    for item in lat_long_serie:
        if isinstance(item, (list, tuple,)):
            point = Point(item)
        elif isinstance(item, dict) and 'coordinates' in item:
            point = Point(item['coordinates'])
        else:
            raise ValueError(f"Unsupported data format: {item}. Expected list, tuple, or dict with 'coordinates'.")
        
        geo_info_point_list.append(point)
    
    return geo_info_point_list

def process_geo_data(df, geo_column, type='Polygon'):
    """
    Procesa datos geográficos de un dataframe y retorna una GeoSerie.
    """
    try:
        geo_info = df[geo_column].apply(convert_to_dict)
        if type == 'Polygon':
            geo_info = convert_to_list_Polygon_type(geo_info)
        elif type == 'Point':
            geo_info = convert_to_list_Point_type(geo_info)
        else:
            raise ValueError("Unsupported geometry type")
    except:
        geo_info = df[geo_column]
        if type == 'Polygon':
            geo_info = convert_to_list_Polygon_type(geo_info)
        elif type == 'Point':
            geo_info = convert_to_list_Point_type(geo_info)
        else:
            raise ValueError("Unsupported geometry type")
    
    geo_column = geopandas.GeoSeries(geo_info)
    return geo_column

