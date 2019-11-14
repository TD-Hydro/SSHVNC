# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.3 on Sat Oct 12 22:13:44 2019
#

import wx
import sys
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class TerminalFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: TerminalFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((500, 500))
        self.terminalTextCtrl = wx.TextCtrl(
            self, wx.ID_ANY, "123", style=wx.TE_MULTILINE | wx.TE_WORDWRAP)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

        self.terminalTextCtrl.Bind(wx.EVT_CHAR, self.InputToShell)

        self.reserveLength = 0
        self.entered = False
        self.tabbed = False

    def __set_properties(self):
        # begin wxGlade: TerminalFrame.__set_properties
        self.SetTitle("Terminal")
        self.terminalTextCtrl.SetBackgroundColour(wx.Colour(0, 0, 0))
        self.terminalTextCtrl.SetForegroundColour(wx.Colour(255, 255, 255))
        self.terminalTextCtrl.SetFont(wx.Font(
            12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Consolas"))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: TerminalFrame.__do_layout
        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_20 = wx.GridSizer(1, 1, 0, 0)
        sizer_20.Add(self.terminalTextCtrl, 0, wx.EXPAND, 0)
        sizer_19.Add(sizer_20, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_19)
        self.Layout()
        # end wxGlade

    def onClose(self, event):
        self.sshc.CloseConn()
        self.Destroy()

    def SetConn(self, connection):
        self.sshc = connection
        self.shell = self.sshc.VirtualShell()

    def InvoleShell(self):
        import threading
        # sys.stdout.write(
        #    "Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n"
        # )

        def WriteAll(sock):
            while True:
                data = sock.recv(256)
                if not data:
                    self.Close()
                else:
                    dataString = data.decode('utf-8')
                    if self.entered:
                        firstLine = dataString.find('\n')
                        if firstLine != -1:
                            dataString = dataString[firstLine:]
                        self.entered = False

                    if not self.tabbed:
                        self.terminalTextCtrl.AppendText(dataString)
                        lenLine = self.terminalTextCtrl.GetNumberOfLines()
                        self.reserveLength = self.terminalTextCtrl.GetLineLength(
                            lenLine - 1)
                    else:
                        cursor = self.terminalTextCtrl.GetInsertionPoint()
                        lenLine = self.terminalTextCtrl.GetNumberOfLines()
                        trimPoint = cursor - \
                            self.terminalTextCtrl.GetLineLength(
                                lenLine - 1) + self.reserveLength
                        self.terminalTextCtrl.Remove(trimPoint, cursor)
                        self.tabbed = False
                        self.terminalTextCtrl.AppendText(dataString)

        writer = threading.Thread(target=WriteAll, args=(self.shell,))
        writer.start()

        '''
        try:
            while True:
                d = sys.stdin.read(1)
                if not d:
                    break
                chan.send(d)
        except EOFError:
            # user hit ^Z or F6
            pass
        '''

    def InputToShell(self, event):
        key = event.GetKeyCode()
        lenLine = self.terminalTextCtrl.GetNumberOfLines()
        cursor = self.terminalTextCtrl.PositionToXY(
            self.terminalTextCtrl.GetInsertionPoint())
        cursorLine = cursor[2]
        cursorColumn = cursor[1]
        if key == wx.WXK_TAB:
            aimLine = self.terminalTextCtrl.GetLineText(lenLine-1)
            self.shell.send(aimLine[self.reserveLength:])
            self.shell.send('\t')
            self.tabbed = True
        elif key == wx.WXK_RETURN:
            aimLine = self.terminalTextCtrl.GetLineText(lenLine-1)
            self.shell.send(aimLine[self.reserveLength:] + '\n')
            self.entered = True
        elif key == wx.WXK_BACK:
            if cursorLine < lenLine - 1 or cursorColumn <= self.reserveLength:
                return False
            else:
                event.Skip()
        else:
            if cursorLine < lenLine - 1:
                return False
            event.Skip()

# end of class TerminalFrame
