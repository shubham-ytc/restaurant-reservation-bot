from flask import Flask, request, jsonify
from flask_cors import CORS

from bot import ImprovedReservationBot
from bot import load_training_data_from_csv

# ---------------- Initialize Flask ----------------
app = Flask(__name__)
CORS(app)

# ---------------- Load Model ----------------
csv_data = load_training_data_from_csv("reservation_dataset_1000.csv")
bot = ImprovedReservationBot(external_data=csv_data)

print("✅ Bot trained and ready!")

# ---------------- Chat API Route ----------------
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    bot.update_state(user_message)
    response = bot.get_response()

    return jsonify({"reply": response})


# ---------------- Run Server ----------------
if __name__ == "__main__":
    app.run(debug=True)
