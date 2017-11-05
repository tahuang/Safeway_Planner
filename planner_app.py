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

import numpy as np
import build_list
import safeway

# Builder used to load all the kivy files
Builder.load_file('days.kv')

class Planner(BoxLayout):
        def __init__(self,**kwargs):
                super(Planner,self).__init__(**kwargs)

class GetRouteButton(Button):
        meals = ObjectProperty()

        # Reads text input from user and creates grocery route.
        def getGroceryRoute(self, meal_list):
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
                safeway.print_shopping_route()

        def __init__(self,**kwargs):
                super(GetRouteButton,self).__init__(**kwargs)
                self.background_normal = ''
                self.background_color = [0.698039, 0.133333, 0.133333, 1]

class Meals(GridLayout):
        def __init__(self, **kwargs):
                super(Meals,self).__init__(**kwargs)
                self.active_box = None
                self.meal_list = []
                self.rows = 4
                self.cols = 7
                for row in range(self.rows):
                        for column in range(self.cols):
                                meal_entry = TextInput()
                                meal_entry.bind(focus=self.set_meal_target)
                                self.meal_list.append(meal_entry)
                                self.add_widget(meal_entry)
                                
        def set_meal_target(self,instance,value):
                self.active_box = instance

class Recipes(GridLayout):
        meals = ObjectProperty()
        
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
                        item.bind(on_press=self.add_recipe)
                        self.add_widget(item)    
                        
        def add_recipe(self,instance):
                print(active_box)
                print('Button pressed')

class PlannerApp(App):
        def build(self):
                self.title = 'Grocery Planner'
                return Planner()

if __name__ == '__main__':
        PlannerApp().run()