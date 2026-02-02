# restaurant-reservation-bot
first AI agent project with scaledown

# 🍽️ Dining Reservation Chatbot (Compressed Menu + Availability Scheduling)

##  Project Overview

The **Dining Reservation Chatbot** is an intelligent restaurant booking assistant designed to streamline table reservations with improved response times.

This system uses:

- **Compressed menu data**
- **Compressed availability schedules**
- **Fast slot-based reservation logic**

The chatbot provides instant booking confirmations while reducing latency by minimizing repeated full-calendar and full-menu processing.

---

##  Key Features

### Chatbot-Based Reservation Booking
Users can interact naturally to:

- Book a table
- Select number of guests
- Choose available time slots
- Confirm reservations instantly

---

###  Compressed Menu Data
Instead of loading the entire restaurant menu every time, the chatbot stores and serves a compressed menu format:

- Menu grouped by categories
- Reduced storage and faster responses

Example:

```json
{
  "Starters": ["Soup", "Salad"],
  "Main Course": ["Pizza", "Pasta"],
  "Desserts": ["Ice Cream"]
}
