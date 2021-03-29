#!/usr/bin/env python3

# MIT License
#
# Copyright (c) 2021 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#

# Prisma
#   Python3 implementation of Webkit2 web-engine based Prism web-browser (executable)
#
#   github.com/ferhatgec/prism
#

# TODO:
# More fonts.

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2
from os import path

class Prisma(Gtk.Window):
    title = 'Fegeya Prisma'
    default_url = 'http://duckduckgo.com'
    default_protocol = 'http'

    window = Gtk.Window(title=title)
    webview = WebKit2.WebView()
    header_bar = Gtk.HeaderBar()

    scrolled_window = Gtk.ScrolledWindow()
    url_bar = Gtk.Entry()

    back_button = Gtk.Button()
    forward_button = Gtk.Button()
    reload_button = Gtk.Button()

    logo = Gtk.Image()

    def __init__(self):
        self.window.connect('destroy', Gtk.main_quit)

        self.header_bar.set_title(self.title)
        self.header_bar.set_subtitle("Browsing for everyone, everytime.")
        self.header_bar.set_show_close_button(True)

        self.window.set_size_request(900, 600)

        if path.exists('/usr/share/pixmaps/prism/prism_32.png'):
            self.logo.set_from_file('/usr/share/pixmaps/prism/prism_32.png')
            self.header_bar.pack_start(self.logo)

        self.initialize_widgets()
        self.connect_signals()

        self.window.set_titlebar(self.header_bar)
        self.window.show_all()

    def initialize_widgets(self):
        img = Gtk.Image()
        img.set_from_icon_name('go-previous', Gtk.IconSize.SMALL_TOOLBAR)
        self.back_button.set_image(img)

        img = Gtk.Image()
        img.set_from_icon_name('go-next', Gtk.IconSize.SMALL_TOOLBAR)

        self.forward_button.set_image(img)

        img = Gtk.Image()
        img = img.set_from_icon_name('view-refresh', Gtk.IconSize.SMALL_TOOLBAR)
        self.reload_button.set_image(img)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.webview.load_uri(self.default_url)

        self.back_button.connect('clicked', self.go_back)
        self.forward_button.connect('clicked', self.go_forward)
        self.reload_button.connect('clicked', self.reload)

        box.add(self.url_bar)
        box.add(self.back_button)
        box.add(self.forward_button)
        box.add(self.reload_button)

        self.header_bar.pack_start(box)

        self.scrolled_window.add(self.webview)

        self.window.add(self.scrolled_window)

    def connect_signals(self):
        self.url_bar.connect('activate', self.on_activate)

    def on_activate(self, data):
        self.webview.load_uri(self.url_bar.get_text())

    def go_back(self, data):
        self.webview.go_back()

    def go_forward(self, data):
        self.webview.go_forward()

    def reload(self, data):
        self.webview.reload()


prism = Prisma()
prism.__init__()
Gtk.main()
