# Get planting and care details about a crop plant from GPT-4
# Usage: python garden_schema.py [zone] [plant,names,csv,list]
# jheckt 2023-06-14


import openai
import os, sys

openai.api_key = os.environ["OPENAI_API_KEY"]

# Get arguments
args = sys.argv[1:]

schema = {
  "type": "object",
  "properties": {
    "plant-info": {
        "type": "object",
        "description": "Basic, factual details about the plant. Short answers.",
        "properties": {
            "common-name": {"type": "string"},
            "latin-name": {"type": "string"},
            "plant-description": {"type": "string"},
        },
        "required": ["common-name", "latin-name", "plant-description"],
        },
    "planting-details": {
        "type": "object",
        "description": "Details on how to sow, care, and harvest the plant.",
        "properties": {
            "soil": {"type": "string"},
            "sun": {"type": "string"},
            "water": {"type": "string"},
            "sowing-method": {"type": "string"},
            "grow-days": {"type": "number"},
            "sowing-months": {
                "type": "array",
                "items": {"type": "string"},
            },
            "harvest-months": {
                "type": "array",
                "items": {"type": "string"},
            },
            "planting-instructions": {"type": "string"},
            "care-instructions": {"type": "string"},
            "harvest-instructions": {"type": "string"},
        },
            "required": ["soil", "sun", "water", "sowing-method", 
                        "grow-days", "sowing-months", "harvest-months","planting-instructions","care-instructions"
                        "harvest-instructions"],
        },
    },
    "required": ["plant-info", "planting-details"],
}


def get_plant_data(plant_name, zone) -> str:
    """
    Get planting and care details about a crop plant from GPT-4
    """
    completion = openai.ChatCompletion.create(
      model="gpt-4-0613",
      messages=[
        {"role": "system", "content": "Please be a helpful organic gardending assistant."},
        {"role": "user", "content": f"Provide planting and growing details for {plant_name} in zone {zone}."}
      ],
      functions=[{"name": "get_plant_info", "parameters": schema}],
      function_call={"name": "get_plant_info"},
      temperature=0,
    )

    return completion.choices[0].message.function_call.arguments


if __name__ == "__main__":
    zone = args[0]
    plants = args[1].split(",")
    garden_object = {}

    for plant in plants:
        plant_data = get_plant_data(plant, zone)
        garden_object[plant] = plant_data

    print(garden_object)


