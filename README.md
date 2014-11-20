# mikePlotLib

## Overview

A collection of plotting / coloring tools I've been using here and there. Finally I'm putting them into one place.
One safe place.

## Installation

Should be as simple as

    pip install mikePlotLib

## SineBow - turn values into colours

### create an rgb sinebow that spans a portion of the color wheel between 0 and 100 with 1000 steps
    from mikeplotlib.sineBow import SineBow
    SB = SineBow(100, mapType='rgb')

### get the rgb tuple for value=57.1
    SB.makeColor(57.1)                       # (0, 245, 9)

### get it as a #hex string
    SB.makeColor(57.1, hexFormat=True)       # #00f509

### get 25 colours evenly spaced over the region
    cols = SB.getNColors(25)

## StackedbarGraph - code for making purdy stacked bar graphs

### Example usage 1

    from stackedBarGraph import StackedBarGrapher()
    SBG = StackedBarGrapher()
    SBG.demo()

### Example usage 2

    import numpy as np
    from matplotlib import pyplot as plt
    from stackedBarGraph import StackedBarGrapher
    SBG = StackedBarGrapher()

    d = np.array([[101.,0.,0.,0.,0.,0.,0.],
                  [92.,3.,0.,4.,5.,6.,0.],
                  [56.,7.,8.,9.,23.,4.,5.],
                  [81.,2.,4.,5.,32.,33.,4.],
                  [0.,45.,2.,3.,45.,67.,8.],
                  [99.,5.,0.,0.,0.,43.,56.]])

    d_widths = [.5,1.,3.,2.,1.,2.]
    d_labels = ["fred","julie","sam","peter","rob","baz"]
    d_colors = ['#2166ac', '#fee090', '#fdbb84', '#fc8d59', '#e34a33', '#b30000', '#777777']
    fig = plt.figure()

    ax = fig.add_subplot(111)
    SBG.stackedBarPlot(ax,
                       d,
                       d_colors,
                       xLabels=d_labels,
                       yTicks=7,
                       widths=d_widths,
                       scale=True
                      )
    plt.title("Scaled bars with set widths")

    fig.subplots_adjust(bottom=0.4)
    plt.tight_layout()
    plt.show()
    plt.close(fig)
    del fig

## cbCols - Easy access to the colorbrewer2.org maps

### Example usage 1 - see all available colours

    from cb2cols import Cb2Cols as CB2
    cb2 = CB2()
    cb2.demo()

### Example usage 2 - the first three colours from qualset1

    from cb2cols import Cb2Cols as CB2
    cb2 = CB2()
    col_set = "qualSet1"
    colours = cb2.maps[col_set].values()[0:3]

## Help

If you experience any problems using mikePlotLib, open an [issue](https://github.com/minillinim/mikePlotLib/issues) on GitHub and tell us about it.

## Licence and referencing

Project home page, info on the source tree, documentation, issues and how to contribute, see http://github.com/minillinim/mikePlotLib

This software is currently unpublished

## Copyright

Copyright (c) 2014 Michael Imelfort. See LICENSE.txt for further details.
