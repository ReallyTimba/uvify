import flet as ft
import flet_map as fm
import requests

class Torremap:
    def __init__(self):
        self.build_map()


    def search_pharmacies(self):
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = """
        [out:json];
        node["amenity"="pharmacy"](41.1347,1.3929,41.1563,1.4177);
        out;
        """
        resp = requests.get(overpass_url, params={'data': query})
        pharmacies = []
        if resp.ok:
            for el in resp.json()["elements"]:
                tags = el.get("tags", {})
                address = tags.get("addr:full") or f"{tags.get('addr:street','')} {tags.get('addr:housenumber','')}".strip()
                tooltip = tags.get("name", "Pharmacy")
                if address:
                    tooltip += "\n" + address
                pharmacies.append({
                    "lat": el["lat"],
                    "lon": el["lon"],
                    "tooltip": tooltip
                })
        return pharmacies

    def build_map(self):
        pharmacies = self.search_pharmacies()

        markers = [
            fm.Marker(
                coordinates=fm.MapLatitudeLongitude(ph["lat"], ph["lon"]),
                content=ft.Container(
                    ft.Icon(name=ft.Icons.LOCAL_PHARMACY, color="green", size=32),
                    tooltip=ph["tooltip"],
                ),
            ) for ph in pharmacies
        ]

        self.marker_layer = fm.MarkerLayer(markers=markers)
        self.class_map = fm.Map(
            layers=[
                fm.TileLayer(
                    url_template="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png",
                    subdomains=["a", "b", "c", "d"],
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                self.marker_layer,
            ],
            initial_center=fm.MapLatitudeLongitude(41.145, 1.405),
            initial_zoom=14,
            expand=True
        )

