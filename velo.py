import csv
import folium
from scipy.spatial import Voronoi, voronoi_plot_2d
import shapely
import shapely.geometry
import shapely.ops

def main():
    map = folium.Map(location=[51.213312, 4.408926], tiles='cartodbpositron', zoom_start=13)

    border = r'gem-antwerpen.geojson'

    map.choropleth(geo_path=border, fill_color='Reds', fill_opacity=0.2, line_opacity=0.7)

    points = []
    with open('velostation.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
        for row in reader:
            folium.CircleMarker(location=[row['point_lat'], row['point_lng']], color='#D11F38',
                    fill_color='#D11F38', radius=1).add_to(map)

            points.append([row['point_lat'], row['point_lng']])

    vor = Voronoi(points)
    # print(vor.regions)
    # print(vor.vertices)
    lines = [
        shapely.geometry.LineString(vor.vertices[line])
        for line in vor.ridge_vertices
        if -1 not in line
    ]

    for poly in shapely.ops.polygonize(lines):
        # print(poly)
        geojson = shapely.geometry.mapping(poly)
        print(geojson)
        
    for line in vor.ridge_vertices:
        if -1 not in line:
            folium.PolyLine((vor.vertices[line[0]], vor.vertices[line[1]]), color='red', opacity=0.7).add_to(map)

    map.save('test.html')

if __name__ == '__main__':
    main()
