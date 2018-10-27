# # # # # # # # # # # # # # # #

# {{ DLFLV }}
# Copyright (C) {{ 2017 }}  {{ Ariel Noyman }}
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# # # # # # # # # # # # # # # # #

# "@context": "https://github.com/RELNO/", "@type": "Person", "address": {
# "@type": "75 Amherst St, Cambridge, MA 02139", "addressLocality":
# "Cambridge", "addressRegion": "MA",},
# "jobTitle": "Research Scientist", "name": "Ariel Noyman",
# "alumniOf": "MIT", "url": "http://arielnoyman.com",
# "https://www.linkedin.com/", "http://twitter.com/relno",
# https://github.com/RELNO]
# # # # # # # # # # # # # # # #
#
# USAGE:
# python3 GSVScraper.py -l __FILE NAME__ -i __ANGLE__ -k __GOOGLEKEY__
#
# # # # # # # # # # # # # # # #

'''
----------------------------
LLDD[LatLonDisDir] finds GSV
locations around a given point.
If so, it retruns these in a
form of a JSON file and on a
 map [using gmplot]
----------------------------
Usage
from LatLonDisDir import LatLonDisDir as LLDD
obj = LLDD(42.349345, -71.082819)
LLDD.gsvFinder(obj, 1000, 50, 30)

 - angular diameter:
 http://www.astronomynotes.com/solarsys/s2.htm
'''


class LatLonDisDir:

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def gsvFinder(self, distance, increments, angle):
        "gsvFinder(self, distance[m], increments[m], angle[deg])"

        import math
        import requests
        import xml.etree.ElementTree as ET
        # from gmplot import gmplot

        # vars
        gmapLatList = []
        gmapLonList = []
        # earthRadiusadius of the Earth
        earthRadius = 6378.1

        # Current lat point converted to radians 52.20472
        latGetRad = math.radians(self.lat)
        # Current long point converted to radians 0.14056
        lonGetRad = math.radians(self.lon)

        # finds the distane between points on the first radius
        # so we can reuse it over the next radiuses
        firstDistOnArc = (math.pi * (increments/1000) * angle) / 180

        print('\n', 'first distance', firstDistOnArc, '\n')

        for d in range(increments, distance, increments):
            print('\n', '--- Distance', d, 'form', self.lat, self.lon)

            # convert km to meters
            dist = d/1000
            # finds the angle in proprtion to 'd'
            angle = math.ceil(math.degrees(firstDistOnArc/dist))

            print('at angle:', angle, ' ---', '\n')

            # runs thru all angles with the jumps of var 'angle'
            for a in range(0, 360, angle):

                # convert deg to rad
                a = math.radians(a)

                # find lat in distance 'dist' & angle 'a'
                latOut = math.asin(math.sin(latGetRad)*math.cos(dist/earthRadius) +
                                   math.cos(latGetRad)*math.sin(dist/earthRadius)*math.cos(a))
                # find lon in distance 'dist' & angle 'a'
                lonOut = lonGetRad + math.atan2(math.sin(a)*math.sin(dist/earthRadius)*math.cos(
                    latGetRad), math.cos(dist/earthRadius)-math.sin(latGetRad)*math.sin(latOut))

                latOut = math.degrees(latOut)
                lonOut = math.degrees(lonOut)
                # create a string with two locations
                latLon = str(latOut) + ',' + str(lonOut)

                # check GSV URL base
                checkURLstart = "http://maps.google.com/cbk?output=xml&hl=en&ll="
                checkURLend = "&radius=50&cb_client=maps_sv&v=4"

                URL = checkURLstart + latLon + checkURLend
                response = requests.get(URL)
                root = ET.fromstring(response.content)

                # output
                print('checking', latLon, '\n' 'at angle', math.degrees(a))
                if root:
                    # print("( ͡° ͜ʖ ͡°)")
                    gmapLatList.append(latOut)
                    gmapLonList.append(lonOut)
                else:
                    print("(ಠ_ಠ)")

        # plot the scatter points
        gmap = gmplot.GoogleMapPlotter(self.lat, self.lon, 15)

        # add first point to map
        gmapLatList.append(self.lat)
        gmapLonList.append(self.lon)
        # make heatmap
        gmap.heatmap(gmapLatList, gmapLonList)
        gmap.draw("LLDD_map.html")


# calling class
obj = LatLonDisDir(42.360197, -71.087115)
obj.gsvFinder(2000, 50, 60)
