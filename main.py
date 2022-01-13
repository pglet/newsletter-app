import datetime
import logging
import pglet
from pglet import Stack, Text, Nav, Toolbar, Grid, Column, Tabs, Tab, Textbox, Button, Message
from pglet import nav, toolbar

import settings
import store

logging.basicConfig(level=logging.DEBUG)

class Menu():
    def __init__(self, on_change=None):
        self.on_change = on_change
        self.view = Nav(value="newsletters", on_change=self.menu_change, items=[
            nav.Item(items=[
                nav.Item(key="newsletters", text="Newsletters", icon="Mail"),
                nav.Item(key="settings", text="Settings", icon="Settings")
            ])
        ])

    def menu_change(self, e):
        if self.on_change != None:
            self.on_change(self.view.value)

class NewslettersScreen():
    def __init__(self):
        self.newsletters = Grid(compact=True, header_visible=True, selection_mode='single', preserve_selection=True, on_select=self.grid_select, columns=[
            Column(name="Subject", field_name="subject", sortable='string'),
            Column(name="Date", field_name="created", sortable='string', sorted="desc", max_width=100)
        ], items=store.get_newsletters())

        self.newsletters.selected_items = [self.newsletters.items[0]]
        self.newsletter_details = NewsletterDetails()

        # main view
        self.view = Stack(gap=10, horizontal=True, width="100%", height="100%", controls=[
            Stack(gap=5, width="30%", border_radius=5, padding=5, bgcolor="#fff", controls=[
                Toolbar(items=[
                    toolbar.Item(text='Create newsletter', icon='Add')
                ]),
                Stack(height="100%", scrolly=True, controls=[
                    self.newsletters
                ])                                                   
            ]),
            Stack(gap=5, width="70%", border_radius=5, padding=5, bgcolor="#fff", controls=[
                self.newsletter_details.view
            ])
        ])

    def grid_select(self, e):
        print("Grid select")
        nl = None
        if len(self.newsletters.selected_items) > 0:
            nl = self.newsletters.selected_items[0]
        self.newsletter_details.set_newsletter(nl)

    def activate(self):
        print("Activate NewslettersScreen")
        self.grid_select(None)

class NewsletterDetails():
    def __init__(self): 
        self.toolbar = Toolbar(items=[
                toolbar.Item(text='Send', icon="Send"),
                toolbar.Item(text='Edit', icon="Edit"),
                toolbar.Item(text='Delete', icon="Delete")
            ])
        self.subject = Text(size='xLarge') 
        self.body = Text(markdown=True)

        self.view = Stack(gap=5, height="100%", controls=[
            self.toolbar,
            Stack(padding=10, height="100%", border_top="solid 1px #eee", controls=[
                self.subject,
                self.body
            ])
        ])

    def set_newsletter(self, newsletter):
        self.newsletter = newsletter

        # toggle Toolbar
        self.toolbar.disabled = True if self.newsletter == None else False

        # set subject and body
        self.subject.value = self.newsletter.subject if self.newsletter != None else ""
        self.body.value = self.newsletter.body if self.newsletter != None else ""

        self.view.update()

class SettingsScreen():
    def __init__(self):
        self.message = Message(value='Settings have been updated', dismiss=True, type='success', visible=False)
        self.save_button = Button(primary=True, text="Save", on_click=self.save_click)
        self.private_key = Textbox(label="Private API key")
        self.tabs = Tabs(margin=10, tabs=[
            Tab(text='Mailgun', controls=[
                Stack(gap=30, controls=[
                    self.private_key,
                    Stack(horizontal=True, controls=[
                        self.save_button
                    ])
                ])
            ])
        ])

        # main view combining all controls
        self.view = Stack(width="100%", min_height="100%", border_radius=5, bgcolor="#fff", controls=[
            Stack(padding=20, scrolly=True, controls=[
                Stack(width="50%", controls=[
                    Text("Settings", size='xLarge'),
                    Text("Application settings are saved in `$HOME/.newsletter/config.json` file.", markdown=True),
                    self.message,
                    self.tabs
                ])
            ])
        ])

    # called when the screen is selected in the menu
    # load settings from a file if exists
    def activate(self):
        config = settings.load()
        self.private_key.value = config.mailgunApiKey
        self.view.update()

    # update settings
    def save_click(self, e):
        self.private_key.error_message = "Please enter Mailgun API key" if not self.private_key.value else ""
        if self.private_key.value:
            print("Save!")
            self.message.visible = True
        self.view.update()

def main(page):

    page.padding = 10
    page.vertical_fill = True
    page.title = "Newsletters"
    page.bgcolor = "#f0f0f0"

    screens = {
        "newsletters": NewslettersScreen(),
        "settings": SettingsScreen()
    }

    screen_holder = Stack(width="100%", horizontal_align='center')

    def menu_change(screen_name):
        screen_holder.controls.clear()
        screen_holder.controls.append(screens[screen_name].view)
        page.update()
        screens[screen_name].activate()

    menu = Menu(menu_change).view

    layout = Stack(gap=10, horizontal=True, vertical_fill=True, width="100%", controls=[
        Stack(width="230", height="100%", border_radius=5, padding=5, bgcolor="#fff", controls=[
            menu
        ]),
        screen_holder
    ])

    page.add(layout) 

    menu_change("newsletters")

pglet.app("newsletters", target=main, no_window=True)