#!/usr/bin/env python

# Safeway shopping route planner
# May 6, 2017
# Tiffany Huang

num_aisles = 20
mapping = {'bread' : 7, 'peanut butter' : 4, 'potatoes' : 0, 
'cheese' : 1, 'bananas' : 0}

input = open('shopping_list.txt', 'r')
items = input.read().splitlines()

route = []
for i in items:
	if (i in mapping.keys()):
		route.append((i, mapping[i]))
	else:
		route.append((i, num_aisles + 1))

route.sort(key=lambda tup: tup[1])

for i in route:
	if (i[1] == num_aisles + 1):
		print("Unknown:"),
		print(i[0])
	else:
		print(i[1]),
		print(":"),
		print(i[0])