#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

# Builder used to load all the kivy files
Builder.load_file('recipe.kv')
Builder.load_file('meals.kv')
Builder.load_file('days.kv')

class GroceryList(BoxLayout):
	def __init__(self,**kwargs):
		super(GroceryList,self).__init__(**kwargs)

class Recipes(BoxLayout):
	def __init__(self,**kwargs):
		super(Recipes,self).__init__(**kwargs)

	def on_touch_move(self, touch):
		self.center_x = touch.x
		self.center_y = touch.y

class Meals(GridLayout):
	def __init__(self,**kwargs):
		super(Meals,self).__init__(**kwargs)

class PlannerApp(App):
    def build(self):
        self.title = 'Grocery Planner'
        return GroceryList()

if __name__ == '__main__':
    PlannerApp().run()