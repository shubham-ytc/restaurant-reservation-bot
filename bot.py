import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from word2number import w2n
import pandas as pd
# ------------------- NLTK Downloads -------------------
nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")

# ---------------- CSV Loader ----------------

def load_training_data_from_csv(file_path):
    df = pd.read_csv(file_path)
    print("training...")
    # Convert CSV into list of (text, intent)
    training_data = list(zip(df["text"], df["intent"]))
    return training_data

class ImprovedReservationBot:
    def __init__(self, external_data=None):

        self.lemmatizer = WordNetLemmatizer()

        # Default Training Data
        default_data = [
            ("book a table", "reserve"),
            ("make a reservation", "reserve"),
            ("i want to make a reservation", "reserve"),
            ("i need a table", "reserve"),

            ("menu", "get_menu"),
            ("what is on the menu", "get_menu"),
            ("give me the menu", "get_menu"),

            ("time slot", "get_slots"),
            ("what time slots are available", "get_slots"),
            ("show me available timings", "get_slots"),

            ("hi", "greet"),
            ("hello", "greet"),
            ("goodbye", "goodbye"),

            ("confirm", "confirm"),
            ("yes confirm", "confirm"),
            ("cancel", "cancel"),
            ("no cancel", "cancel")
        ]

        # Merge external data if provided
        if external_data:
            self.training_data = default_data + external_data
        else:
            self.training_data = default_data

        # State Tracker
        self.state = {
            "intent": None,
            "slots": {"party_size": None, "time": None},
            "is_complete": False,
            "awaiting_confirmation": False,
            "booking_confirmed": False
        }

        # Menu Data
        self.menu = {
            "Starters": "Garlic Bread, Caesar Salad",
            "Mains": "Vegetable Pasta, Margherita Pizza, Grilled Paneer",
            "Desserts": "Chocolate Lava Cake, Fruit Salad"
        }

        # Available Time Slots
        self.available_slots = ["6:00 PM", "7:00 PM", "8:30 PM", "9:00 PM"]

        # Train Intent Model
        self.classifier = self._train_intent_model()

    # ------------------- RESET BOT -------------------
    def reset_booking(self):
        self.state = {
            "intent": None,
            "slots": {"party_size": None, "time": None},
            "is_complete": False,
            "awaiting_confirmation": False,
            "booking_confirmed": False
        }

    # ------------------- FEATURES -------------------
    def _get_features(self, text):
        tokens = word_tokenize(text.lower())
        return {self.lemmatizer.lemmatize(t): True for t in tokens}

    def _train_intent_model(self):
        feature_sets = [(self._get_features(s), intent)
                        for (s, intent) in self.training_data]
        return nltk.NaiveBayesClassifier.train(feature_sets)

    # ------------------- TIME NORMALIZER -------------------
    def normalize_time(self, user_time):
        user_time = user_time.lower().replace(" ", "")

        # Convert 6pm -> 6:00 PM
        if re.fullmatch(r"\d{1,2}(am|pm)", user_time):
            hour = int(user_time[:-2])
            suffix = user_time[-2:].upper()
            return f"{hour}:00 {suffix}"

        # Convert 6:30pm -> 6:30 PM
        if re.fullmatch(r"\d{1,2}:\d{2}(am|pm)", user_time):
            hour_min = user_time[:-2]
            suffix = user_time[-2:].upper()
            return f"{hour_min} {suffix}"

        return user_time.upper()

    # ------------------- CONFIRM/CANCEL CHECK -------------------
    def detect_confirm_cancel(self, text):
        t = text.lower().strip()

        confirm_words = ["confirm", "yes", "y", "ok", "okay", "sure"]
        cancel_words = ["cancel", "no", "n", "stop", "not now"]

        if any(word == t for word in confirm_words):
            return "confirm"
        if any(word == t for word in cancel_words):
            return "cancel"

        # if sentence contains confirm/cancel words
        if "confirm" in t or "yes" in t:
            return "confirm"
        if "cancel" in t or "no" in t:
            return "cancel"

        return None

    # ------------------- UPDATE STATE -------------------
    def update_state(self, text):

        # If bot is waiting for confirmation, don't run intent classifier
        if self.state["awaiting_confirmation"]:
            action = self.detect_confirm_cancel(text)

            if action == "confirm":
                self.state["booking_confirmed"] = True
                self.state["awaiting_confirmation"] = False
                self.state["is_complete"] = True
                self.state["intent"] = "confirm"
                return

            elif action == "cancel":
                self.state["intent"] = "cancel"
                return

            else:
                # Still waiting
                self.state["intent"] = "confirm_wait"
                return

        # Predict Intent
        current_intent = self.classifier.classify(self._get_features(text))

        # Keep reservation intent stable
        if self.state["intent"] is None:
            self.state["intent"] = current_intent
        if self.state["intent"] != "reserve":
            self.state["intent"] = current_intent

        # Extract Party Size
        tokens = word_tokenize(text)
        tagged = nltk.pos_tag(tokens)

        for word, tag in tagged:
            if tag == "CD":
                try:
                    val = w2n.word_to_num(word)
                    if val < 20:
                        self.state["slots"]["party_size"] = val
                        self.state["intent"] = "reserve"
                except:
                    pass

        # Extract Time Using Regex
        time_match = re.search(r"(\d{1,2})(:\d{2})?\s?(am|pm)", text.lower())
        if time_match:
            extracted = time_match.group()
            normalized = self.normalize_time(extracted)

            # Validate slot
            if normalized in self.available_slots:
                self.state["slots"]["time"] = normalized
                self.state["intent"] = "reserve"

        # If both slots filled -> ask for confirmation
        if all(self.state["slots"].values()):
            self.state["awaiting_confirmation"] = True

    # ------------------- BOT RESPONSE -------------------
    def get_response(self):

        if self.state["intent"] == "greet":
            return "Hello! How can I help you today?"

        elif self.state["intent"] == "get_menu":
            response = "Here is our menu:\n"
            for category, items in self.menu.items():
                response += f"- {category}: {items}\n"
            return response

        elif self.state["intent"] == "get_slots":
            slots_str = ", ".join(self.available_slots)
            return f"We have these slots available: {slots_str}. Which one works for you?"

        elif self.state["intent"] == "reserve":
            slots = self.state["slots"]

            if not slots["party_size"]:
                return "Sure! For how many people?"

            if not slots["time"]:
                slots_str = ", ".join(self.available_slots)
                return f"Got it, table for {slots['party_size']}. Available times: {slots_str}. Choose one."

            # Both available -> ask confirm
            return f"Please confirm your booking: Table for {slots['party_size']} at {slots['time']}. (confirm/cancel)"

        elif self.state["intent"] == "confirm_wait":
            slots = self.state["slots"]
            return f"Please type **confirm** to book or **cancel** to stop. (Table for {slots['party_size']} at {slots['time']})"

        elif self.state["intent"] == "confirm":
            slots = self.state["slots"]
            msg = f"✅ Booking Confirmed! Table booked for {slots['party_size']} people at {slots['time']}."
            self.reset_booking()
            return msg

        elif self.state["intent"] == "cancel":
            self.reset_booking()
            return "❌ Booking cancelled. No problem! If you want, you can book again anytime."

        elif self.state["intent"] == "goodbye":
            return "Goodbye! Have a great day 😊"

        return "I'm not sure I understand. Can you rephrase?"


# ------------------- RUN CHATBOT -------------------
# Load dataset CSV
csv_data = load_training_data_from_csv("reservation_dataset_1000.csv")

# Pass into bot training
bot = ImprovedReservationBot(external_data=csv_data)

# print("Bot: Hello! I can help you reserve a table, show menu, or available slots.\n")

# while True:
#     user = input("You: ")
#     bot.update_state(user)
#     print("Bot:", bot.get_response())
