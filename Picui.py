import wx

class MyFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.Show(True)
		
		#panel.Layout()
		
		self.button_1 = wx.Button(self, wx.ID_ANY, ("Select File"))
		self.button_1.Bind(wx.EVT_BUTTON, self.OnFileButton)
			
		self.button_2 = wx.Button(self, wx.ID_ANY, ("Start"))
		self.button_2.Bind(wx.EVT_BUTTON, self.OnStartButton)
		
		self.button_3 = wx.Button(self, wx.ID_ANY, ("TEST"))
		self.button_3.Bind(wx.EVT_BUTTON, self.OnStartButton)
		
		self.__set_properties()
		self.__do_layout()
		
	def __set_properties(self):
		self.SetTitle("Picui")
		
	def __do_layout(self):
		wx.Frame.SetSize(self, 0, 0, 800, 600)

		panel = wx.Panel(self, size = (800, 600))
		self.bs = wx.BoxSizer(wx.HORIZONTAL)
		self.bs.SetDimension(0, 0, 800, 600)
		
		self.bsLeft = wx.BoxSizer(wx.VERTICAL)
		self.bsLeft.SetMinSize((3*self.GetSize()[0]/4, self.GetSize()[1]))
		#bs.Fit(self)
		
		self.bs.Add(self.button_1, 0, wx.ALL, 5)
		self.bsLeft.Add(self.button_2, 250, wx.ALL, 250)
		self.bs.Add(self.button_3, 600, wx.ALL, 100)
		
		self.Layout()
		self.Update()
		
	def OnFileButton(event, button_label):
		openFileDialog = wx.FileDialog(frame, "Open", "", "", "PNG or JPEG files (*.png)|*.png|*.jpeg|(*.jpeg)", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal()
		print(openFileDialog.GetPath())
	
	def OnStartButton(event, button_label):
		print "Starting"

app = wx.App()
wx.InitAllImageHandlers()
frame = MyFrame(None ,wx.ID_ANY, "")
frame.Centre()
frame.Show()
app.MainLoop()