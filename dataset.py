import random
import pandas as pd

# ------------------- Intent Templates -------------------

greet = ["hi", "hello", "hey", "good morning", "good evening"]

goodbye = ["bye", "goodbye", "see you", "thanks bye", "exit"]

reserve_templates = [
    "book a table",
    "i want to reserve a table",
    "can you book a table for {} people",
    "reserve a table for {}",
    "i need a table for {} persons",
    "table booking for {} people",
    "i want dinner reservation for {}",
    "book seat for {} guests"
]

menu_templates = [
    "show me the menu",
    "what is on the menu",
    "give me food list",
    "menu please",
    "what dishes do you have",
    "tell me your menu items"
]

slot_templates = [
    "what time slots are available",
    "show available timings",
    "do you have free slots",
    "available reservation times",
    "when can i come",
    "tell me available slots"
]

confirm_templates = [
    "confirm",
    "yes confirm",
    "okay confirm booking",
    "sure confirm it",
    "book it",
    "yes finalize"
]

cancel_templates = [
    "cancel",
    "no cancel",
    "stop booking",
    "dont book",
    "cancel reservation",
    "never mind cancel"
]

# ------------------- Generate Dataset -------------------

data = []

for _ in range(1000):

    intent_type = random.choice([
        "greet", "goodbye", "reserve",
        "get_menu", "get_slots",
        "confirm", "cancel"
    ])

    if intent_type == "greet":
        text = random.choice(greet)
        intent = "greet"

    elif intent_type == "goodbye":
        text = random.choice(goodbye)
        intent = "goodbye"

    elif intent_type == "reserve":
        template = random.choice(reserve_templates)
        if "{}" in template:
            num = random.randint(1, 10)
            text = template.format(num)
        else:
            text = template
        intent = "reserve"

    elif intent_type == "get_menu":
        text = random.choice(menu_templates)
        intent = "get_menu"

    elif intent_type == "get_slots":
        text = random.choice(slot_templates)
        intent = "get_slots"

    elif intent_type == "confirm":
        text = random.choice(confirm_templates)
        intent = "confirm"

    elif intent_type == "cancel":
        text = random.choice(cancel_templates)
        intent = "cancel"

    data.append([text, intent])

# ------------------- Save CSV -------------------

df = pd.DataFrame(data, columns=["text", "intent"])
df.to_csv("reservation_dataset_1000.csv", index=False)

print("✅ Dataset Generated Successfully!")
print(df.head(10))
