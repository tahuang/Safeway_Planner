# Build shopping list from selected recipes
# June 25, 2017
# Tim MacDonald


def build_list(selected_items):
    recipes = get_recipes()
    ingredients = sum_ingredients(recipes, selected_items)
    write_shopping_list(ingredients)
    return


def get_recipes():
    """Open the catalogue of receipes and parse all the ingredients."""
    f = open("recipes.txt")
    recipe_name_flag = True
    recipes = dict()
    for line in f:
        if recipe_name_flag == True:
            ingredients_list = []
            recipe_name = line.rstrip("\n")
            recipe_name_flag = False
        elif (line == "\n") or (line == "END"):
            recipe_name_flag = True
            if recipe_name in recipes:
                raise ValueError("Duplicate recipes")
            recipes[recipe_name] = ingredients_list
        else:
            if line[0] == "#":
                continue
            ingredients = line.split()
            ingredients = (
                float(ingredients[0]),
                ingredients[1],
                " ".join(ingredients[2:]),
            )
            ingredients_list.append(ingredients)
    return recipes


def sum_ingredients(recipes, selected_items):
    """Find the ingredients given the selected recipes and items."""
    full_list = []
    for item, num in selected_items.items():
        # If the item is a recipe, gather the ingredients from the recipe.
        if item in recipes:
            for ingredient in recipes[item]:
                total_ingredient = (ingredient[0] * num, ingredient[1], ingredient[2])
                full_list.append(total_ingredient)
        else:
            # If the item is capitalized, it was intended to have a recipe and none was found.
            if item[0].isupper() == True:
                print("No recipe found for " + item)
            # Otherwise, the item is just an ingredient and we add it to the list.
            full_list.append((1.0 * num, "--", item))

    # Condensed list will be a dictionary with keys being the ingredients
    # and values being another dictionary that has keys of units and values
    # of amount of a particular unit. This will help us consolidate ingredients
    # even if different types of units are used in different recipes.
    condensed_list = {}
    for amount, unit, name in full_list:
        # If the ingredient is already in the condensed list, update
        # the ingredient.
        if name in condensed_list:
            if unit in condensed_list[name]:
                condensed_list[name][unit] += amount
            else:
                condensed_list[name][unit] = amount
        else:
            condensed_list[name] = {unit: amount}

    return condensed_list


def write_shopping_list(ingredients: dict[str, dict[str, float]]) -> None:
    f = open("shopping_list.txt", "w")
    for item in ingredients:
        unit_str = (
            "("
            + ", ".join(
                str(amount) + " " + unit for unit, amount in ingredients[item].items()
            )
            + ")"
        )
        f.write(unit_str + " " + item + "\n")
    f.close()
    return


if __name__ == "__main__":
    """For testing this file only."""
    selected_items = dict()
    s = selected_items

    s["banana"] = 4
    s["Simple Sandwich"] = 3
    s["yogurt"] = 3
    s["sausage"] = 1
    s["frozen broccoli"] = 1
    s["cheddar cheese"] = 1
    s["Peanut Butter Toast"] = 2
    s["Cream Cheese Bagel"] = 4
    s["Pizza Potatoes"] = 1
    s["Chocolate Chip Cookies"] = 1

    build_list(s)

    pass
