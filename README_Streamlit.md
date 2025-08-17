# Grocery Planner - Streamlit Version

This is a Streamlit conversion of the original Kivy-based grocery planning application. The app allows you to plan weekly meals and generate optimized shopping routes.

## Features

- **Weekly Meal Planner**: Plan meals for each day of the week (4 meals per day)
- **Recipe Library**: Browse and search through available recipes
- **Shopping List Generation**: Automatically generate shopping lists from meal plans
- **Route Optimization**: Generate optimized shopping routes based on store layouts
- **Save/Load Functionality**: Save and load meal plans to/from files

## Installation

1. **Ensure you have the required data files**:
   - `recipes.txt` - Contains recipe definitions
   - `*.map` files - Store layout files for route optimization
   - `aisle_mapping.txt` - Item to aisle mappings

## Running the App

1. **Start the Streamlit app**:
   ```bash
   streamlit run streamlit_planner.py
   ```

2. **Open your browser** and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## How to Use

### Planning Meals
1. Use the meal grid to plan your weekly meals.
2. Click on any meal button above the meal box to add recipes or ingredients.
3. Use the recipe library on the right to quickly add recipes.
4. Search for specific recipes using the search box.

### Generating Shopping Lists
1. Plan your meals for the week.
2. Use the "Generate Shopping Route" button in the sidebar to create an optimized shopping route.

### Saving and Loading
1. Use the sidebar controls to save your meal plan to a file.
2. Load previously saved meal plans using the load function.
3. Files are saved in JSON format for easy parsing.

### Store Selection
1. Place your store map files (`.map` extension) in the same directory.
2. Select your preferred store from the dropdown in the sidebar.
3. Generate optimized shopping routes based on the store layout.

## File Structure

- `streamlit_planner.py` - Main Streamlit application.
- `build_list.py` - Shopping list generation logic.
- `safeway.py` - Route optimization logic.
- `units.py` - Unit conversion utilities.
- `recipes.txt` - Recipe database.
- `*.map` - Store layout files.
- `requirements.txt` - Python dependencies.

## Differences from Kivy Version

- **Web-based interface** instead of desktop application.
- **Responsive design** that works on different screen sizes.
- **Improved recipe search** with real-time filtering.
- **Better file management** with clear save/load controls.
- **Enhanced shopping list display** with better formatting.

## Troubleshooting

- **Missing files**: Ensure all required data files are in the same directory as the app.
- **Port conflicts**: If port 8501 is busy, Streamlit will automatically use the next available port.
- **Recipe loading**: If recipes don't load, check that `recipes.txt` exists and is properly formatted.

## Contributing

Feel free to submit issues and enhancement requests! 