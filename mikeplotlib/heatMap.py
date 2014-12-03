#!/usr/bin/env python
###############################################################################
#                                                                             #
#    heatMap.py - make a purdy heatmap                                        #
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

import numpy as np
np.seterr(all='raise')

import os

from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
import matplotlib.font_manager as fm

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, leaves_list
from mikeplotlib.sineBow import SineBow

from pkg_resources import resource_filename

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class HeatMap(object):
    def __init__(self,
                 data,
                 columnNames,
                 rowNames,
                 colorMap,
                 ):
        '''make a heatmap

        Inputs:
         data - [[float]], data to use in heatmap. Rows x Columns
         columnNames - [string], column names used for labeling
         rowNames - [string], row names used for labeling
         colorMap - string, sineBow type colormap

        Outputs:
         None
        '''
        self.colorMap = colorMap
        self.data = data

        self.rowNames = rowNames
        self.columnNames = columnNames

        # work out heatmap color ranges
        self.SBs = []
        for c in range(len(self.columnNames)):
            vec = [self.data[r][c] for r in range(len(self.rowNames))]
            max = np.max(vec)
            min = np.min(vec)
            if min == max == 0:
                max = 1
            self.SBs.append(SineBow(max, lowerBound=min, mapType=self.colorMap))

        self.fontPath = os.path.abspath(resource_filename('mikeplotlib',
                                                          'Menlo-Regular.ttf'))
        # some default values
        self.gapPerc = 0.02     # percent of the block width to use as a gap

    def makeMap(self,
                width,
                height,
                fileName,
                orderRows=False,
                orderColumns=False):
        '''make a heatmap

        Inputs:
         width - float, width of the heatmap
         height - float, height of the heatmap

        Outputs:
         None
        '''
        (rows, cols) = np.shape(self.data)
        prop = fm.FontProperties(fname=self.fontPath,
                                 size='small',
                                 #stretch='ultra-condensed'
                                 )

        #---------------------------------------------------
        # reorder rows and columns?
        if orderRows:
            # work out linkage
            row_dist = pdist(self.data)
            row_linkage_matrix = linkage(row_dist)
            row_ordering = leaves_list(row_linkage_matrix)
        else:
            row_ordering = np.arange(rows)

        if orderColumns:
            column_dist = pdist(np.transpose(self.data))
            column_linkage_matrix = linkage(column_dist)
            column_ordering = leaves_list(column_linkage_matrix)
        else:
            column_ordering = np.arange(cols)

        patch_width  = float(width) / float( cols + self.gapPerc * (cols-1) )
        gap = patch_width * self.gapPerc
        patch_height = (float(height) - (gap * (rows-1))) / float(rows)

        #----------------------------------------------------
        # plot the actual heatmap
        #
        fig = plt.figure(facecolor='w')

        hm_ax = fig.add_subplot(223)
        row_desc_ax = fig.add_subplot(224)
        col_desc_ax = fig.add_subplot(221)

        col_desc_ax = plt.subplot2grid((4,5), (0,0), rowspan=1, colspan=3)
        hm_ax = plt.subplot2grid((4,5), (1,0), rowspan=3, colspan=3)
        row_desc_ax = plt.subplot2grid((4,5), (1,3), rowspan=3, colspan=2)

        # how much to round the corner by
        corner = gap

        top = 0
        for r in row_ordering:
            left = 0.
            # label the heatmap row
            row_desc_ax.text(0,
                             top+gap+patch_height/2,
                             self.rowNames[r],
                             verticalalignment='center',
                             fontproperties=prop)

            for c in column_ordering:
                hm_ax.add_patch(FancyBboxPatch((left+corner, top+corner),
                                               patch_width-2*corner,
                                               patch_height-2*corner,
                                               edgecolor='none',
                                               boxstyle="round,pad=%d" % corner,
                                               facecolor=self.SBs[c].makeColor(self.data[r][c],
                                                                               hexFormat=True))
                             )

                left += patch_width + gap
            top += (patch_height + gap)
        left = 0
        # label the heatmap columns
        for c in column_ordering:
            col_desc_ax.text(left + gap + patch_width/2,
                             top,
                             self.columnNames[c],
                             verticalalignment='bottom',
                             horizontalalignment='center',
                             fontproperties=prop,
                             rotation=90)
            left += patch_width + gap

        # fix limits and set borders
        hm_ax.set_xlim(0, width)
        hm_ax.set_ylim(height, 0)
        hm_ax.set_axis_off()

        row_desc_ax.set_ylim(height, 0)
        row_desc_ax.set_axis_off()

        col_desc_ax.set_xlim(0, width)
        col_desc_ax.set_ylim(height, 0)
        col_desc_ax.set_axis_off()

        # fix the spacing
        plt.subplots_adjust(wspace=.05, hspace=.05)

        fig.set_size_inches(8,10)
        fig.savefig(fileName,dpi=300)

        #plt.show()
        plt.close(fig)
        del fig


###############################################################################
###############################################################################
###############################################################################
###############################################################################
