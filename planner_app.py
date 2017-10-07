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
from kivy.graphics import Color, Line
from kivy.uix.textinput import TextInput

import build_list
import safeway

# Builder used to load all the kivy files
Builder.load_file('recipe.kv')
#Builder.load_file('meals.kv')
Builder.load_file('days.kv')

class GroceryList(BoxLayout):
	def __init__(self,**kwargs):
		super(GroceryList,self).__init__(**kwargs)

class Recipes(Widget):
	def __init__(self,**kwargs):
		super(Recipes,self).__init__(**kwargs)

class Meals(GridLayout):
	def getGroceryList(self, button):
		items = dict()
		for meal in meal_list:
			if items.has_key(meal.text):
				items[meal.text] += 1
			else:
				items[meal.text] = 1

		build_list.build_list(items)
		safeway.print_shopping_route()

	button = Button(text='Get Grocery List')
	button.bind(on_press=getGroceryList)

	def __init__(self, **kwargs):
		super(Meals,self).__init__(**kwargs)
		meal_list = []
		self.rows = 4
		self.cols = 7
		for row in range(self.rows):
			for column in range(self.cols):
				meal_entry = TextInput()
				meal_list.append(meal_entry)
				self.add_widget(meal_entry)


class DrawGrid(Widget):
	# Width of grid lines
	grid_line_width = NumericProperty(2.)
	# Color of grid lines in rgba
	grid_line_color = ListProperty([0., 0., 0., 1.])
	# Color of line around grid
	grid_outline_color = ListProperty([0., 0., 0., 1.])
	# Width of grid outline
	grid_outline_width = NumericProperty(2.)
	# Location of grid lines, takes 'behind' or 'on_top'
	grid_location = StringProperty('behind')

	def __init__(self,**kwargs):
		super(DrawGrid,self).__init__(**kwargs)
		self.draw_grid()

	def on_size(self, instance, value):
		self.canvas.before.clear()
		self.canvas.after.clear()
		self.draw_grid()


	def draw_grid(self):
		canvas = self.canvas.after
		if self.grid_location == 'behind':
			canvas = self.canvas.before
		width = self.size[0]
		height = self.size[1]
		iters = 1
		grid_width_spacing = width / 7.0
		grid_height_spacing = height / 3.0
		#draw grid interior
		with canvas:
			Color(rgba=self.grid_line_color)
			while width >= grid_width_spacing:
				Line(width=self.grid_line_width,
					points=(self.pos[0] + iters*grid_width_spacing, 
						self.pos[1], 
						self.pos[0] + iters*grid_width_spacing, 
						self.pos[1] + self.size[1]))
				width -= grid_width_spacing
				iters += 1
			iters = 1
			while height >= grid_height_spacing:
				Line(width=self.grid_line_width,
					points=(self.pos[0], 
						self.pos[1] + iters*grid_height_spacing, 
						self.pos[0] + self.size[0], 
						self.pos[1] + iters*grid_height_spacing))
				height -= grid_height_spacing
				iters += 1
		#draw grid outline
		with self.canvas.after:
			Color(self.grid_outline_color)
			Line(width=self.grid_outline_width, 
				rectangle=(self.pos[0], self.pos[1], 
				self.size[0], self.size[1]))


class PlannerApp(App):

    def build(self):
        self.title = 'Grocery Planner'
        return GroceryList()

if __name__ == '__main__':
    PlannerApp().run()