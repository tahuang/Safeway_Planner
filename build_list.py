# Build shopping list from selected recipes
# May 6, 2017
# Tiffany Huang


def build_list(selected_items):
    recipes = get_recipes()
    ingredients = sum_ingredients(recipes,selected_items)
    return

def get_recipes():
    f = open('recipes.txt')
    recipe_name_flag = True
    recipes = dict()
    for line in f:
        if recipe_name_flag == True:
            ingredients_list = []
            recipe_name = line.rstrip('\n')
            recipe_name_flag = False
            continue
        if (line == '\n') or (line == 'END'):
            recipe_name_flag = True
            if recipes.has_key(recipe_name):
                raise ValueError('Duplicate recipes')
            recipes[recipe_name] = ingredients_list
        else:
            ingredients = line.split()
            ingredients = (float(ingredients[0]),ingredients[1],' '.join(ingredients[2:]))
            ingredients_list.append(ingredients)
    return recipes

def sum_ingredients(recipes,selected_items):
    full_list = []
    for item in selected_items:
        num = selected_items[item]
        if recipes.has_key(item):
            for ingredient in recipes[item]:
                total_ingredient = (ingredient[0]*num,ingredient[1],ingredient[2])
                full_list.append(total_ingredient)
        else:
            full_list.append((1.*num,'--',item))
    
    condensed_list = []
    for ingredient in full_list:
        dup_flag = False
        unit = ingredient[1]
        name = ingredient[2]
        total_units = 0.
        for line in condensed_list:
            if (line[1] == unit) and (line[2] == name):
                dup_flag = True
        if dup_flag == False:
            for line in full_list:
                if (line[1] == unit) and (line[2] == name):
                    total_units += line[0]
            condensed_list.append((total_units,unit,name))
    
    return condensed_list

if __name__ == '__main__':
    selected_items = dict()
    selected_items['Chocolate Chip Cookies'] = 1
    selected_items['Artichoke Cheese Dip']   = 2
    selected_items['bananas']                = 5
    
    build_list(selected_items)
    
    pass