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

    home_button = Gtk.ToolButton()
    back_button = Gtk.ToolButton()
    forward_button = Gtk.ToolButton()
    reload_button = Gtk.ToolButton()

    security = Gtk.Label()

    img = Gtk.Image()

    def __init__(self):
        self.window.connect('destroy', Gtk.main_quit)

        self.header_bar.set_title(self.title)
        self.header_bar.set_subtitle("Browsing for everyone, everytime.")
        self.header_bar.set_show_close_button(True)

        self.window.set_size_request(900, 600)

        if path.exists('/usr/share/pixmaps/prism/homepage/index.html'):
            self.default_url = 'file:///usr/share/pixmaps/prism/homepage/index.html'

        if 'file:///'  in self.default_url:
            self.security.set_label('🏠  |  Home')
        elif 'https' in self.default_url:
            self.security.set_label('🔒  |  Home')
        else:
            self.security.set_label('🔓  |  Home')

        self.initialize_widgets()
        self.connect_signals()

        self.window.set_titlebar(self.header_bar)
        self.window.show_all()

    def initialize_widgets(self):
        img = Gtk.Image()

        if path.exists('/usr/share/pixmaps/prism/prism_32.png'):
            img.set_from_file('/usr/share/pixmaps/prism/prism_32.png')

        self.home_button.set_icon_widget(img)

        self.img = Gtk.Image()

        if path.exists('/usr/share/pixmaps/prism/white_arrow_left.png'):
            self.img.set_from_file('/usr/share/pixmaps/prism/white_arrow_left.png')

        self.back_button.set_icon_widget(self.img)

        self.img = Gtk.Image()

        if path.exists('/usr/share/pixmaps/prism/white_arrow_right.png'):
            self.img.set_from_file('/usr/share/pixmaps/prism/white_arrow_right.png')
        else:
            self.img.set_from_icon_name('go-next', Gtk.IconSize.SMALL_TOOLBAR)

        self.forward_button.set_icon_widget(self.img)


        self.img = Gtk.Image()

        if path.exists('/usr/share/pixmaps/prism/white_refresh.png'):
            self.img.set_from_file('/usr/share/pixmaps/prism/white_refresh.png')
        else:
            self.img.set_from_icon_name('view-refresh', Gtk.IconSize.SMALL_TOOLBAR)

        self.reload_button.set_icon_widget(self.img)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.webview.load_uri(self.default_url)

        self.back_button.connect('clicked', self.go_back)
        self.forward_button.connect('clicked', self.go_forward)
        self.reload_button.connect('clicked', self.reload)

        box.add(self.home_button)
        box.add(self.url_bar)
        box.add(self.back_button)
        box.add(self.forward_button)
        box.add(self.reload_button)
        box.add(self.security)

        self.header_bar.pack_start(box)

        self.scrolled_window.add(self.webview)

        self.window.add(self.scrolled_window)

    def connect_signals(self):
        self.webview.connect('load_changed', self.on_load_changed)

        self.url_bar.connect('activate', self.on_activate)

    def on_load_changed(self, data, web):
        self.url_bar.set_text(self.webview.get_uri())
        self.on_check_security()

    def on_check_security(self):
        if 'file:///'  in self.webview.get_uri():
            self.security.set_label('🏠  |  Home')

            if self.webview.get_uri() == self.default_url:
                self.url_bar.set_text('prisma:home')
        elif 'https' in self.webview.get_uri():
            self.security.set_label('🔒  |  Secure')
        else:
            self.security.set_label('🔓  |  Unsecure')

    def on_activate(self, data):
        url = self.url_bar.get_text()

        if url == 'prisma:home':
            self.webview.load_uri(self.default_url)
            return

        self.on_check_security()

        if 'http' in url and not 'https' in url:
            if 'google' in self.default_url:
                url = self.default_url + '/search?q=' + self.url_bar.get_text()
            elif 'duckduckgo' in self.default_url:
                url = self.default_url + '?q='        + self.url_bar.get_text()
            else:
                url = self.default_url + '/'          + self.url_bar.get_text()
        else:
            url = self.default_protocol + self.url_bar.get_text()

        self.webview.load_uri(url)

    def go_back(self, data):
        self.webview.go_back()

    def go_forward(self, data):
        self.webview.go_forward()

    def reload(self, data):
        self.webview.reload()


prism = Prisma()
prism.__init__()
Gtk.main()
