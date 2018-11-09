import gmplot


gmap = gmplot.GoogleMapPlotter(42.5080882978956, 1.5293202323005406, 30)
# Scatter points
top_attraction_lats, top_attraction_lons = zip(*[
    (42.5080882978956, 1.5293202323005406)
    ])
gmap.scatter(top_attraction_lats, top_attraction_lons, '#3B0B39', size=10, marker=False)

#gmap = gmplot.GoogleMapPlotter.from_geocode("Andorra")
gmap.apikey = ""
gmap.draw("mymap.html")
