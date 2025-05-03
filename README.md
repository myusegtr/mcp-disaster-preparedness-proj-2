# 🌍 Disaster Preparedness AI System

## 🧭 AIM

To build a robust, AI-enhanced disaster alert system leveraging real-time weather and earthquake data using the **FastMCP framework**, with hybrid deployment — a local MCP-based interactive chatbot and a production-grade API server hosted on **AWS EC2**.

---

## 📖 Project Description

This project is a two-part AI-driven disaster preparedness application designed to assist users with real-time environmental hazard information across the U.S. and globally:

1. **Local Interactive MCP Chat Interface (`client.py`)**  
   A command-line conversational AI tool using Groq-powered LLM and MCPAgent, enabling users to retrieve live weather alerts by state.

2. **Deployed Disaster Alert API Server (`disaster.py`)**  
   A FastMCP-based API server that exposes tools for fetching:
   - Active weather alerts (via NOAA's NWS API)
   - Significant earthquakes in the past 24 hours (via USGS GeoJSON Feed)

The system is modular, extensible, and serves as a foundation for integrating more disaster types, IoT triggers, and user alerting channels (SMS, Email, Webhooks).

---

## 🛠️ Tools & Technologies Used

### 🧑‍💻 Common Across Both Parts
- **Python 3.11+**
- **FastMCP** — Framework for building agent and tool-based apps.
- **LangChain + Groq** — For LLM chat integration.
- **httpx** — Asynchronous HTTP client for data fetching.
- **MCPAgent / MCPClient** — For managing tools and agent logic.
- **Open APIs**:
  - NOAA National Weather Service API
  - USGS Earthquake GeoJSON API

### 📍 Part 1 — Local Chat Interface (`client.py`)
- **LangChain-Groq** (Qwen QWQ-32B model)
- `.env` file for storing API keys
- CLI-based memory-enabled conversational system

### ☁️ Part 2 — Deployed Server (`disaster.py`)
- **FastAPI via FastMCP**
- Hosted using **AWS EC2 Free Tier**
- Optional: `uvicorn` for serving the API

---

## ✅ Inference / Conclusion

This AI-powered disaster alert system offers:

- **Real-time, multi-source alerting**
- **Flexible deployment**: local dev + cloud production
- **Modular tool definition** for easy expansion
- **LLM memory support** for interactive querying

By integrating key U.S. government data sources with modern AI interfaces, it demonstrates how accessible and proactive disaster intelligence can be achieved with lightweight Python tools and cloud computing.

---

## 🚀 Deployment (AWS EC2)

### Deploy Using AWS EC2 Instance

> Amazon EC2 (Elastic Compute Cloud) acts as a remote virtual server to run production-grade Python apps.

### 🧱 Prerequisites
- AWS account (free tier)
- GitHub repository with your code
- `.pem` key pair for EC2 access

### 🔧 Step-by-Step Setup

1. **Login to AWS Console**
   - Go to: https://console.aws.amazon.com

2. **Launch EC2 Instance**
   - EC2 → Launch Instance
   - Name: `mcp-server`
   - OS: Amazon Linux 2023 (Free tier eligible)
   - Type: `t2.micro`
   - Key Pair: Create/download a `.pem` file
   - Networking: Enable **SSH (port 22)** and optionally **HTTP (80)**

3. **Connect to EC2 via SSH**
   ```bash
   ssh -i "your-key.pem" ec2-user@<your-ec2-public-ip>

4. **Install Python & Git on EC2**
   ```bash
   sudo yum update -y
   sudo yum install python3 git -y

5. **📥 Clone Your GitHub Repository**
    ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

6. **🧪 Set Up Python Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt 

7. **Run the API Server**   
   ```bash
   uvicorn disaster:app --host 0.0.0.0 --port 8000
   Open the url received in browser

8. **💡 Further Improvements**   

   🌐 Frontend Dashboard using React or Vue for visualizing alerts

   📲 Push notifications (SMS, Email, Telegram bots)

   📊 Alert severity analytics over time

   🔒 OAuth integration for secured access

   🛰️ IoT sensor data integration (flood, seismic, fire sensors)

   📁 Log storage and alert history archiving (S3 or DynamoDB)




### 🖥️ How to Use Locally

**Clone the Repo**
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

**Initialize Groq api key and install requirements**
    GROQ_API_KEY=your_groq_api_key
    ```bash
    pip install -r requirements.txt

**Run locally in terminal**
    ```bash
    uv run server/client.py


    



