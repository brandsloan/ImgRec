import wx
import cv2, time
import msvcrt

class Screen(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title=title, size=(900,500))

		self.SetBackgroundColour("#E4F1FE")
		self.Show(True)

		self.InitUI()
	def OnFileButton(event, button_label):
		openFileDialog = wx.FileDialog(frame, "Open", "", "", "PNG or JPEG files (*.png)|*.png|*.jpeg|(*.jpeg)", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
		openFileDialog.ShowModal()
		button_label = wx.Bitmap
		print(openFileDialog.GetPath())
	
	def OnStartButton(event, button_label):
		print "Starting"
		exec(VidCapture.py)
		#VidCapture
		
	def OnSliderScroll(self, event):
		obj = event.GetEventObject()
		self.val = obj.GetValue()
		print self.val
		
	def InitUI(self):

		pnlMain = wx.Panel(self, size=(900,500))

		# Setup horizontal box sizer
		self.bsMain = wx.BoxSizer(wx.HORIZONTAL)
		self.bsMain.SetDimension(0,0,900,500)

		# Setup LEFT box sizer
		self.bsLeft = wx.BoxSizer(wx.VERTICAL)
		self.bsLeft.SetMinSize((3*(self.bsMain.GetSize()[0]/4),self.bsMain.GetSize()[1]))
		
		self.bsRight = wx.BoxSizer(wx.VERTICAL)
		self.bsRight.SetMinSize((3*(self.bsMain.GetSize()[0]/4),self.bsMain.GetSize()[1]))

        # Make add button
		BasePic = wx.Button(pnlMain, label="Select Base Image", size=(100,100))
		EndButton = wx.Button(pnlMain, label="End", size=(100, 50))
		StartButton = wx.Button(pnlMain, label="Start", size=(100, 50))
		self.eTol = wx.Slider(pnlMain, value=95, minValue=0, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
		self.timed = wx.SpinButton(pnlMain, -1) 
		BasePic.Bind(wx.EVT_BUTTON, self.OnFileButton)
		EndButton.Bind(wx.EVT_BUTTON, self.OnStartButton)
		StartButton.Bind(wx.EVT_BUTTON, self.OnStartButton)
		self.eTol.Bind(wx.EVT_SCROLL, self.OnSliderScroll)
		# Add all the components to the LEFT sizer
		self.bsLeft.Add(BasePic, 0, wx.ALIGN_TOP | wx.ALIGN_LEFT)
		self.bsRight.Add(EndButton, 0, wx.ALIGN_LEFT)
		self.bsLeft.Add(StartButton, 0 ,wx.ALIGN_RIGHT)
		self.bsRight.Add(self.eTol, 1, wx.ALIGN_LEFT)
		self.bsLeft.Add(self.timed, 0, wx.ALIGN_LEFT)
		# Add the vertical sizers to the horizontal sizer
		self.bsMain.Add(self.bsLeft)
		self.bsMain.Add(self.bsRight)

		# Add the vertical sizer to the panel
		pnlMain.SetSizer(self.bsMain)
		self.bsMain.Layout()

if __name__ == '__main__':
	app = wx.App(False)
	frame = Screen(None, 'Layout')
	app.MainLoop()