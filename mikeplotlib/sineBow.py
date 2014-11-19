#!/usr/bin/env python
###############################################################################
#                                                                             #
#    sineBow.py - make color scales in a sinebow fashion                      #
#                 see: http://basecase.org/env/on-rainbows                    #
#                                                                             #
###############################################################################
#                                                                             #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program. If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

__author__ = "Michael Imelfort"
__copyright__ = "Copyright 2014"
__credits__ = ["Michael Imelfort"]
__license__ = "GPL3"
__version__ = "1.0.0"
__maintainer__ = "Michael Imelfort"
__email__ = "mike@mikeimelfort.com"
__status__ = "Released"

###############################################################################

import math

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class SineBow:
    def __init__(self,
                 upperBound,
                 resolution,
                 lowerBound=0.,
                 mapType="rb"):
        '''
        Default constructor.

        Set the type upper and lower bounds and resolution of the colormap

        Inputs:
         upperBound - float, the maximum value to map
         resolution - int, the number of steps between lower and upper bounds
         lowerBound - float, the minimum value to map
         mapType - string, type of map to make [rb, br, bgr, rgb]

        Outputs:
         None
        '''
        # constants
        self.RBLowerOffset = 0.5
        self.RBDivisor = (2.0/3.0)
        self.RB_ERROR_COLOUR = [0,0,0]

        # set the limits
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.resolution = resolution
        self.tickSize = (self.upperBound-self.lowerBound) / (self.resolution-1)

        # set the type, red-blue by default
        self.type = mapType
        self.rOffset = 0.0
        self.gOffset = self.RBDivisor * math.pi * 2.0
        self.bOffset = self.RBDivisor * math.pi

        self.ignoreRed = False
        self.ignoreGreen = True
        self.ignoreBlue = False

        self.lowerScale = 0.0
        self.upperScale = self.RBDivisor * math.pi

        if(self.type == "rgb"): # red-blue-green
            self.rOffset = 0.0
            self.gOffset = self.RBDivisor * math.pi
            self.bOffset = self.RBDivisor * math.pi * 2.0

            self.ignoreRed = False
            self.ignoreGreen = False
            self.ignoreBlue = False

            self.lowerScale = 0.0
            self.upperScale = (self.RBDivisor * math.pi * 2.0)

        elif(self.type == "bgr"): # green-blue-red
            self.rOffset = self.RBDivisor * math.pi * 2.0
            self.gOffset = self.RBDivisor * math.pi
            self.bOffset = 0.0

            self.ignoreRed = False
            self.ignoreGreen = False
            self.ignoreBlue = False

            self.lowerScale = 0.0
            self.upperScale = (self.RBDivisor * math.pi * 2.0)

        elif(self.type == "br"): # blue-red
            self.rOffset = self.RBDivisor * math.pi
            self.gOffset = self.RBDivisor * math.pi * 2.0
            self.bOffset = 0.0

            self.ignoreRed = False
            self.ignoreGreen = True
            self.ignoreBlue = False

            self.lowerScale = 0.0
            self.upperScale = (self.RBDivisor * math.pi)

        self.scaleMultiplier = (self.upperScale - self.lowerScale) / \
                                (self.upperBound - self.lowerBound)

    def _getValue(self,
                  pointVal):
        '''Get a raw value, not a color

        Inputs:
         pointVal - float, the value to convert to a RBG-ish value

        Outputs:
         None
        '''
        val = (math.cos(pointVal) + self.RBLowerOffset) * self.RBDivisor
        if val <= 0:
            return 0.
        return val*val

    def getColor(self, pointVal, hexFormat=False):
        """Return an RGB color tuple for the given point value.

        If nothing makes sense. return black

        Inputs:
         pointVal - float, the point value to convert to a colour

        Output:
         An RGB colour tuple
        """
        if(pointVal > self.upperBound or pointVal < self.lowerBound):
            return self.RB_ERROR_COLOUR

        # normalise the value to suit the ticks
        normalised_val = round(pointVal/self.tickSize) * self.tickSize

        # map the normalised value onto the horizontal scale
        scaled_val = ((normalised_val - self.lowerBound) * \
                          self.scaleMultiplier) + self.lowerScale
        r = 0
        g = 0
        b = 0

        if(not self.ignoreRed):
            r = int(round(self._getValue(scaled_val - self.rOffset) * 255))
        if(not self.ignoreGreen):
            g = int(round(self._getValue(scaled_val - self.gOffset) * 255))
        if(not self.ignoreBlue):
            b = int(round(self._getValue(scaled_val - self.bOffset) * 255))

        ratio = 255./float(r + b + g)
        rgb = tuple([int(float(val) * ratio) for val in (r, g, b)])
        if hexFormat:
            return "#%s" % format(rgb[0]<<16 | rgb[1]<<8 | rgb[2], '06x')
        return rgb

###############################################################################
###############################################################################
###############################################################################
###############################################################################
