"""
The channel selection panel to be attached to the GraphFrame in the CP GUI.
"""
import wx


class ChannelPanel(wx.Panel):
    """
    The channel panel for the CP GraphFrame.
    """
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        self.fgf = self.GetTopLevelParent()

        self.bsMain = wx.BoxSizer(wx.VERTICAL)

        self.coldict = None
        self.activex = {}
        self.activey = {}
        self.make_channel_checkboxes()

        self.SetSizer(self.bsMain)

    def make_channel_checkboxes(self):
        """
        Make all the controls for the channel selector checkboxes.
        """
        self.bsX, self.chkboxesX = self.make_buttons('X Channels')
        for i, button in enumerate(self.chkboxesX):
            if i == 0:
                button.SetValue(True)
            else:
                button.SetValue(False)

        self.bsY, self.chkboxesY = self.make_buttons('Y Channels')
        for i, button in enumerate(self.chkboxesY):
            if i == 0:
                button.SetValue(False)
            else:
                button.SetValue(True)

        self.bsMain.Prepend(self.bsY, 1, wx.EXPAND)
        self.bsMain.Prepend((20, 20), 0, wx.EXPAND)
        self.bsMain.Prepend(self.bsX, 1, wx.EXPAND)

        while len(self.bsMain.Children) > 3:
            nChildren = len(self.bsMain.Children)
            self.bsMain.Hide(nChildren-1)
            self.bsMain.Remove(nChildren-1)

        self.activex, self.activey = self.active_channels()
        self.bsMain.Layout()
        self.Fit()

    def active_channels(self):
        activex = dict([(chk.GetLabel(), chk.GetValue()) for chk in
                        self.chkboxesX])
        activey = dict( [(chk.GetLabel(), chk.GetValue()) for chk in
                         self.chkboxesY])
        return activex, activey

    # This version is hideously slow for some reason...
    # def make_channel_checkboxes(self):
    #     """
    #     Make all the controls for the channel selector checkboxes.
    #     """
    #     self.bsX, self.chkboxesX = self.make_buttons('X Channels')
    #     self.bsY, self.chkboxesY = self.make_buttons('Y Channels')
    #
    #     bs = wx.BoxSizer(wx.VERTICAL)
    #     bs.Add(self.bsX, 1, wx.EXPAND)
    #     bs.Add((20, 20), 0, wx.EXPAND)
    #     bs.Add(self.bsY, 1, wx.EXPAND)
    #
    #     bsMain_old = self.bsMain
    #     self.bsMain = bs
    #     self.SetSizer(self.bsMain)
    #     bsMain_old.Destroy()
    #
    #     self.bsMain.Layout()
    #     self.Fit()

    def make_buttons(self, label):
        """
        Make the sizer containing the controls for a channel selector.
        """
        bs = wx.BoxSizer(wx.VERTICAL)

        lbl = wx.StaticText(self, wx.ID_ANY, label)
        bs.Add(lbl, 0, wx.EXPAND)

        chkboxes = []
        coldict = {}
        try:
            pyo = self.fgf.app.pyo
            columns = pyo.data.columns

            chk = wx.CheckBox(self, wx.ID_ANY, 'Index')
            chkboxes.append(chk)
            bs.Add(chk, 0, wx.EXPAND)
            coldict['Index'] = None

            for col in columns:
                strcol = str(col)
                coldict[strcol] = col
                chk = wx.CheckBox(self, wx.ID_ANY, strcol)
                bs.Add(chk, 0, wx.EXPAND)
                chkboxes.append(chk)
        except AttributeError:
            pass

        self.coldict = coldict
        return bs, chkboxes
