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
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp

import numpy as np
import glob

import build_list
import safeway

# Builder used to load all the kivy files
Builder.load_file('days.kv')

class Planner(BoxLayout):
        def __init__(self,**kwargs):
                super(Planner,self).__init__(**kwargs)

class GetRouteButton(Button):
        meals = ObjectProperty()
        shopping_area = ObjectProperty()

        # Reads text input from user and creates grocery route.
        def getGroceryRoute(self, meal_list, map_file):
                items = dict()
                # Parse each meal block for different items
                for meal in meal_list:
                        if meal.text == '':
                                continue
                        meal_parts = meal.text.split('\n')
                        for part in meal_parts:
                                if part[0] == '!':
                                        continue
                                if items.has_key(part):
                                        items[part] += 1
                                else:
                                        items[part] = 1

                build_list.build_list(items)
                safeway.print_shopping_route(map_file)

        def __init__(self,**kwargs):
                super(GetRouteButton,self).__init__(**kwargs)
                self.background_normal = ''
                self.background_color = [0.698039, 0.133333, 0.133333, 1]

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

class Recipes(GridLayout):
        def __init__(self, **kwargs):
                super(Recipes,self).__init__(**kwargs)
                # Get all the recipe names from file
                recipe_list = []
                recipe_file = open('recipes.txt')
                recipe_name_flag = True
                for line in recipe_file:
                        if recipe_name_flag == True:
                                recipe_name = line.rstrip('\n')
                                recipe_list.append(recipe_name)
                                recipe_name_flag = False
                        elif (line == '\n') or (line == 'END'):
                                recipe_name_flag = True

                # Make buttons for all the recipes
                self.size_hint = 1, 0.3
                self.rows = int(np.ceil(np.sqrt(len(recipe_list))))
                self.cols = int(np.floor(np.sqrt(len(recipe_list))))
                for recipe in recipe_list:
                        item = Button(text=recipe, font_size='14sp')
                        self.add_widget(item)    	

class ShoppingArea(BoxLayout):
	def __init__(self, **kwargs):
		super(ShoppingArea,self).__init__(**kwargs)

		dropdown = DropDown()
		self.text_to_file = {}
		self.map_file = ''
		for index, file in enumerate(glob.glob("*.txt")):

			with open(file, 'r') as f:
				first_line = f.readline().strip()
				self.text_to_file[first_line] = file

			btn = Button(text=first_line, size_hint_y=None, height=60, background_color=[0, 0, 0.545098, 1])

			# for each button, attach a callback that will call the select() method
    		# on the dropdown. We'll pass the text of the button as the data of the
    		# selection.
			btn.bind(on_release=lambda btn: dropdown.select(btn.text))

			# then add the button inside the dropdown
			dropdown.add_widget(btn)

		# create a big main button
		mainbutton = Button(text='Choose shopping area', background_color=[0, 0, 0.545098, 1])

		# show the dropdown menu when the main button is released
		# note: all the bind() calls pass the instance of the caller (here, the
		# mainbutton instance) as the first argument of the callback (here,
		# dropdown.open.).
		mainbutton.bind(on_release=dropdown.open)

		# one last thing, listen for the selection in the dropdown list and
		# assign the data to the button text.
		dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
		dropdown.bind(on_select=lambda instance, x: setattr(self, 'map_file', self.text_to_file[x]))
		self.add_widget(mainbutton)

class PlannerApp(App):
        def build(self):
                self.title = 'Grocery Planner'
                return Planner()

if __name__ == '__main__':
        PlannerApp().run()