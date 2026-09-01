# CRM Application with BANT Qualification & AI Assistant

This repository contains the source code for a full-stack Customer Relationship Management (CRM) web application. Built as a Bachelor's Thesis project, this platform is tailored for small and medium-sized enterprises (SMEs) to streamline their sales processes, monitor lead lifecycles, and leverage Artificial Intelligence for natural language data querying.

## 🚀 Key Features

### 📊 Comprehensive Lead Management
* **BANT Qualification Framework:** Leads are qualified strictly following the Budget, Authority, Need, and Timeline methodology.
* **Interactive Kanban Board:** Manage the sales pipeline effortlessly using a drag-and-drop Kanban interface or a paginated table view.
* **Dynamic Scoring Engine:** The system auto-calculates a lead's "Confidence" score (0-100) and priority (Low, Medium, High) in real-time as qualification checkpoints are met.
* **State-Machine Lifecycle:** Leads follow a strict progression (New -> Contacted -> In Progress -> Won/Lost/Inactive), heavily validated at the backend level.

### 🤖 Conversational AI Assistant (MCP)
* **Natural Language Queries:** Users can ask the built-in AI assistant to fetch CRM metrics or summarize lead data using natural language.
* **Decoupled MCP Architecture:** The AI functionality is powered by the Model Context Protocol (MCP). It features an MCP Client running inside the Django app and a standalone `FastMCP` Server operating on an independent ASGI server (port 8001).
* **OpenAI Function Calling:** The assistant securely maps LLM reasoning to internal REST API endpoints without hallucinating business logic, maintaining strict team-based data isolation.

### ⚙️ Smart Automations & Workflows
* **Event-Driven Tasks:** The backend automatically generates time-sensitive follow-up tasks whenever a lead transitions between statuses.
* **Automated Client Conversion:** Marking a lead as "Won" triggers an automatic conversion process, seamlessly transferring all historical data, email logs, and notes to a new `Client` entity.

### 🔌 Third-Party Integrations
* **Google Workspace:** Supports secure OAuth2 alternative login and automatic two-way synchronization of CRM tasks directly to the user's personal Google Calendar.
* **Mailjet REST API:** Send customized emails (supporting up to 5 Base64 encoded attachments) and maintain an immutable communication log right from the lead's profile.

### 📈 Analytics & Reporting
* **Visual Dashboard:** Integrated `vue-chartjs` components display essential KPIs, including win rates, lead status distribution, and pipeline value.
* **Data Export:** Generate and download reports natively in CSV, XLSX, or PDF formats.

### 🏢 Team & Access Management (RBAC)
* **Strict Data Isolation:** All database records are strongly bound to specific `Team` entities, ensuring agents only see data belonging to their respective departments.
* **Self-Serve Onboarding:** Administrators can generate temporary, 1-minute expiration invite codes to easily onboard new team members.

---

## 🛠️ Technology Stack

This project utilizes a modern, fully decoupled Client-Server architecture.

### Backend (REST API)
* **Framework:** Python 3, Django 6.0, Django REST Framework (DRF).
* **Asynchronous Server:** Uvicorn (ASGI) for non-blocking I/O operations, ensuring high performance for AI routing and external API calls.
* **Database:** SQLite (development environment), heavily optimized with `select_related` and `prefetch_related` queries to eliminate N+1 bottlenecks.
* **Authentication:** Djoser, Simple JWT (JSON Web Tokens).

### Frontend (SPA)
* **Framework:** Vue.js 3 (Composition API), Vite.
* **State Management:** Pinia.
* **Routing:** Vue Router.
* **Styling:** TailwindCSS, Flowbite UI.
* **HTTP Client:** Axios (with automated JWT header interceptors).

### AI Server
* **Framework:** FastMCP (Port 8001).
* **Integration:** Model Context Protocol (MCP), OpenAI API.

---

## 🏗️ Architecture Overview

1. **Presentation Layer:** The Vue SPA handles the user interface, local validation, and state reactivity without full page reloads.
2. **Business Logic Layer:** The Django backend is modularized (`lead`, `client`, `tasks`, `products`, `emails`, `ai_assistant`, `team`). Complex operations, like Lead creation with nested address and product interests, are executed inside atomic database transactions.
3. **Data Layer:** A relational schema featuring strict foreign key constraints (e.g., cascading deletes for orphaned records, protected deletes for historical data consistency).

---

## 👨‍💻 Author
**Alexandru Marian Pașcalău**
