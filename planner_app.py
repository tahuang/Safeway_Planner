#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class GroceryList(Widget):
    cookies = ObjectProperty(None)

class FoodItem(Widget):
	def on_touch_move(self, touch):
		self.center_x = touch.x
		self.center_y = touch.y

class PlannerApp(App):
    def build(self):
        return GroceryList()


if __name__ == '__main__':
    PlannerApp().run()