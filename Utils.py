

def create_GeoJson(lonlat_list:list)->str:
    '''
    input: list of [lon, lat]
    output: geojson string

    should I expose appearance variables?
    '''
    assert type(lonlat_list) == list, "latlon must be list"
    assert type(lonlat_list[0]) == list, "content of latlon must be list"

    s1 = '''
    {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {
          "stroke": "#ff3300",
          "stroke-width": 10,
          "stroke-opacity": 0.2,
          "fill": "#00ffcc",
          "fill-opacity": 0.2,
          "color": "#3fff33b2"
        },
        "geometry": {
          "type": "Polygon",
          "coordinates": [
    '''
#     s2 = '''
#         ]
#       }
#     }
#   ]
# }
#     '''
#     return s1 + str(lonlat_list) + s2
    s2 = '''
        ]
        }
        }
    ,
    {
      "type": "Feature",
      "properties": {
        "stroke": "#0000ff",
        "stroke-width": 2.1,
        "stroke-opacity": 0.2,
        "fill": "#0000ff",
        "fill-opacity": 0.2
      },
      "geometry": {
        "type": "LineString",
        "coordinates": 
    '''    
    s3 = '''
        
        }
        }
      ]
    }
    '''
    return s1 + str(lonlat_list) + s2 + str(lonlat_list) + s3
    
