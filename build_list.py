# Build shopping list from selected recipes
# June 25, 2017
# Tim MacDonald


def build_list(selected_items):
    recipes = get_recipes()
    ingredients = sum_ingredients(recipes,selected_items)
    write_shopping_list(ingredients)
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
        elif (line == '\n') or (line == 'END'):
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

def write_shopping_list(ingredients):
    f = open('shopping_list.txt','w')
    for item in ingredients:
        f.write(str(item[0]) + ' ' + item[1] + ' ' + item[2] + '\n')
    f.close()
    return

if __name__ == '__main__':
    selected_items = dict()
    #selected_items['Chocolate Chip Cookies'] = 1
    #selected_items['Artichoke Cheese Dip']   = 2
    #selected_items['bananas']                = 5
    
    #selected_items['Pizza Potato'] = 1
    #selected_items['Bacon Ranch Chicken Bake'] = 1
    #selected_items['frozen broccoli'] = 1
    #selected_items['banana'] = 6
    #selected_items['keifer'] = 1
    #selected_items['snack bar'] = 4
    #selected_items['bread'] = 1
    #selected_items['trash bags'] = 1
    #selected_items['shampoo'] = 1
    #selected_items['sausage'] = 1
    #selected_items['peanut butter'] = 1  
    
    selected_items['Cream Cheese Bagel'] = 3
    selected_items['Lunch Sandwich'] = 3
    selected_items['frozen broccoli'] = 1
    selected_items['Lunch Celery'] = 3
    selected_items['banana'] = 5
    selected_items['meatballs'] = 1
    selected_items['Basic Dinner Rice'] = 2
    selected_items['Basic Dinner Pasta'] = 1
    selected_items['Peanut Butter Toast'] = 3
    selected_items['chips'] = 1
    selected_items['cheddar cheese'] = 1
    selected_items['grapes'] = 1
    selected_items['Pesto Chicken Bake'] = 1
    selected_items['yogurt'] = 4
    selected_items['Basic Eggs'] = 2
    selected_items['sausage'] = 1
    selected_items['crackers'] = 1
    
    
    build_list(selected_items)
    
    #1. -- bread
    #2. -- potatoes
    #2.24 cup cheese
    #5. -- snapea crisps
    #8. -- bananas
    #1. -- peanut butter
    #5.3 oz eggs    
    
    pass