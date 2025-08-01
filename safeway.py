#!/usr/bin/env python

# Safeway shopping route planner
# May 6, 2017
# Tiffany Huang
from __future__ import print_function
import math
import io
import sys


def print_shopping_route(map_file):
    full_mapping = create_item_aisle_mapping(map_file)
    items = read_shopping_list()
    create_full_route(full_mapping, items)
    return


def get_shopping_route_string(map_file):
    """Returns the shopping route as a string instead of printing to console."""
    # Capture stdout to get the output as a string
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    full_mapping = create_item_aisle_mapping(map_file)
    items = read_shopping_list()
    create_full_route(full_mapping, items)
    output = new_stdout.getvalue()
    return output


# Create mapping between items and which aisle they are in from text file.
def create_item_aisle_mapping(shopping_map):
    full_mapping = {}

    if shopping_map == "":
        shopping_map = "irvine.map"
        print("No file specified, using default")

    with open(shopping_map) as f:
        print("---- " + f.readline()[:-1] + " ----\n")
        store = "None"

        for line in f.read().splitlines():
            if (line == "") or (line[0] == "#"):
                continue
            elif line[0] == "@":
                store = line[1:]
                full_mapping[store] = {}
            else:
                (key, val) = line.split(",")
                full_mapping[store][key] = float(val)

    return full_mapping


# Read in the shopping list
def read_shopping_list():
    input = open("shopping_list.txt", "r")
    items = input.read().splitlines()
    return items


def create_full_route(full_mapping, items):
    # first check for unmapped items.
    unknown_items = []
    for item in items:
        # The string format is "(amount unit) name".
        item_label = item[item.index(")") + 2 :]
        item_found = False
        for store in full_mapping:
            if item_label in full_mapping[store]:
                item_found = True
        if item_found == False:
            unknown_items.append(item)

    # map known items
    for store in full_mapping:
        print("---- Shopping at " + store)
        store_mapping = full_mapping[store]
        store_items = []
        for item in items:
            item_label = item[item.index(")") + 2 :]
            if item_label in store_mapping:
                store_items.append(item)
        route = create_store_route(store_mapping, store_items)
        # create_map_diagram(route)
        print_store_route(route)
        print("")  # effectively a new line

    if unknown_items != []:
        print("---- Unknown Location")
        route = create_store_route({}, unknown_items)
        print_store_route(route)


# Route is list of lists, where each list contains all items in the same aisle
def create_store_route(store_mapping, items):
    # Number of aisles total
    num_aisles = 300
    route = [[] for i in range(num_aisles + 2)]
    for item in items:
        # The string format is "(amount unit, amount unit...) name".
        unit_str = item[item.index("(") + 1 : item.index(")")]
        item_name = item[item.index(")") + 2 :]
        if item_name in store_mapping.keys():
            aisle = int(math.floor(store_mapping[item_name]))
            route[aisle].append((item_name, store_mapping[item_name], unit_str))
        else:
            route[num_aisles + 1].append((item_name, num_aisles + 1, unit_str))

    # Create the route
    # Remove aisles with no items
    route = [x for x in route if x]
    # Sort items in aisle
    for aisle in route:
        aisle.sort(key=lambda tup: tup[1])
    return route


def print_store_route(route):
    if route:
        # Flag for which side of the aisle you start from (0 - bottom of aisle near entrance to Safeway,
        # 1 - top of aisle far from entrance to Safeway)
        starting_point = 0
        for idx, aisle in enumerate(route):
            curr_aisle = int(math.floor(aisle[0][1]))
            # Print out items in the aisle
            aisle_name = str(curr_aisle)
            if curr_aisle == 100:
                aisle_name = "Produce"
            elif curr_aisle == 200:
                aisle_name = "Meat"
            elif curr_aisle == 301:
                aisle_name = "Unknown"
            print(aisle_name + " : ", end="")
            for item in aisle:
                print(item[0] + " (" + item[2] + ")")

            # Determine if you need to go all the way through the aisle or back the way you came.
            continue
            # TODO: see if we want to keep this
            if idx != len(route) - 1:
                last_item_place = aisle[-1][1]
                next_aisle = int(math.floor(route[idx + 1][0][1]))
                # Find the shortest distance to the next item in the next aisle
                first_dist = (last_item_place - curr_aisle) + (
                    route[idx + 1][0][1] - next_aisle
                )  # Distance to item near bottom of aisle
                second_dist = (curr_aisle + 1 - last_item_place) + (
                    next_aisle + 1 - route[idx + 1][-1][1]
                )  # Distance to item near top of aisle
                if (first_dist < second_dist and not starting_point) or (
                    second_dist < first_dist and starting_point
                ):
                    print("-- Go back the way you came through the aisle")
                else:
                    starting_point = not starting_point

                # If you're starting from the top of the aisle, reverse the sorting of the next aisle.
                if starting_point:
                    route[idx + 1].reverse()
    else:
        print("No items for this location.")


if __name__ == "__main__":
    print_shopping_route("mp_center.map")

    pass
