"""Main module."""

import os
import ipyleaflet


class map(ipyleaflet.Map):
    def __init__(self, center=[25, 75], zoom=5, height="600px", **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.layout.height = height
        self.scroll_wheel_zoom = True

    def add_basemap(self, basemap="OpenStreetMap"):

        basemaps = {
            "OpenStreetMap": ipyleaflet.basemaps.OpenStreetMap.Mapnik,
            "OpenTopoMap": ipyleaflet.basemaps.OpenTopoMap,
        }
        if basemap in basemaps:
            tile_layer = basemaps[basemap]
            url = tile_layer["url"]
            self.add_layer(
                ipyleaflet.TileLayer(
                    url=url, name=basemap, attribution=tile_layer["attribution"]
                )
            )
        else:
            url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
            layer = ipyleaflet.TileLayer(
                url=url,
                name=basemap,
                attribution=eval(f"ipyleaflet.basemaps.{basemap}.attribution"),
            )
            self.add_layer(layer)

    def google_map(self, map_type="roadmap"):
        map_types = {"roadmap": "m", "satellite": "s", "hybrid": "y", "terrain": "p"}
        map_type = map_types[map_type.lower()]
        url = f"https://mt{map_type}.google.com/vt/lyrs={map_type}&x={{x}}&y={{y}}&z={{z}}&s=Galileo"
        layer = ipyleaflet.TileLayer(url=url, name="Google Map", attribution="Google")
        self.add_layer(layer)

    def add_geojson(self, data,zoom_to_layer=True,hover_style=None, **kwargs):
        import geopandas as gpd
        
        if hover_style is None:
            hover_style={"color": "white", "dashArray": "0", "fillOpacity": 0.5}
        
        if isinstance(data, str):    
            gdf=gpd.read_file(data)
            geojson = gdf.__geo_interface__
        elif isinstance(data, dict):
            geojson = data
        layer = ipyleaflet.GeoJSON(data=geojson,hover_style=hover_style, **kwargs)
        self.add_layer(layer)
        
        if zoom_to_layer:
            bounds=gdf.total_bounds
            self.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    def add_shp(self, data, **kwargs):
        import geopandas as gpd
         
        gdf=gpd.read_file(data)
        gdf= gdf.to_crs(epsg=4326)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, **kwargs)    
        
    def add_gdf(self,gdf, **kwargs):
        
        gdf= gdf.to_crs(epsg=4326)   
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, **kwargs)
        
    def add_vector(self, data, **kwargs):
        import geopandas as gpd
        
        if isinstance(data, str):  
            gdf=gpd.read_file(data)
            self.add_gdf(gdf, **kwargs)
        elif isinstance(data, gpd.GeoDataFrame):
            self.add_gdf(data, **kwargs)
        elif isinstance(data, dict):
            self.add_geojson(data, **kwargs)
        else:
            raise ValueError("data must be a file path or a GeoDataFrame or a dict")