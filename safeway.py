#!/usr/bin/env python

# Safeway shopping route planner
# May 6, 2017
# Tiffany Huang

import math

# Number of aisles total
num_aisles = 20

# Create mapping between items and which aisle they are in from text file.
mapping = {}
with open("aisle_mapping.txt") as f:
    for line in f.read().splitlines():
        (key, val) = line.split(",")
        mapping[key] = float(val)

# Read in the shopping list
input = open('shopping_list.txt', 'r')
items = input.read().splitlines()

route = []
for item in items:
    item_data = item.split()
    item_num  = item_data[0]
    item_unit = item_data[1]
    item_name = ' '.join(item_data[2:])
    if (item_name in mapping.keys()):
	    route.append((item_name, mapping[item_name], item_num, item_unit))
    else:
	    route.append((item_name, num_aisles + 1, item_num, item_unit))

# Create the route
route.sort(key=lambda tup: tup[1])

# Output the route
for idx, i in enumerate(route):
	aisle_name = int(math.floor(i[1]))
	if (i[1] == num_aisles + 1):
		aisle_name = "Unknown"
	elif (i[1] == 0):
		aisle_name = "Produce"
	elif (i[1] == 2.5):
		aisle_name = "Meat"
	print str(aisle_name) + " : " + i[0] + ' (' + i[2] + ' ' + i[3] + ')'

	# Determine if you go all the way through the aisle or go back down
	# for the next item.
	if (idx != len(route) - 1):
		next_aisle = route[idx+1][1]
		# There's no going back through meat aisle
		if (aisle_name != "Meat" and next_aisle % 1 == 0 and 
			math.floor(i[1]) != math.floor(next_aisle) and next_aisle != num_aisles + 1):
			print "Go back down Aisle " + str(aisle_name)