from pario import ParIO
import wx
import wx.lib.scrolledpanel as scrolled

class Param(scrolled.ScrolledPanel):
    def __init__(self, frame, pos,size,smin=-100,smax=100,sdef=0):
        '''
        name -> Name of the Param
        origin -> relative origin from where CheckBox and Slider is placed
        smin, smax, sdef slider properties
        00
        origin is a tuple
        '''
        # scrolled.ScrolledPanel.__init__(self,pos=pos,size=size)
        self.par = ParIO()
        # size[1] = 90 * self.par.npars 
        super(Param,self).__init__(frame,pos=pos,size=size)
        self.min = smin 
        self.max = smax 
        self.sdef = sdef
        self.xo, self.yo = pos 
        self.checkboxes = [] # container for checkboxes
        self.sliders = [] # container for sliders
        self.initui()
        self.SetupScrolling()
        self.SetAutoLayout(True)
    
    def initui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        for i,n in enumerate(self.par.name_pars):
            cb = wx.CheckBox(self,label=n,pos=(self.xo,self.yo+5))
            cb.Bind(wx.EVT_CHECKBOX,self.on_cb)
            self.checkboxes.append(cb)
            vbox.Add(cb,0,wx.ALIGN_LEFT,5)
            sl = wx.Slider(self,5,0,-100,100,(self.xo,self.yo+20),(300,60),style= wx.SL_LABELS|wx.SL_AUTOTICKS)
            self.sliders.append(sl)
            vbox.Add(sl,0,wx.ALIGN_LEFT,5)
            # vbox.Add(wx.StaticLine(self,pos=(self.xo,self.yo+65),size=(250,-1)))
        self.SetSizer(vbox)
        #
    def update_book(self):
        # returns the params to update
        names, values = [],[] # to be sent to pario
        for i,(cb,sl) in enumerate(zip(self.checkboxes,self.sliders)):
            if cb.GetValue():
                n = self.par.name_pars[i]
                names.append(n)
                values.append(sl.GetValue())
        self.par.updateParams(names,values) 
    def reset(self):
        for cb,sl in zip(self.checkboxes,self.sliders):
            cb.SetValue(0) # reset check box
            sl.SetValue(self.sdef)
    def on_cb(self,event):
        # if checkbox is unchecked, reset the slider to default
        # if checkbox is checked --> unchecked : reset to default
        # if checkbox is unchecked --> checked : don't do anything
        cb = event.GetEventObject()
        sl = self.sliders[self.checkboxes.index(cb)]
        if not cb.GetValue():
            sl.SetValue(self.sdef)

