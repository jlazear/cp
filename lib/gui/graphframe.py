"""
The Graph Frame for the CP app.
"""
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

import wx

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

        bsPlot, cPlot, tbPlot = self.make_canvas(self.panel)
        self.bsPlot = bsPlot
        self.cPlot = cPlot
        self.tbPlot = tbPlot

        self.panel.SetSizer(self.bsPlot)

        self.Bind(wx.EVT_CLOSE, self.onClose, self)

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

        bsPlot, cPlot, tbPlot = self.make_canvas(self.panel,
                                                 fig=newfigure)
        self.bsPlot = bsPlot
        self.cPlot = cPlot
        self.tbPlot = tbPlot

        self.panel.SetSizer(self.bsPlot)
        self.bsPlot.Layout()

        oldcanvas.Destroy()
        oldtoolbar.Destroy()

    def onClose(self, event):
        self.Destroy()
