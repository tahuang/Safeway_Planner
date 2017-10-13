#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.uix.textinput import TextInput

import build_list
import safeway

# Builder used to load all the kivy files
Builder.load_file('days.kv')

class Planner(BoxLayout):
	def __init__(self,**kwargs):
		super(Planner,self).__init__(**kwargs)

class GetRouteButton(Button):
	meals = ObjectProperty()

	def getGroceryRoute(self, meal_list):
		items = dict()
		for meal in meal_list:
			if meal.text == '':
				continue
			meal_parts = meal.text.split('\n')
			for part in meal_parts:
				if items.has_key(part):
					items[part] += 1
				else:
					items[part] = 1

		build_list.build_list(items)
		safeway.print_shopping_route()

	def __init__(self,**kwargs):
		super(GetRouteButton,self).__init__(**kwargs)

class Meals(GridLayout):
	def __init__(self, **kwargs):
		super(Meals,self).__init__(**kwargs)
		self.meal_list = []
		self.rows = 4
		self.cols = 7
		for row in range(self.rows):
			for column in range(self.cols):
				meal_entry = TextInput()
				self.meal_list.append(meal_entry)
				self.add_widget(meal_entry)

class PlannerApp(App):
    def build(self):
        self.title = 'Grocery Planner'
        return Planner()

if __name__ == '__main__':
    PlannerApp().run()