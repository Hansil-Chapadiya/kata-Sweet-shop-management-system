---
# 🍬 Kata Sweet Shop Management System (Angular + FastAPI)

## ⚠️ PLEASE WAIT ⏳
### 💤 The API is hosted on Render and may take up to **50 seconds** to wake up after inactivity. Please be patient while waiting for responses.

---

## 📦 Project Overview

A full-stack **Sweet Shop Inventory Management System** to:

- 🔍 Search and view available sweets
- ➕ Add new sweets with name, type, quantity, and price
- 📦 Track inventory with sorting, filtering, and low-stock alerts
- 🔁 Restock sweets
- 📩 Email alerts on low stock (background tasks)
- 🎨 Clean and responsive UI using Angular with an **Orange & White** theme

---

## 🚀 Live Demo

- 🖥️ **Frontend (Angular)**: [https://kata-sweet-shop-management-system-r.vercel.app](https://kata-sweet-shop-management-system-r.vercel.app)
- 🧠 **Backend (FastAPI on Render)**: [https://kata-sweet-shop-management-system.onrender.com](https://kata-sweet-shop-management-system.onrender.com)

---

## 🛠 Tech Stack

| Frontend   | Backend          | Database | Styling    |
| ---------- | ---------------- | -------- | ---------- |
| Angular 14 | FastAPI (Python) | MongoDB  | SCSS / CSS |

---

## 📁 Features

### ✅ Core Functionalities

- 🧁 **Add Sweet**: Add sweets with name, type, quantity, and price
- 📃 **Inventory Table**: View sweets with sorting and pagination
- 🔍 **Search & Filter**: Filter sweets by name or type
- ⚠️ **Low Stock Highlight**: Auto-highlight items below stock threshold
- 🔄 **Restock Feature**: Increase quantity of existing sweets
- 📩 **Email Notification System**: Auto email alerts on low stock via background task
- 🌐 **API Integration**: Full integration with FastAPI backend

---

## 🧪 Testing

- ✅ **Frontend**: Manually tested with reactive forms and UI flow
- ✅ **Backend**: Tested with **Pytest** and **HTTPX** for async APIs

---

# 🍬 Kata Sweet Shop Management System

## 🧁 Dashboard
![Dashboard](./assets/Dashboard.png)

## ➕ Add Sweet
![Add Sweet](./assets/addSweet.png)

## 🗑️ Delete Sweet
![Delete Sweet](./assets/Delete%20Sweet.png)

## 🏠 Home Page
![Home Page](./assets/HomePage.png)

## 📦 Purchase Screen
![Purchase](./assets/Purchase.png)

## 🔁 Restock Screen
![Restock](./assets/Restock.png)

## ✅ Success Alert
![Success](./assets/Success.png)


## ⚙️ Environment Variables

```env
# Angular (environment.ts or environment.prod.ts)
API_URL=https://kata-sweet-shop-management-system.onrender.com
NEXT_PUBLIC_API_URL=https://kata-sweet-shop-api.onrender.com
