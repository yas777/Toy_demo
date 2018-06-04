import sys, os
import gi
import time
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject, Gtk
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

# gint res

class GTK_Main(object):
	def __init__(self):
		window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
		window.set_title("Video-Player")
		window.set_default_size(900, 600)
		# color = window.get_property("background-color")
		# print(color)
		window.connect("destroy", Gtk.main_quit, "WM destroy")
		vbox = Gtk.VBox()
		window.add(vbox)
		hbox = Gtk.HBox()
		hbox1 = Gtk.HBox()
		self.Lb1 = Gtk.Label("")
		vbox.pack_start(hbox, False, False, 0)
		vbox.pack_start(self.Lb1,False,False,0)
		vbox.pack_start(hbox1,True,True,50)
		self.label = Gtk.Label("Select the video - ")
		hbox.pack_start(self.label,False,False,150)
		self.button = Gtk.Button("Browse")
		hbox.pack_start(self.button, False, False, 350)
		self.button.connect("clicked", self.start_stop)
		self.movie_window = Gtk.DrawingArea()
		# self.movie_window.connect("button-press-event", self.pause)
		# self.movie_window.set_size_request(300,300)
		# self.movie_window.modify_bg(Gtk.StateType.NORMAL,Gtk.Gdk.Color(red=255.000000, green=255.000000, blue=0.000000, alpha=0.000000))  
		# vbox.add(self.movie_window)
		hbox1.pack_start(self.movie_window,True,True,50)
		window.show_all()
		self.player = Gst.ElementFactory.make("playbin", "player")
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect("message", self.on_message)
		bus.connect("sync-message::element", self.on_sync_message)

	# def pause(self,w):s
	# 	# print("PAUSE.............................")
	# 	# print(self.player.get_state())
	# 	if self.player.get_state(0) == "<enum GST_STATE_PLAYING of type Gst.State>":
	# 		self.player.set_state(Gst.State.PAUSED)
	# 	else:
	# 		self.player.set_state(Gst.State.PLAYING)

	def start_stop(self, w):
		if self.button.get_label() == "Browse":
			# filepath = self.entry.get_text().strip()
			#GtkFileChooserAction action = GTK_FILE_CHOOSER_ACTION_OPEN
			act = Gtk.FileChooserAction.OPEN
			dialog = Gtk.FileChooserDialog("Open File",None,act,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
			response = dialog.run()
			filepath = dialog.get_filename()
			dialog.destroy()
			print(filepath)
			# res = gtk_dialog_run(GTK_DIALOG(dialog))
			# if res == GTK_RESPONSE_ACCEPT:
			# 	# char *filename
			# 	chooser = GTK_FILE_CHOOSER(dialog)
			# 	filepath = gtk_file_chooser_get_filename(*chooser)
		 #    	# open_file (filename);
		 #    	# g_free (filename);
			# gtk_widget_destroy(dialog)
		# if self.button.get_label() == "Stop":
		# 	self.player.set_state(Gst.State.PAUSED)
		if os.path.isfile(filepath):
			filepath = os.path.realpath(filepath)
			self.button.set_label("Stop")
			self.player.set_property("uri", "file://" + filepath)
			self.player.set_state(Gst.State.PLAYING)
			# self.player.set_state(Gst.State.PAUSED)
			# time.sleep(3)
			# self.player.set_state(Gst.State.PAUSED)
			print(self.player.get_state(0).state)
			print("STATE....................!!!!!!!!!!!!!!!!!!")
			chosen_file = os.path.basename(filepath)
			self.Lb1.set_label("Selcted Video : " + chosen_file)
			# self.button.set_label(None)# self.label = "bla"	
			# self.label = Gtk.Label("Selected Video : " + filepath)
			# self.button.Label(None)
		else:
			self.player.set_state(Gst.State.NULL)
			self.button.set_label("Browse")

	def on_message(self, bus, message):
		t = message.type
		if t == Gst.MessageType.EOS:
			self.player.set_state(Gst.State.NULL)
			self.button.set_label("Browse")
		elif t == Gst.MessageType.ERROR:
			self.player.set_state(Gst.State.NULL)
			err, debug = message.parse_error()
		# print("Error: %s" % err, debug)
		self.button.set_label("Browse")

	def on_sync_message(self, bus, message):
		if message.get_structure().get_name() == 'prepare-window-handle':
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			imagesink.set_window_handle(self.movie_window.get_property('window').get_xid())

GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()