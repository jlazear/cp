"""
The Graph Frame for the CP app.
"""
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import wx

from channelpanel import ChannelPanel


class GraphFrame(wx.Frame):
    """
    The plot frame
    """
    title = 'Plot'

    def __init__(self):
        styles = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX)
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          title=self.title, style=styles, size=(800, 600))

        self.panel = wx.Panel(self)

        # Splitter pane
        self.splMain = wx.SplitterWindow(self.panel, wx.ID_ANY,
                                         style=wx.SP_LIVE_UPDATE)
        self.splMain.SetMinimumPaneSize(150)

        # Plot figure canvas
        self.wPlot = wx.Window(self.splMain, style=wx.BORDER_SUNKEN)
        bsPlot, cPlot, tbPlot = self.make_canvas(self.wPlot)
        self.bsPlot = bsPlot
        self.cPlot = cPlot
        self.tbPlot = tbPlot

        self.wPlot.SetSizer(self.bsPlot)

        # Channel selection panel
        self.wRight = wx.Window(self.splMain)
        self.bsRight = wx.BoxSizer(wx.VERTICAL)
        self.pChannels = ChannelPanel(self.wRight)

        self.bsRight.Add(self.pChannels, 1, wx.EXPAND | wx.TOP)
        self.wRight.SetSizer(self.bsRight)

        # Add subwindows to splitter
        self.splMain.SplitVertically(self.wPlot, self.wRight, 800)

        self.bsMain = wx.BoxSizer(wx.VERTICAL)
        self.bsMain.Add(self.splMain, 1, wx.ALL | wx.EXPAND)

        self.panel.SetSizer(self.bsMain)
        self.Layout()

    def make_canvas(self, parent, fig=None, tb=True):
        if fig is None:
            fig, _, _ = self.init_plot()
        else:
            fig = fig

        canvas = FigCanvas(parent, -1, fig)

        bsPlot = wx.BoxSizer(wx.VERTICAL)
        bsPlot.Add(canvas, 1, flag=wx.GROW)

        if tb:
            toolbar = NavigationToolbar(canvas)
            toolbar.Realize()
            bsPlot.Add(toolbar, 0, wx.LEFT | wx.EXPAND)
        else:
            toolbar = None

        return bsPlot, canvas, toolbar

    def init_plot(self, plotsize=(9., 6.), data=None):
        fig = Figure(plotsize, dpi=100)

        axes = fig.add_subplot(111)

        if data is not None:
            xs, ys = data
            lines = [axes.plot(xs, ys)]
        else:
            lines = [[]]

        return fig, axes, lines

    def replace_figure(self, newfigure):
        """
        Replaces the canvas and figure with the specified figure and its
        associated toolbar. The old figure, canvas, and sizer are destroyed.
        """
        oldcanvas = self.cPlot
        oldtoolbar = self.tbPlot
        # oldsizer = self.bsPlot  # Automatically destroyed when unattached

        bsPlot, cPlot, tbPlot = self.make_canvas(self.wPlot,
                                                 fig=newfigure)
        self.bsPlot = bsPlot
        self.cPlot = cPlot
        self.tbPlot = tbPlot

        self.wPlot.SetSizer(self.bsPlot)
        self.bsPlot.Layout()

        oldcanvas.Destroy()
        oldtoolbar.Destroy()
