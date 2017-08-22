#!/usr/bin/env python

# Safeway shopping route planner
# May 6, 2017
# Tiffany Huang
from __future__ import print_function
import math


# Number of aisles total
num_aisles = 300

# Create mapping between items and which aisle they are in from text file.
mapping = {}

main_store_list = 'aisle_map_mv.txt'

with open("aisle_mapping.txt") as f:
    for line in f.read().splitlines():
        (key, val) = line.split(",")
        mapping[key] = float(val)

# Read in the shopping list
input = open('shopping_list.txt', 'r')
items = input.read().splitlines()

# Route is list of lists, where each list contains all items in the same aisle
route = [[] for i in range(num_aisles + 2)]
for item in items:
    item_data = item.split()
    item_num  = item_data[0]
    item_unit = item_data[1]
    item_name = ' '.join(item_data[2:])
    if (item_name in mapping.keys()):
        aisle = int(math.floor(mapping[item_name]))
        route[aisle].append((item_name, mapping[item_name], item_num, item_unit))
    else:
        route[num_aisles + 1].append((item_name, num_aisles + 1, item_num, item_unit))

# Create the route
# Remove aisles with no items
route = [x for x in route if x]
# Sort items in aisle
for aisle in route:
    aisle.sort(key=lambda tup: tup[1])

if (route):
    # Flag for which side of the aisle you start from (0 - bottom of aisle near entrance to Safeway,
    # 1 - top of aisle far from entrance to Safeway)
    starting_point = 0
    for idx, aisle in enumerate(route):
        curr_aisle = int(math.floor(aisle[0][1]))
        # Print out items in the aisle
        aisle_name = str(curr_aisle)
        if (curr_aisle == 100):
            aisle_name = "Produce"
        elif (curr_aisle == 200):
            aisle_name = "Meat"
        elif (curr_aisle == num_aisles + 1):
            aisle_name = "Unknown"
        print(aisle_name + " : ", end="")
        for item in aisle:
            print(item[0] + ' (' + item[2] + ' ' + item[3] + ')')

        # Determine if you need to go all the way through the aisle or back the way you came.
        if (idx != len(route) - 1):
            last_item_place = aisle[-1][1]
            next_aisle = int(math.floor(route[idx+1][0][1]))
            # Find the shortest distance to the next item in the next aisle
            first_dist = (last_item_place - curr_aisle) + (route[idx+1][0][1] - next_aisle) # Distance to item near bottom of aisle
            second_dist = (curr_aisle + 1 - last_item_place) + (next_aisle + 1 - route[idx+1][-1][1]) # Distance to item near top of aisle
            if ((first_dist < second_dist and not starting_point) or
                (second_dist < first_dist and starting_point)):
                print('Go back the way you came through the aisle')
            else:
                starting_point = not starting_point

            # If you're starting from the top of the aisle, reverse the sorting of the next aisle.
            if (starting_point):
                route[idx+1].reverse()
else:
    print("No items in your shopping list!")


