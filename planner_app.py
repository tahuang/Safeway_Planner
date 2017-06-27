#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

Builder.load_string('''
<RootWidget>:
	BoxLayout:
		GridLayout:
			rows: 10
			Button:
				text: 'Foods'
		GridLayout:
			col: 7
    		Button:
    			text: 'Monday'
    		Button:
    			text: 'Tuesday'
    		Button:
    			text: 'Wednesday'
    		Button:
    			text: 'Thursday'
    		Button:
    			text: 'Friday'
    		Button:
    			text: 'Saturday'
    		Button:
    			text: 'Sunday'
''')

class RootWidget(BoxLayout):
    pass

class GroceryList(App):

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    GroceryList().run()