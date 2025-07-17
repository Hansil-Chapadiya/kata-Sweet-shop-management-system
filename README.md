# 🍬 Kata Sweet Shop Management System

## ⚠️ PLEASE WAIT ⏳
### 💤 The API is hosted on Render and may take up to **50 seconds** to wake up after inactivity. Please be patient while waiting for responses.

---

## 📦 Project Overview

This is a full-stack **Sweet Shop Inventory Management System** that allows you to:

- 🔍 Search & view all available sweets
- ➕ Add new sweets with name, type, quantity, and price
- 📦 Track inventory with sorting, filtering, and low-stock alerts
- 🔁 Restock sweets (Optional)
- 📩 Email notifications on low stock (backend functionality)
- 🎨 Clean and responsive UI using Tailwind CSS with **Orange & White** theme

---

## 🚀 Live Demo

- 🖥️ **Frontend (Next.js)**: [https://kata-sweet-shop-management.vercel.app](https://kata-sweet-shop-management.vercel.app)
- 🧠 **Backend (FastAPI on Render)**: [https://kata-sweet-shop-management-system.onrender.com/](https://kata-sweet-shop-management-system.onrender.com/)

---

## 🛠 Tech Stack

| Frontend         | Backend         | Database  | Styling       |
|------------------|------------------|-----------|----------------|
| Next.js (React)  | FastAPI (Python) | MongoDB   | Tailwind CSS   |

---

## 📁 Features

### ✅ Main Functionalities

- 🧁 **Add Sweet**: Add new sweet items via a form
- 📃 **Inventory Table**: View all sweets with sorting
- 🔎 **Search & Filter**: Filter sweets by name or type
- 📉 **Low Stock Alerts**: Highlight items below threshold
- 🌐 **API Integration**: Realtime calls with async handling
- 🌒 **Production-Ready Deployment**: Vercel + Render combo

---

## 🧪 Testing

- Frontend tested with manual UI + form inputs
- Backend tested with Pytest and HTTPX for async endpoints

---

## ⚙️ Environment Variables

```env
NEXT_PUBLIC_API_URL=https://kata-sweet-shop-api.onrender.com
