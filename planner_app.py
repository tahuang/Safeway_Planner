#!/usr/bin/env python

# Grocery planning app
# June 25, 2017
# Tiffany Huang

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

import numpy as np
import glob

import build_list
import safeway

# Builder used to load all the kivy files
Builder.load_file('days.kv')


class Planner(BoxLayout):
    def __init__(self, **kwargs):
        super(Planner, self).__init__(**kwargs)


class GetRouteButton(Button):
    meals = ObjectProperty()
    shopping_area = ObjectProperty()

    # Reads text input from user and creates grocery route.
    def getGroceryRoute(self, meal_list, map_file):
        items = dict()
        # Parse each meal block for different items
        for meal in meal_list:
            if meal[0].text == '':
                continue
            meal_parts = meal[0].text.split('\n')
            for part in meal_parts:
                if (part == '') or (part[0] == '!'):
                    continue
                if part in items:
                    items[part] += 1
                else:
                    items[part] = 1

        build_list.build_list(items)
        safeway.print_shopping_route(map_file)

    def __init__(self, **kwargs):
        super(GetRouteButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.698039, 0.133333, 0.133333, 1]


class SaveButton(Button):
    meals = ObjectProperty()

    def save(self, meal_list, filename):
        save_file = open(filename, "w")
        for meal_entry in meal_list:
            if meal_entry[0].text == '':
                continue
            meals = meal_entry[0].text.split('\n')
            for idx, item in enumerate(meals):
                save_file.write(item)
                if idx == 0:
                    row_column = " " + str(meal_entry[1]) + "\n"
                else:
                    row_column = "\n"
                save_file.write(row_column)
        save_file.close()

    def __init__(self, **kwargs):
        super(SaveButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [0.6, 0.196078, 0.8, 1]


class LoadButton(Button):
    meals = ObjectProperty()

    # Loads meals from file and puts them into the GUI
    def load(self, meal_list, filename):
        load_file = open(filename, "r")
        box_index = 0
        for line in load_file:
            meal = line.strip('\n')
            if meal == '':
                continue
            if meal[-1].isdigit():
                # Get the box index from the first item in the box
                box_index = int(line.split()[-1])
                meal_list[box_index][0].select_all()
                meal_list[box_index][0].delete_selection()
                meal_list[box_index][0].insert_text(meal[:-2] + "\n")
            else:
                meal_list[box_index][0].insert_text(meal + "\n")
        load_file.close()

    def __init__(self, **kwargs):
        super(LoadButton, self).__init__(**kwargs)
        self.background_normal = ''
        self.background_color = [1, 0.647059, 0, 1]


class FileNamePopup(Popup):
    def __init__(self, **kwargs):
        self.content = BoxLayout(orientation="vertical")
        self.ok_button = Button(text='OK')
        self.textinput = TextInput()
        self.content.add_widget(self.textinput)
        self.content.add_widget(self.ok_button)


class MyTextInput(TextInput):
    def __init__(self, recipes, **kwargs):
        super(MyTextInput, self).__init__(**kwargs)
        self.recipes = recipes

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """ Add support for tab as an 'autocomplete' using the suggestion text.
        """
        if self.suggestion_text and keycode[1] == 'tab':
            self.insert_text(self.suggestion_text)
            return True
        return super(MyTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

    def on_text(self, instance, value):
        self.suggestion_text = ''
        val = value[value.rfind('\n') + 1:]
        if not val:
            return
        try:
            word = [word for word in self.recipes if word.startswith(
                val)][0][len(val):]
            if not word:
                return
            self.suggestion_text = word
        except IndexError:
            return

    def on_touch_down(self, touch):
        self.parent.active_box = self
        return super(MyTextInput, self).on_touch_down(touch)


class Meals(GridLayout):
    def __init__(self, **kwargs):
        super(Meals, self).__init__(**kwargs)
        self.active_box = TextInput()
        self.meal_list = []
        self.rows = 4
        self.cols = 7
        self.recipe_list = []

        # Get all the recipe names from file
        recipe_file = open('recipes.txt')
        recipe_name_flag = True
        for line in recipe_file:
            if recipe_name_flag == True:
                recipe_name = line.rstrip('\n')
                self.recipe_list.append(recipe_name)
                recipe_name_flag = False
            elif (line == '\n') or (line == 'END'):
                recipe_name_flag = True

        self.recipe_list.sort()

        for row in range(self.rows):
            for column in range(self.cols):
                meal_entry = MyTextInput(self.recipe_list)
                self.meal_list.append((meal_entry, row*self.cols + column))
                self.add_widget(meal_entry)


class Recipes(GridLayout):
    def __init__(self, **kwargs):
        super(Recipes, self).__init__(**kwargs)
        self.meals = Meals()

        # Make buttons for all the recipes
        num_col = 4
        self.rows = int(np.ceil(len(self.meals.recipe_list)/float(num_col)))
        self.cols = num_col
        # for some reason this removes the need to double click on the shopping list boxes
        self.minimum_height = 1000
        for recipe in self.meals.recipe_list:
            item = Button(text=recipe, font_size='14sp',
                          size_hint_y=None, height=40)
            item.bind(on_press=self.add_recipe)
            self.add_widget(item)

    def add_recipe(self, instance):
        '''When you click a recipe button, populate the text box where the cursor was last.'''
        if self.meals.active_box is None:
            return
        self.meals.active_box.insert_text(instance.text + "\n")


class ShoppingArea(Spinner):
    def __init__(self, **kwargs):
        super(ShoppingArea, self).__init__(**kwargs)

        self.text_to_file = {}
        self.map_file = ''
        self.text = 'Choose shopping area'
        self.background_color = [0, 0, 0.545098, 1]
        for index, file in enumerate(glob.glob("*.map")):

            with open(file, 'r') as f:
                first_line = f.readline().strip()
                self.text_to_file[first_line] = file

            self.values.append(first_line)


class PlannerApp(App):
    def build(self):
        self.title = 'Grocery Planner'
        return Planner()


if __name__ == '__main__':
    PlannerApp().run()
