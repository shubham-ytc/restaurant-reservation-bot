# 🤖 AI Dining Reservation Chatbot

An intelligent, **intent-based AI agent** built using **Python and Flask**. This system streamlines restaurant bookings by allowing users to reserve tables through natural language conversation, utilizing **Naive Bayes classification** for intent detection and **Scaledown AI** for efficient menu data compression.

## ✨ Features

* **💬 Natural Language Processing**: Conversation-based booking flow.
* **🧠 Intent Detection**: Uses Naive Bayes classification to distinguish between booking requests, menu inquiries, and general FAQs.
* **📅 Smart Slot Filling**: Automatically extracts time, date, and party size from user messages.
* **🗜️ Menu Compression**: Integrates Scaledown AI to handle large menu datasets with minimal latency.
* **🗄️ Database Integration**: Persistent storage of reservations using a SQLite backend.
* **⚡ RESTful API**: Fast and lightweight endpoints for integration with web or mobile frontends.

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **AI/NLP:** Naive Bayes Classification, Scaledown AI (Text Compression)
* **Database:** SQLite (managed via `booking_db.py`)
* **Data Handling:** Pandas, CSV
* **Frontend:** HTML5, CSS3, JavaScript (Tailwind CSS ready)

---

## 📁 Project Structure

```
restaurant-reservation-bot/
├── app.py                # Main Flask application & API routes
├── bot.py                # Chatbot logic & intent classification engine
├── booking_db.py         # Database schema and CRUD operations
├── booking.db            # SQLite database file
├── menu_compressor.py    # Scaledown AI implementation for menu data
├── dataset.py            # Logic for processing reservation datasets
├── reservation_dataset_1000.csv # Training data for the intent model
├── templates/
│   └── index.html        # Frontend Chat Interface
└── README.md             # Project Documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/shubham-yt/restaurant-reservation-bot.git
cd restaurant-reservation-bot
```

### 2️⃣ Environment Setup (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install flask pandas scikit-learn
```

### 4️⃣ Initialize & Run

```bash
python booking_db.py  # Initialize database tables
python app.py         # Start the Flask server
```

*Access the app at: `http://127.0.0.1:5000`*

---

## 🔌 API Documentation

### ➤ Chat Interface

**Endpoint:** `POST /chat`

**Payload:**

```json
{
  "message": "I'd like to book a table for 4 people at 8pm tonight"
}
```

**Response:**

```json
{
  "reply": "I've found an available slot for 4 people at 8:00 PM. Shall I confirm your booking?",
  "intent": "reservation_request"
}
```

### ➤ Menu Retrieval

**Endpoint:** `GET /menu`

**Description:** Fetches the menu processed through the Scaledown AI compressor.

---

## 🔄 Workflow Logic

1. **User Input:** "Table for 2 tomorrow at 7."
2. **Intent Classification:** Naive Bayes identifies this as a `booking` intent.
3. **Slot Filling:** Extract `party_size: 2`, `time: 19:00`, `date: 2026-02-19`.
4. **Database Check:** Queries `booking.db` for availability.
5. **Confirmation:** Bot asks for user confirmation.
6. **Commit:** Final details are written to the `booking` table.

---

## 🗄️ Database Schema (`booking` table)

| Column | Data Type | Description |
| --- | --- | --- |
| `id` | INTEGER | Primary Key (Auto-increment) |
| `name` | TEXT | Customer Name |
| `date` | TEXT | Date of Reservation |
| `time_slot` | TEXT | Reserved Time |
| `party_size` | INTEGER | Number of Guests |

---

## 👨‍💻 Author

**Shubham Holkar** 📍 Mumbai, India

GitHub: [@shubham-ytc](https://github.com/shubham-ytc)

## 📜 License

This project is licensed under the MIT License.

---

**Happy Coding! 🚀**