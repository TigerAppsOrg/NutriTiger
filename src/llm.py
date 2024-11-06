from openai import OpenAI
import hashlib
import os

# Organizes data --> less info to send + figure out serving size
def parse_nutritional_info(query, api_response):
    # Initialize an empty list to store the parsed food data
    foods = []

    # 11.6.24 --> Let's allow for the same name to occur, distinguish based on ingredients
    unique_items = set()  # Set to track existing meal names to avoid duplicates
    
    # Loop through each food item in the response
    for food in api_response["foods"]:
        meal_name = food.get("description")

        formatted_serving_size = "100g" if None in (food.get('servingSize'), food.get('servingSizeUnit')) else f"{round(int(food.get('servingSize')))} {food.get('servingSizeUnit')}"

        # Initialize a dictionary to store the information for each food item
        food_info = {
            "recipeid": 'usda-' + str(food.get("fdcId")),
            "mealname": meal_name.title(),  # Use the description as meal name
            "servingSize": formatted_serving_size,  # Format the serving size
            "ingredients": food.get("ingredients", "No ingredients listed")  # Get ingredients if available
        }
        
        # Map nutrient names from the API to the desired keys
        nutrients_map = {
            "Energy": "calories",
            "Protein": "proteins",
            "Carbohydrate, by difference": "carbs",
            "Total lipid (fat)": "fats"
        }
        
        # Extract nutrient information
        for nutrient in food.get("foodNutrients", []):
            nutrient_name = nutrient.get("nutrientName")
            if nutrient_name in nutrients_map:
                # Map the nutrient value to the corresponding key in food_info
                food_info[nutrients_map[nutrient_name]] = round(int(nutrient.get("value")))
        
        # Check if mealName is already processed
        all_nutrition = (
            meal_name +
            str(food_info.get("calories", 0)) + 
            str(food_info.get("proteins", 0)) + 
            str(food_info.get("carbs", 0)) + 
            str(food_info.get("fats", 0))
        )
        if all_nutrition in unique_items:
            continue  # Skip parsing this food item if mealName is a duplicate
        
        # Add item to the set
        unique_items.add(all_nutrition)


        # Create a string from the specified data to hash
        data_str = (
            food_info["servingSize"] +
            food_info["mealname"] +
            food_info["recipeid"][5:] + 
            str(food_info.get("calories", 0)) + 
            str(food_info.get("proteins", 0)) + 
            str(food_info.get("carbs", 0)) + 
            str(food_info.get("fats", 0))
        )
        
        # Generate the SHA-256 hash
        sha256 = hashlib.sha256()
        sha256.update(data_str.encode('utf-8'))
        string_hash = sha256.hexdigest()
        
        # Add the hash to food_info
        food_info["signature"] = string_hash

        # Append the parsed food item to the list
        foods.append(food_info)
    
    # Return the list of parsed food items
    return foods

def filter_parsed_data(query, data):
    # Construct the prompt for GPT to parse rational items
    prompt = (
        f"Given a list of {query} items with nutritional information, "
        "filter and return only those that are rational based on the following criteria:\n\n"
        "- Macronutrient counts should be within reason.\n"
        "- Ingredients should be relevant to the item.\n\n"
        "Here is the list of items:\n\n"
        f"{data}\n\n"
        "Return only the rational items that fit the criteria, in the same format as a list of JSON objects."
    )

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a helpful assistant that processes nutritional data."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )

    # Extract the response
    rational_items = response.choices[0].message['content'].strip()
    return rational_items