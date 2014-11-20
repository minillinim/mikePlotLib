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
__version__ = "2.0.0"
__maintainer__ = "Michael Imelfort"
__email__ = "mike@mikeimelfort.com"
__status__ = "Released"

###############################################################################

import math

###############################################################################
###############################################################################
###############################################################################
###############################################################################

schemes = ['rb', 'br', 'gr', 'rg', 'bg', 'gb', 'rgb', 'bgr', 'sine']
class SineBow(object):
    def __init__(self,
                 upperBound,
                 lowerBound=0.,
                 mapType="rb",
                 mode="bright"):
        '''
        Default constructor.

        Set the type upper and lower bounds and resolution of the colormap

        Inputs:
         upperBound - float, the maximum value to map
         lowerBound - float, the minimum value to map
         mapType - string, type of map to make
                   ['rb', 'br', 'gr', 'rg', 'bg', 'gb', 'rgb', 'bgr', 'sine']

        Outputs:
         None
        '''
        self.schemes = {'rb' : (0., math.pi/2.),
                        'br' : (math.pi/2., 0.),
                        'gr' : (math.pi, 3.*math.pi/2.),
                        'rg' : (3.*math.pi/2., math.pi),
                        'bg' : (math.pi/2, math.pi),
                        'gb' : (math.pi, math.pi/2),
                        'rgb' : (3.*math.pi/2., math.pi/2.),
                        'bgr' : (math.pi/2., 3.*math.pi/2.),
                        'sine' : (0., 3.*math.pi/2.)}

        self.lowerBound = lowerBound
        self.upperBound = upperBound
        self.boundSpan = float(self.upperBound - self.lowerBound)

        (self.thetaMin, self.thetaMax) = self.schemes[mapType]
        self.thetaSpan = self.thetaMax - self.thetaMin

        if mode == "bright":
            self.maker = self.makeBrightColor
        else:
            self.maker = self.makeSoftColor

    def _findTheta(self, value):
        '''find the angle corresponding to the given value

        Input:
         value - float, the value to produce a color for

        Outputs:
         an angle
        '''
        return ((value - self.lowerBound)/self.boundSpan * self.thetaSpan) +\
                    self.thetaMin

    def getNColors(self, n, hexFormat=False):
        '''get N evenly spaced colors

        Input:
         n - int, the number of colors to make
         hexFormat == True -> return rgb hex code

        Outputs:
         a list of rgb values or hex codes
        '''
        step_size = self.boundSpan / (n-1.)
        values = [(i * step_size) for i in range(n)]
        return [self.makeColor(i, hexFormat=hexFormat) for i in values]

    def makeColor(self, value, hexFormat=False):
        '''return a bright color

        Inputs:
         value - float, the value to produce a color for
         hexFormat == True -> return rgb hex code

        Outputs:
         an RGB tuple or a hex code
        '''
        (r,g,b) = self.maker(value)
        if hexFormat:
            return "#%s" % (format(r<<16 | g<<8 | b, '06x'))
        else:
            return (r,g,b)

    def makeBrightColor(self, value):
        '''return a bright color

        Inputs:
         value - float, the value to produce a color for

        Outputs:
         an RGB tuple or a hex code
        '''
        theta = self._findTheta(value)
        if theta > math.pi:
            rr = int(255.*math.cos(theta+math.pi/2.))
        elif theta < math.pi/2:
            rr = int(255.*math.cos(theta))
        else:
            rr = 0

        if theta > math.pi/2. and theta < 3.*math.pi/2.:
            gg = int(-1*255.*math.cos(theta))
        else:
            gg = 0

        if theta < math.pi:
            bb = int(255.*math.sin(theta))
        else:
            bb = 0

        return (rr, gg, bb)

    def makeSoftColor(self, value):
        '''return a soft color

        Inputs:
         value - float, the value to produce a color for

        Outputs:
         an RGB tuple or a hex code
        '''
        theta = self._findTheta(value)
        if theta > math.pi:
            rr = int(255.*math.pow(math.cos(theta+math.pi/2.),2))
        elif theta < math.pi/2:
            rr = int(255.*math.pow(math.cos(theta),2))
        else:
            rr = 0

        if theta > math.pi/2. and theta < 3.*math.pi/2.:
            gg = int(255.*math.pow(math.cos(theta),2))
        else:
            gg = 0

        if theta < math.pi:
            bb = int(255.*math.pow(math.sin(theta),2))
        else:
            bb = 0

        return (rr, gg, bb)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
