#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, ListProperty, StringProperty
from kivy.graphics import Color, Line

# Builder used to load all the kivy files
Builder.load_file('recipe.kv')
Builder.load_file('meals.kv')
Builder.load_file('days.kv')

class GroceryList(BoxLayout):
	def __init__(self,**kwargs):
		super(GroceryList,self).__init__(**kwargs)

class Recipes(Widget):
	def __init__(self,**kwargs):
		super(Recipes,self).__init__(**kwargs)

	def on_touch_down(self, touch):
		if self.collide_point(*touch.pos):
			touch.grab(self)
            # do whatever else here

	def on_touch_move(self, touch):
		if touch.grab_current is self:
			self.pos = touch.pos
            # now we only handle moves which we have grabbed
	
	def on_touch_up(self, touch):
		if touch.grab_current is self:
			touch.ungrab(self)
            # and finish up here

class Meals(GridLayout):
	def __init__(self, **kwargs):
		super(Meals,self).__init__(**kwargs)

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
	grid_location = StringProperty('on_top')

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
		iters = 0
		grid_width_spacing = width / 7
		grid_height_spacing = height / 3
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
			iters = 0
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