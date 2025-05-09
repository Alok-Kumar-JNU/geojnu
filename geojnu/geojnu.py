"""Main module."""

import os
import ipyleaflet
import localtileserver


class map(ipyleaflet.Map):
    """A custom map class extending ipyleaflet.Map with additional functionality.

    Args:
        center (list, optional): The initial center of the map as [latitude, longitude]. Defaults to [25, 75].
        zoom (int, optional): The initial zoom level of the map. Defaults to 5.
        height (str, optional): The height of the map in pixels. Defaults to "600px".
        **kwargs: Additional keyword arguments passed to the ipyleaflet.Map constructor.
    """

    def __init__(self, center=[25, 75], zoom=5, height="600px", **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.layout.height = height
        self.scroll_wheel_zoom = True

    def add_basemap(self, basemap="OpenStreetMap"):
        """Adds a basemap to the map.

        Args:
            basemap (str, optional): The name of the basemap to add. Defaults to "OpenStreetMap".
                Supported basemaps: "OpenStreetMap", "OpenTopoMap".
        """
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
        """Adds a Google Map layer to the map.

        Args:
            map_type (str, optional): The type of Google Map to add. Defaults to "roadmap".
                Supported types: "roadmap", "satellite", "hybrid", "terrain".
        """
        map_types = {"roadmap": "m", "satellite": "s", "hybrid": "y", "terrain": "p"}
        map_type = map_types[map_type.lower()]
        url = f"https://mt{map_type}.google.com/vt/lyrs={map_type}&x={{x}}&y={{y}}&z={{z}}&s=Galileo"
        layer = ipyleaflet.TileLayer(url=url, name="Google Map", attribution="Google")
        self.add_layer(layer)

    def add_geojson(self, data, zoom_to_layer=True, hover_style=None, **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (str or dict): The GeoJSON data or file path to the GeoJSON file.
            zoom_to_layer (bool, optional): Whether to zoom to the layer's bounds. Defaults to True.
            hover_style (dict, optional): The style to apply when hovering over features. Defaults to None.
            **kwargs: Additional keyword arguments passed to the ipyleaflet.GeoJSON constructor.
        """
        import geopandas as gpd

        if hover_style is None:
            hover_style = {"color": "white", "dashArray": "0", "fillOpacity": 0.5}

        if isinstance(data, str):
            gdf = gpd.read_file(data)
            geojson = gdf.__geo_interface__
        elif isinstance(data, dict):
            geojson = data
        layer = ipyleaflet.GeoJSON(data=geojson, hover_style=hover_style, **kwargs)
        self.add_layer(layer)

        if zoom_to_layer:
            bounds = gdf.total_bounds
            self.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

    def add_shp(self, data, **kwargs):
        """Adds a shapefile layer to the map.

        Args:
            data (str): The file path to the shapefile.
            **kwargs: Additional keyword arguments passed to the add_geojson method.
        """
        import geopandas as gpd

        gdf = gpd.read_file(data)
        gdf = gdf.to_crs(epsg=4326)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, **kwargs)

    def add_gdf(self, gdf, **kwargs):
        """Adds a GeoDataFrame layer to the map.

        Args:
            gdf (geopandas.GeoDataFrame): The GeoDataFrame to add.
            **kwargs: Additional keyword arguments passed to the add_geojson method.
        """
        gdf = gdf.to_crs(epsg=4326)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, **kwargs)

    def add_vector(self, data, **kwargs):
        """Adds a vector layer to the map.

        Args:
            data (str, geopandas.GeoDataFrame, or dict): The vector data to add. Can be a file path,
                a GeoDataFrame, or a GeoJSON dictionary.
            **kwargs: Additional keyword arguments passed to the add_geojson or add_gdf method.

        Raises:
            ValueError: If the data is not a valid file path, GeoDataFrame, or GeoJSON dictionary.
        """
        import geopandas as gpd

        if isinstance(data, str):
            gdf = gpd.read_file(data)
            self.add_gdf(gdf, **kwargs)
        elif isinstance(data, gpd.GeoDataFrame):
            self.add_gdf(data, **kwargs)
        elif isinstance(data, dict):
            self.add_geojson(data, **kwargs)
        else:
            raise ValueError("data must be a file path or a GeoDataFrame or a dict")

    def add_raster(self, filepath, **kwargs):

        from localtileserver import TileClient, get_leaflet_tile_layer

        client = TileClient(filepath)
        tile_layer = get_leaflet_tile_layer(client, **kwargs)

        self.add(tile_layer)
        self.center = client.center()
        self.zoom = client.default_zoom
