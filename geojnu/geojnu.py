"""Main module."""

import ipyleaflet

class map(ipyleaflet.Map):
    def __init__(self,center=[25,75],zoom=5,height="600px", **kwargs):
        super().__init__(center=center,zoom=zoom,**kwargs)
        self.layout.height = height
        
    def add_basemap(self, basemap="OpenStreetMap"):
        
        basemaps = {
            "OpenStreetMap": ipyleaflet.basemaps.OpenStreetMap.Mapnik,
            "OpenTopoMap": ipyleaflet.basemaps.OpenTopoMap,
        }
        if basemap in basemaps:
            tile_layer= basemaps[basemap]
            url=tile_layer["url"]
            self.add_layer(ipyleaflet.TileLayer(url=url, name=basemap, attribution=tile_layer["attribution"]))
        else:
            url=eval(f"ipyleaflet.basemaps.{basemap}").build_url()
            layer=ipyleaflet.TileLayer(url=url, name=basemap, attribution=eval(f"ipyleaflet.basemaps.{basemap}.attribution"))   
            self.add_layer(layer)
            
    def google_map(self,map_type="roadmap"):
        map_types = {
            "roadmap": "m",
            "satellite": "s",
            "hybrid": "y",
            "terrain": "p"
        }
        map_type = map_types[map_type.lower()]
        url=f"https://mt{map_type}.google.com/vt/lyrs={map_type}&x={{x}}&y={{y}}&z={{z}}&s=Galileo"
        layer=ipyleaflet.TileLayer(url=url, name="Google Map", attribution="Google")
        self.add_layer(layer)    
