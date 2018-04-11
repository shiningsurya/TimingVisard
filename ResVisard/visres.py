#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import sys
from param import Param
from tempo2res import Tempo2Res
import logging
logging.basicConfig(filename='visres.log', level=logging.INFO)
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

class VisRes(wx.Frame):
    '''
    The Main class of the application
    '''
    title = "Visualize Residuals on the fly"

    def __init__(self, *args, **kw):
        #### 
        # some arg passing
        if len(sys.argv) < 2:
            print "visres.py <PAR FILE> <TIM FILE>"
            sys.exit(0) # bye bye
        self.parfile = sys.argv[1]
        self.timfile = sys.argv[2]
        # le OOP
        self.myres = Tempo2Res(timfile=self.timfile,parfile=self.parfile)
        self.myres.fit(self.parfile,self.timfile)    
        wx.Frame.__init__(self, None, -1, self.title)
        self.sliders = [] # container to hold sliders

        self.InitUI()
       # 
        self.create_menu() # create menu
        self.statusbar = self.CreateStatusBar() # create status bar
        self.create_figure() # creates figure
   
    def create_figure(self):
        """ Creates the main panel with all the controls on it:
             * mpl canvas 
             * mpl navigation toolbar
             * Control panel for interaction
        """
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100 
        self.fig = Figure((self.xfig//(1*self.dpi), self.yfig//(1.2*self.dpi)), dpi=self.dpi)
        self.canvas = FigCanvas(self.pnl_plot, -1, self.fig)
        
        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        #
        self.axes = self.fig.add_subplot(111)
        self.plotter(self.myres.toas,self.myres.res,self.myres.toaerr)
        # from PIL import Image
        # img = Image.open('./joy-division-unknown-pleasures.jpg')
        # self.axes.imshow(img)
        # self.axes.set_title("Visualize Residuals")
        # self.axes.set_xlabel('MJD')
        # self.axes.set_ylabel('Residuals')
        # Bind the 'pick' event for clicking on one of the bars
        #
        # self.canvas.mpl_connect('pick_event', self.on_pick)
    def plotter(self,toa,res,toaerr):
        # self.axes.clear()
        self.axes.cla()
        self.axes.errorbar(toa,res,yerr=1e-6*toaerr,fmt='.',c='green')
        self.axes.set_title("Visualize Residuals")
        self.axes.set_xlabel('MJD')
        self.axes.set_ylabel('Residuals')
    def create_menu(self):
        '''
        On the title bar wale
        '''
        self.menubar = wx.MenuBar()
        
        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu()
        m_about = menu_help.Append(-1, "&About\tF1", "About the Visualizer")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.SetMenuBar(self.menubar)
    
    def on_exit(self, event):
        self.Destroy()
        
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
        
    def on_about(self, event):
        msg = """ Residuals Visualizer 

        *Tweak the parameters in the par file 
        *See the structures that come in the residuals
        *Repeat

        ---------------------------------------------
        The original motivation is to understand how wrong parameters 
	affect the residuals and in which way. 
        Fruit of discussions of Prakash Aragamuswamy and Suryarao Bethapudi. 
        We will put it up on Github and make it super interactive 
        and publish it on distill.pub
        
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def InitUI(self):   
        self.SetTitle('ResVisard')
        self.Centre()
        self.Show(True)    
        self.Maximize(True)
        self.dx, self.dy = wx.DisplaySize() # returns a tuple
        '''
        Display size logic 
        | 20  |  .....   | 20   | 250   | 20  |
        | Pad | Plot     | Pad  | SL    | 20  |
        '''
        self.pnl_param = Param(self,(1000,20),(350,self.dy))
        self.xfig, self.yfig = 900,self.dy-40
        self.pnl_plot  = wx.Panel(self,pos=(20,20), size=(self.xfig,self.yfig))#,size=(self.dx-180,self.dy-40))
        # self.pnl_plot.SetForegroundColour('Blue')
        self.fitb = wx.Button(self,pos=(930,20),size=(60,self.dy/2-100),style=wx.BU_EXACTFIT,label='FIT')
        self.fitb.Bind(wx.EVT_BUTTON,self.on_fit)
        self.resetb = wx.Button(self,pos=(930,self.dy/2-80),size=(60,self.dy/2-100),style=wx.BU_EXACTFIT,label='RESET')
        self.resetb.Bind(wx.EVT_BUTTON,self.on_reset)
        ####
    def on_reset(self,event):
        self.pnl_param.reset()
        self.myres.fit(self.parfile,self.timfile)
        self.plotter(self.myres.toas,self.myres.res,self.myres.toaerr)
    def on_fit(self,event):
        '''
        Perhaps the main fuction
        '''
        # Read params from Param
        # Update PAR file
        # Compute residuals
        # Plot
        self.pnl_param.update_book() 
        self.myres.fit(pfile='./.temp_par_file',tfile='test.tim')
        logging.info('Refitting')
        # print "hdhahha"
        self.plotter(self.myres.toas,self.myres.res,self.myres.toaerr)
def main():
    ex = wx.App()
    VisRes(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()  
