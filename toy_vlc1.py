#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import vlc
import subprocess
import time

import gi
gi.require_version('Gtk','3.0')

from gi.repository import Gtk, Gio, Gdk, GLib

class Handler:

    def on_play_here_realize(self, widget):
        vlcOptions = "--no-xlib"
        self.win_id = widget.get_window().get_xid()
        self.setup_player(vlcOptions)
        self.player.audio_set_mute(False)
        self.is_playing = False

    def on_rotate_toggled(self, widget):
        pos = self.player.get_position()
        self.player.stop()
        self.player.release()
        self.vlcInstance.release()
        if widget.get_active():
            vlcOptions = "--no-xlib --video-filter=transform{type=180}"
        else:
            vlcOptions = "--no-xlib"
        self.setup_player(vlcOptions)
        self.player.set_mrl(self.video)
        self.player.play()
        self.player.set_position(pos)
        if not self.is_playing:
            time.sleep(.05)
            self.player.pause()

    def setup_player(self, options):
        self.vlcInstance = vlc.Instance(options)
        self.player = self.vlcInstance.media_player_new()
        self.player.set_xwindow(self.win_id)

    def on_backward_clicked(self, widget):
        skip_pos = go.slider.get_value() - 10
        if skip_pos < 0:
            self.player.set_position(0)
            go.slider.set_value(0)
        else:
            self.player.set_position(skip_pos / 100)
            go.slider.set_value(skip_pos)

    def on_forward_clicked(self, widget):
        skip_pos = go.slider.get_value() + 10
        if skip_pos > 100:
            self.player.pause()
            self.player.set_position(0.99)
            go.slider.set_value(100)
        else:
            self.player.set_position(skip_pos / 100)
            go.slider.set_value(skip_pos)

    def on_playpause_togglebutton_toggled(self, widget):
        if widget.get_active():
            img = Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_PLAY,Gtk.IconSize.BUTTON)
            widget.set_property("image",img)
            self.is_playing = False
        else:
            img = Gtk.Image.new_from_stock(Gtk.STOCK_MEDIA_PAUSE,Gtk.IconSize.BUTTON)
            widget.set_property("image",img)
            self.is_playing = True
        self.player.pause()
        GLib.timeout_add(1000, self.update_slider)

    def on_vbutton_clicked(self, widget):
        if widget.get_label() == "Browse":
            go.obj("vbutton").set_sensitive(False)
            # filepath = self.entry.get_text().strip()
            #GtkFileChooserAction action = GTK_FILE_CHOOSER_ACTION_OPEN
            act = Gtk.FileChooserAction.OPEN
            dialog = Gtk.FileChooserDialog("Open File",None,act,(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            response = dialog.run()
            filepath = dialog.get_filename()
            dialog.destroy()
            if os.path.isfile(filepath):
                # col = Gdk.Color(220,220,220)
                # # window.present()
                # go.obj("box1").apply_default_background()
                go.obj("play_here").show()
                go.obj("box3").show()
                filepath = os.path.realpath(filepath)
                self.video = "file://"+filepath
                self.duration = go.get_duration(self.video)
                self.player.set_mrl(self.video)
                self.is_playing = True
                go.slider.set_value(0)
                go.obj("playpause_togglebutton").set_active(False)
                go.obj("playpause_togglebutton").set_sensitive(True)
                go.obj("mute").set_sensitive(True)
                # go.obj("rotate").set_sensitive(True)
                self.player.play()
                GLib.timeout_add(1000, self.update_slider)


    def on_ibutton_clicked(self, widget):
        image = "file://"+os.path.abspath("mediaplayer.jpg")
        self.player.set_mrl(image)
        self.is_playing = False
        self.player.play()
        go.obj("playpause_togglebutton").set_sensitive(False)
        go.obj("mute").set_sensitive(False)
        # go.obj("rotate").set_sensitive(False)

    def on_mute_toggled(self, widget):
        if widget.get_active():
            widget.set_label("Unmute")
        else:
            widget.set_label("Mute")
        self.player.audio_toggle_mute()

    def on_progress_change_value(self, widget, scroll, value):

        if self.duration == go.slider.get_value():
            print("yessssssss..................")
        self.player.set_position(value / 100)
        widget.set_value(value)

    def update_slider(self):
        if go.slider.get_value() == 100:
            # time.sleep(2)
            go.obj("vbutton").set_sensitive("True")
        if not self.is_playing:
            return False # cancel timeout
        else:
            pos = go.slider.get_value()
            new_pos = (pos + 100 / self.duration)
            go.slider.set_value(new_pos)
            if new_pos > 100:
                self.is_playing = False
        return True # continue calling every x milliseconds

class VlcPlayer:

    def __init__(self):
        self.app = Gtk.Application.new("org.media.player", Gio.ApplicationFlags(0))
        self.app.connect("activate", self.on_app_activate)

    def on_app_activate(self, app):
        #setting up builder
        builder = Gtk.Builder()
        builder.add_from_file("20_vlc_player3.glade")
        builder.connect_signals(Handler())
        self.obj = builder.get_object
        #slider position is float between 0..100
        self.slider = self.obj("progress")
        window = self.obj("window")
        window.set_application(app)
        window.show_all()
        go.obj("play_here").hide()
        go.obj("box3").hide()
        go.obj("headbox1").show()
        # ob1 = window.get_object("box1")
        # window.add(ob1)

    def get_duration(self,video):
        command = ['ffprobe',
                        '-v', "error",
                        '-show_entries', "format=duration",
                        '-of', 'default=noprint_wrappers=1:nokey=1',
                        video
                        ]
        ffprobe_cmd = subprocess.run(command, stdout=subprocess.PIPE)
        #stdout of subprocess is byte variable, convert into float then into integer
        return int(float(ffprobe_cmd.stdout.decode()))

    def run(self, argv):
        self.app.run(argv)

go = VlcPlayer()
go.run(None)
