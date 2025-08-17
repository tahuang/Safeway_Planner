#!/usr/bin/env python

# Grocery planning app - Streamlit version.
# Converted from Kivy app.
# Original: June 25, 2017 by Tiffany Huang

import streamlit as st
import glob
from typing import Dict, List
import build_list
import safeway
import json

# Page configuration.
st.set_page_config(
    page_title="Grocery Planner",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for better styling.
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .meal-grid {
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .recipe-button {
        margin: 0.1rem;
        font-size: 0.9rem;
        padding: 0.3rem 0.5rem;
    }
    .recipe-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.5rem;
        margin: 0.5rem 0;
    }
    .category-button {
        background-color: #f0f8ff;
        border: 1px solid #1f77b4;
        border-radius: 0.3rem;
        padding: 0.3rem 0.5rem;
        margin: 0.2rem;
        font-size: 0.8rem;
    }
    .shopping-list {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .route-output {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        font-family: monospace;
    }
</style>
""",
    unsafe_allow_html=True,
)


class StreamlitGroceryPlanner:
    def __init__(self):
        self.recipe_list = self.load_recipes()
        self.days = [
            "Sunday",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
        ]
        self.meals_per_day = 4
        self.shopping_route = ""

        # Initialize meal plan in session state if not exists.
        if "meal_plan" not in st.session_state:
            st.session_state.meal_plan = self.initialize_meal_plan()

        if "misc_items" not in st.session_state:
            st.session_state.misc_items = ""

        # Add a version counter for the misc items box to force widget refresh on load
        if "misc_items_box_version" not in st.session_state:
            st.session_state.misc_items_box_version = 0
        # Add a version counter for the meal boxes to force widget refresh on load
        if "meal_box_version" not in st.session_state:
            st.session_state.meal_box_version = 0

    def load_recipes(self) -> List[str]:
        """Load recipe names from recipes.txt file."""
        recipe_list = []
        try:
            with open("recipes.txt", "r") as recipe_file:
                # The next line after a newline is a recipe name.
                recipe_name_flag = True
                for line in recipe_file:
                    if recipe_name_flag == True:
                        line = line.strip()
                        recipe_list.append(line)
                        recipe_name_flag = False
                    elif line == "\n":
                        recipe_name_flag = True
            # Sort the recipe list alphabetically.
            recipe_list.sort()
        except FileNotFoundError:
            st.error("recipes.txt file not found!")
            return []
        return recipe_list

    def get_recipe_ingredients(self, recipe_name: str) -> List[str]:
        """Get ingredients for a specific recipe."""
        ingredients = []
        try:
            with open("recipes.txt", "r") as recipe_file:
                lines = recipe_file.readlines()
                in_recipe = False
                for line in lines:
                    line = line.strip()
                    if line == recipe_name:
                        in_recipe = True
                        continue
                    elif in_recipe:
                        if not line:  # Empty line marks end of recipe.
                            break
                        elif line.startswith("#"):  # Skip comments.
                            continue
                        elif line == "END":  # Skip END marker.
                            break
                        # Otherwise this is an ingredient line.
                        ingredients.append(line)
        except FileNotFoundError:
            st.error("recipes.txt file not found!")
        return ingredients

    def initialize_meal_plan(self) -> Dict[str, List[str]]:
        """Initialize empty meal plan structure."""
        meal_plan = {}
        for day in self.days:
            meal_plan[day] = [""] * self.meals_per_day
        return meal_plan

    def load_meal_plan_from_file(self, filename: str) -> Dict[str, List[str]]:
        try:
            with open(filename, "r") as load_file:
                data = json.load(load_file)
                meal_plan = data.get("meal_plan", self.initialize_meal_plan())
                misc_items = data.get("misc_items", "")
                # Ensure all days and meals are present
                for day in self.days:
                    if day not in meal_plan:
                        meal_plan[day] = [""] * self.meals_per_day
                    else:
                        # Pad or trim to correct number of meals
                        meal_plan[day] = (meal_plan[day] + [""] * self.meals_per_day)[
                            : self.meals_per_day
                        ]
                st.session_state.misc_items = misc_items
                return meal_plan
        except json.JSONDecodeError:
            st.error(
                f"File {filename} is not a valid meal plan file (JSON expected). Please save a new meal plan."
            )
            return self.initialize_meal_plan()
        except FileNotFoundError:
            st.error(f"File {filename} not found!")
            return self.initialize_meal_plan()
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return self.initialize_meal_plan()

    def save_meal_plan_to_file(self, filename: str):
        """Save meal plan to file as JSON."""
        data = {
            "meal_plan": st.session_state.meal_plan,
            "misc_items": st.session_state.misc_items,
        }
        try:
            with open(filename, "w") as save_file:
                json.dump(data, save_file, indent=2)
            st.success(f"Meal plan saved to {filename}")
        except Exception as e:
            st.error(f"Error saving file: {e}")

    def get_grocery_items(self, meal_plan: Dict[str, List[str]]) -> Dict[str, int]:
        """Extract grocery items from meal plan."""
        items = {}
        for day in self.days:
            for meal in meal_plan[day]:
                if meal.strip():
                    meal_parts = meal.split("\n")
                    for part in meal_parts:
                        part = part.strip()
                        # Ignore empty items anditems that start with !.
                        if (part == "") or (part[0] == "!"):
                            continue

                        if part in items:
                            items[part] += 1
                        else:
                            items[part] = 1
        return items

    def get_available_map_files(self) -> Dict[str, str]:
        """Get available store map files."""
        text_to_file = {}
        for file in glob.glob("*.map"):
            try:
                with open(file, "r") as f:
                    first_line = f.readline().strip()
                    text_to_file[first_line] = file
            except Exception as e:
                st.error(f"Error reading map file {file}: {e}")

        # Sort stores so "Shopping in Irvine" appears first
        sorted_stores = sorted(
            text_to_file.keys(), key=lambda x: ("Irvine" not in x, x)
        )
        return {store: text_to_file[store] for store in sorted_stores}

    def run(self):
        """Main application runner."""
        st.markdown(
            '<h1 class="main-header">🛒 Grocery Planner</h1>', unsafe_allow_html=True
        )

        # Sidebar for controls.
        with st.sidebar:
            # Shopping route generation.
            st.subheader("Shopping Route")
            map_files = self.get_available_map_files()
            if map_files:
                selected_store = st.selectbox("Select store:", list(map_files.keys()))
                if st.button("🗺️ Generate Shopping Route"):
                    # Generate shopping list first.
                    items = self.get_grocery_items(st.session_state.meal_plan)

                    # Incorporate miscellaneous items from the misc box, one per line.
                    misc = st.session_state.misc_items.strip()
                    if misc:
                        for misc_item in misc.splitlines():
                            misc_item = misc_item.strip()
                            if misc_item:
                                items[misc_item] = items.get(misc_item, 0) + 1

                    print(items)
                    build_list.build_list(items)

                    # Generate route.
                    self.shopping_route = safeway.get_shopping_route_string(
                        map_files[selected_store]
                    )
            else:
                st.warning("No store map files found (*.map)")

            st.divider()

            # --- File Upload (User -> App) ---
            uploaded_file = st.file_uploader(
                "📂 Upload Meal Plan File", type=["txt", "json"]
            )

            # Handle file upload processing
            if "upload_processed" not in st.session_state:
                st.session_state.upload_processed = False

            if uploaded_file is not None and not st.session_state.upload_processed:
                try:
                    file_content = uploaded_file.read()
                    # Try to decode as UTF-8 text.
                    file_text = file_content.decode("utf-8")
                    data = json.loads(file_text)
                    st.session_state.meal_plan = data.get(
                        "meal_plan", self.initialize_meal_plan()
                    )
                    st.session_state.misc_items = data.get("misc_items", "")

                    # Clear all meal slot and misc_items_box widget state so text areas update.
                    for day in self.days:
                        for meal_idx in range(self.meals_per_day):
                            key = f"{day}_{meal_idx}"
                            if key in st.session_state:
                                del st.session_state[key]

                    # Increment the version to force the widgets to refresh.
                    st.session_state.misc_items_box_version += 1
                    st.session_state.meal_box_version += 1

                    st.session_state.upload_processed = True
                    st.success("Meal plan loaded from uploaded file!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to load meal plan: {e}")
                    st.session_state.upload_processed = True

            # Reset upload processed flag when no file is selected
            if uploaded_file is None:
                st.session_state.upload_processed = False

        # Main content area.
        col1, col2 = st.columns([2, 1])

        with col1:
            st.header("📅 Weekly Meal Planner")

            # Create the meal grid using columns.
            for day in self.days:
                cols = st.columns([1] + [2] * self.meals_per_day)
                with cols[0]:
                    st.write(f"**{day}**")

                for meal_idx in range(self.meals_per_day):
                    with cols[meal_idx + 1]:
                        # Create a unique identifier for this meal slot.
                        meal_slot_id = f"{day}_{meal_idx}"

                        # Check if this meal slot is currently selected as target.
                        is_target = (
                            "target_meal_slot" in st.session_state
                            and st.session_state.target_meal_slot == meal_slot_id
                        )

                        # Create a clickable meal label button.
                        button_text = (
                            f"🍽️ Meal {meal_idx + 1}"
                            if is_target
                            else f"Meal {meal_idx + 1}"
                        )
                        button_type = "primary" if is_target else "secondary"

                        if st.button(
                            button_text,
                            key=f"meal_label_{meal_slot_id}",
                            type=button_type,
                            use_container_width=True,
                        ):
                            # If clicking the same meal that's already selected, deselect it.
                            if (
                                "target_meal_slot" in st.session_state
                                and st.session_state.target_meal_slot == meal_slot_id
                            ):
                                del st.session_state.target_meal_slot
                            else:
                                # Select the new meal slot.
                                st.session_state.target_meal_slot = meal_slot_id
                            st.rerun()

                        # Text area for meal input.
                        meal_box_key = (
                            f"{meal_slot_id}_{st.session_state.meal_box_version}"
                        )
                        new_value = st.text_area(
                            "Recipe/Ingredients",
                            value=st.session_state.meal_plan[day][meal_idx],
                            key=meal_box_key,
                            height=100,
                            placeholder="Click 'Meal X' above to select, then choose a recipe...",
                        )

                        # Update meal plan if changed.
                        if new_value != st.session_state.meal_plan[day][meal_idx]:
                            st.session_state.meal_plan[day][meal_idx] = new_value

            # Miscellaneous items box.
            st.header("🧺 Miscellaneous Items")
            misc_box_key = f"misc_items_box_{st.session_state.misc_items_box_version}"
            misc_box_value = st.text_area(
                "Enter snacks, household items, or anything else to add to your shopping list:",
                value=st.session_state.misc_items,
                key=misc_box_key,
                height=100,
                placeholder="e.g. toilet paper, snacks, cleaning supplies...",
            )
            if misc_box_value != st.session_state.misc_items:
                st.session_state.misc_items = misc_box_value

            # --- File Download (App -> User) ---
            st.divider()
            data = {
                "meal_plan": st.session_state.meal_plan,
                "misc_items": st.session_state.misc_items,
            }
            json_str = json.dumps(data, indent=2)
            st.download_button(
                label="💾 Download Meal Plan",
                data=json_str,
                file_name="meal_plan.txt",
                mime="application/json",
                use_container_width=True,
            )

        with col2:
            st.header("📋 Recipe Library")

            # Recipe search and display controls.
            search_term = st.text_input(
                "Search recipes", placeholder="Type to filter recipes..."
            )

            # Handle recipe filtering.
            filtered_recipes = [
                r for r in self.recipe_list if search_term.lower() in r.lower()
            ]

            # Pagination controls for large recipe lists.
            recipes_per_page = 30
            total_pages = (
                len(filtered_recipes) + recipes_per_page - 1
            ) // recipes_per_page

            # Initialize current page in session state if not exists.
            if "recipe_current_page" not in st.session_state:
                st.session_state.recipe_current_page = 1

            # Calculate start and end indices for current page.
            start_idx = (st.session_state.recipe_current_page - 1) * recipes_per_page
            end_idx = min(start_idx + recipes_per_page, len(filtered_recipes))
            current_recipes = filtered_recipes[start_idx:end_idx]

            # Display recipes in a compact multi-column layout.
            if current_recipes:
                # Use columns for compact display - 2 columns for better space usage.
                recipe_cols = st.columns(2)

                for idx, recipe in enumerate(current_recipes):
                    col_idx = idx % 2
                    with recipe_cols[col_idx]:
                        ingredients = self.get_recipe_ingredients(recipe)
                        if st.button(
                            recipe,
                            key=f"recipe_{recipe}_{idx}",
                            use_container_width=True,
                            help=" | ".join(ingredients),
                        ):
                            # Check if a meal slot is selected as target.
                            if "target_meal_slot" in st.session_state:
                                target_slot = st.session_state.target_meal_slot
                                day, meal_idx = target_slot.split("_")
                                meal_idx = int(meal_idx)

                                # Add the recipe to the selected meal slot (append if content exists).
                                current_content = st.session_state.meal_plan[day][
                                    meal_idx
                                ]
                                if current_content.strip():
                                    # If there's existing content, add the new recipe on a new line.
                                    new_content = current_content + "\n" + recipe
                                else:
                                    # If empty, just set the recipe.
                                    new_content = recipe

                                st.session_state.meal_plan[day][meal_idx] = new_content

                                # Don't clear the target selection - keep it selected for multiple recipes.
                                st.rerun()
                            else:
                                st.warning(
                                    "Please click a 'Meal X' button first, then choose a recipe."
                                )

            # Show pagination info if needed.
            if total_pages > 1:
                st.write("📄 Pages:")

                # Create clickable page numbers
                page_cols = st.columns(
                    min(total_pages, 10)
                )  # Max 10 columns to avoid overflow

                for page_num in range(1, total_pages + 1):
                    col_idx = (page_num - 1) % 10  # Wrap around if more than 10 pages

                    with page_cols[col_idx]:
                        # Style the current page differently
                        if page_num == st.session_state.recipe_current_page:
                            if st.button(
                                f"**{page_num}**",
                                key=f"page_{page_num}",
                                use_container_width=True,
                            ):
                                st.session_state.recipe_current_page = page_num
                                st.rerun()
                        else:
                            if st.button(
                                str(page_num),
                                key=f"page_{page_num}",
                                use_container_width=True,
                            ):
                                st.session_state.recipe_current_page = page_num
                                st.rerun()

                st.caption(
                    f"📄 Page {st.session_state.recipe_current_page} of {total_pages} • Recipes {start_idx + 1}-{end_idx} of {len(filtered_recipes)}"
                )

        # Shopping list section.
        st.header("🛒 Menu")

        # Generate shopping list.
        items = self.get_grocery_items(st.session_state.meal_plan)

        if items:
            # Display items in a nice format.
            for item in items.keys():
                st.write(f"• {item}")

            # Show shopping route if generated.
            if self.shopping_route:
                st.subheader("🗺️ Shopping Route:")
                st.text(self.shopping_route)
        else:
            st.info(
                "No items in meal plan yet. Add some meals to generate a shopping list!"
            )


def main():
    """Main function to run the Streamlit app."""
    planner = StreamlitGroceryPlanner()
    planner.run()


if __name__ == "__main__":
    main()
