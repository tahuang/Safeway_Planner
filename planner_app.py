#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.uix.widget import Widget


class GroceryList(Widget):
    pass

class FoodItem(Widget):
	pass

class PlannerApp(App):
    def build(self):
        return GroceryList()


if __name__ == '__main__':
    PlannerApp().run()