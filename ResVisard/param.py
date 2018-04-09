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

        self.initui()
        self.SetupScrolling()
        self.SetAutoLayout(True)
    
    def initui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        for i,n in enumerate(self.par.name_pars):
            cb = wx.CheckBox(self,label=n,pos=(self.xo,self.yo+5))
    #TODO:        self.Bind(wx.EVT_CHECKBOX,self.on_cb, cb)
            vbox.Add(cb,0,wx.ALIGN_LEFT,5)
            vbox.Add(wx.Slider(self,5,0,-100,100,(self.xo,self.yo+20),(300,60),style= wx.SL_LABELS|wx.SL_AUTOTICKS),0,wx.ALIGN_LEFT,5)
            # vbox.Add(wx.StaticLine(self,pos=(self.xo,self.yo+65),size=(250,-1)))
        self.SetSizer(vbox)
        #
    def read_cb(self):
        return self.cb.GetValue()
    def read_slider(self):
        return self.slider.GetValue()
    def on_cb(self,event):
        # if checkbox is unchecked, reset the slider to default
        # if checkbox is checked --> unchecked : reset to default
        # if checkbox is unchecked --> checked : don't do anything
        if not self.cb.GetValue():
            self.slider.SetValue(self.sdef)

