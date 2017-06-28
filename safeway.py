#!/usr/bin/env python

# Safeway shopping route planner
# May 6, 2017
# Tiffany Huang

import math

# Number of aisles total
num_aisles = 300

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

# Keep track of items in the same aisle
last_item = route[0]
last_aisle = int(math.floor(last_item[1]))
next_aisle = [last_item]
idx = 1
print(str(int(math.floor(last_item[1]))) + " : " + last_item[0] + ' (' + last_item[2] + ' ' + last_item[3] + ')')

# Output the route
while (idx != len(route) - 1):
	i = route[idx]
	curr_aisle = int(math.floor(i[1]))
	# Determine if you go all the way through the aisle or go back the way you came.
	if (curr_aisle == last_aisle and last_aisle == int(math.floor(route[0][1]))):
		next_aisle.append(i)
		print(i[0] + ' (' + i[2] + ' ' + i[3] + ')')
		idx += 1
	else:
		last_item = next_aisle[-1]
		last_aisle = int(math.floor(last_item[1]))
		next_aisle.clear()
		aisle_name = str(curr_aisle)
		if (i[1] == num_aisles + 1):
			aisle_name = "Unknown"
		elif (i[1] == 100):
			aisle_name = "Produce"
		elif (i[1] == 200):
			aisle_name = "Meat"
		print(aisle_name + " : ")
		next_item = i
		while (math.floor(next_item[1]) == curr_aisle):
			if (idx != len(route) - 1):
				next_aisle.append(i)
				next_item = route[idx+1]
				idx += 1
			else:
				break

		first_dist = (last_item[1] - last_aisle) + (next_aisle[0][1] - curr_aisle)
		second_dist = (last_item[1] - last_aisle) + (next_aisle[-1][1] - curr_aisle)
		if ((first_dist < second_dist and last_item[1] - last_aisle < 0.5) or
			second_dist < first_dist and last_item[1] - last_item >= 0.5):
			print('Go back the way you came through aisle ' + str(curr_aisle))
		if (second_dist < first_dist):
			next_aisle.reverse()
		for item in next_aisle:
			print(item[0] + ' (' + item[2] + ' ' + item[3] + ')')
		