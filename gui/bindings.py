"""
The data control panel for PSquid.
"""
import wx


class Binder(object):
    """
    Responsible for binding a PSquid object to its GUI.
    """
    def __init__(self, fmf, fgf, pyo):
        self.pyo = pyo
        self.fmf = fmf
        self.fgf = fgf

        self.make_binders()

    def make_binders(self):
        """
        Make the binding classes.
        """
        fmf = self.fmf

        self.mainbindings = MainBindings(self, self.fmf)
        self.graphbindings = GraphBindings(self, self.fgf)

    def bind(self):
        """
        Bind everything.
        """
        self.bind_main()
        self.bind_graph()
        self.bind_pyo()

    def bind_main(self):
        """
        Bind the main panel.
        """
        self.mainbindings.bind()

    def bind_graph(self):
        """
        Bind the graph panel.
        """
        self.graphbindings.bind()

    def bind_pyo(self):
        """
        Connect the PyOscope figure to the Canvas.
        """
        pass #DELME


class MainBindings(object):
    """
    Callback functions for the Main panel bindings.
    """
    def __init__(self, binder, fmf):
        self.binder = binder
        self.fmf = fmf
        self.fgf = binder.fgf
        self.pyo = binder.pyo

        self.timer = self.fmf.timer

    def bind(self):
        self.fmf.bindings = self

        # File
        self.fmf.Bind(wx.EVT_CLOSE, self.on_close, self.fmf)
        self.fmf.Bind(wx.EVT_MENU, self.on_close, self.fmf.miQuit)

    def on_close(self, event):
        # Stop timers
        timers = [self.timer,]
        for timer in timers:
            timer.Stop()

        # Let the event queue flush out
        wx.Yield()

        # Clean up the interfaces and objects
        self.pyo.stop()
        # self.pyo.close()
        self.fmf.Destroy()
        self.fgf.Destroy()


class GraphBindings(object):
    """
    Callback functions for the Graph panel bindings.
    """
    def __init__(self, binder, fgf):
        self.binder = binder
        self.fgf = fgf
        self.fmf = binder.fmf
        self.pyo = binder.pyo

        self.timer = self.fmf.timer

        self.cols = []

    def bind(self):
        self.fgf.bindings = self

        # Initialize
        self.fgf.replace_figure(self.pyo.fig)  # Swap out placeholder figure
        self.pyo.canvas = self.pyo.fig.canvas  # Canvas created in prev line
        self.canvas = self.pyo.canvas
        self.pyo.fig.canvas.SendSizeEventToParent()  # Force resize/redraw

        # Timer
        self.fmf.Bind(wx.EVT_TIMER, self.on_timer, self.timer)

    def on_timer(self, event):
        """
        Plot update loop. The way PyOscope is written, this should simply call
        the pyoscope update() method and then redraw the canvas. Also redraws
        the channel selection checkboxes, if necessary.
        """
        try:
            self.update_channels()
            self.pyo._update()
            self.canvas.draw()
        except Exception as e:
            self.timer.Stop()
            raise e

    def update_channels(self):
        """
        Update the channel selection checkboxes, if necessary.
        """
        pChannels = self.fgf.pChannels
        try:
            cols = self.pyo.data.columns
            if list(cols) != list(self.cols):
                pChannels.make_channel_checkboxes()
            self.cols = cols

            activex, activey = pChannels.active_channels()
            if (activex != pChannels.activex) or (activey != pChannels.activey):
                xlabels = [chk.GetLabel() for chk in pChannels.chkboxesX]
                xs = [pChannels.coldict[xlabel]
                      for xlabel in xlabels if activex[xlabel]]
                ylabels = [chk.GetLabel() for chk in pChannels.chkboxesY]
                ys = [pChannels.coldict[ylabel]
                      for ylabel in ylabels if activey[ylabel]]

                if not xs:
                    xs = [None]
                if not ys:
                    ys = [None]

                self.pyo.plot(xs, ys)
        except (AttributeError, TypeError):
            pass


