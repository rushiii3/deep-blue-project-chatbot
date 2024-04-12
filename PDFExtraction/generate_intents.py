import json
from intents_generator import SubjectiveTest
intents = {"intents": []}

# Open the JSON file
with open('./file_output/output.json', 'r') as file:
    # Read the contents of the file
    json_data = json.load(file)

# Iterate over each key in the JSON data
for key, value in json_data.items():
    print(f"Key: {key}")
    # Check if the value is a list
    if isinstance(value, list):
        # Iterate over each item in the list
        for item in value:
            # Iterate over each key-value pair in the item
            for sub_key, sub_value in item.items():
                # print(f"\t{sub_key}: {sub_value}")
                subjective_generator = SubjectiveTest(sub_value)
                result = subjective_generator.generate_test()
                if result is None:
                    print("No keywords found for:", sub_key, ". Continuing with further processing.")
                else:
                    question_list, answer_list, keyword = result
                    for q, a, k in zip(question_list, answer_list, keyword):
                        intent = {
                            "tag": k,
                            "patterns": [q],
                            "responses": [a]
                        }
                        # Append the intent to the intents list
                        intents["intents"].append(intent)
                        print("Question:", q)
                        print("Answer:", a)
                        print("Keywords:", k)
                        print()

    else:
        # If the value is not a list, it's a dictionary
        # Iterate over each key-value pair in the dictionary
        for sub_key, sub_value in value.items():
            print(f"\t{sub_key}: {sub_value}")
            print()
with open('intents.json', 'w') as file:
    json.dump(intents, file, indent=4)