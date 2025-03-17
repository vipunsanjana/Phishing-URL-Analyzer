# URL Phishing Detection and Reporting System

## Overview
This project automates the detection and reporting of phishing URLs by integrating multiple technologies, including:
- **Firebase** for real-time database interactions.
- **MySQL** for storing URLs and related metadata.
- **LangChain** for AI-based processing and decision-making.
- **Google Sheets** for reporting and logging data.
- **Google Chat** for sending alerts and notifications.
- **OpenAI** for enhanced analysis.
- **Azure Log Analytics** for initial query execution.

The system first runs a **KQL query** in **Azure Log Analytics** to fetch URLs and cluster names. Then, it retrieves URLs from **MySQL** and processes them one by one to determine if they are phishing URLs.

## Features
- **Automated Phishing Detection:** Scrapes and analyzes URLs.
- **Database Management:** Stores URLs and metadata in **MySQL**.
- **Queue-based Processing:** Uses `asyncio.Queue` for parallel URL processing.
- **Retry Mechanism:** Implements error handling with retries.
- **Integration with Google Services:**
  - **Google Sheets** for logging.
  - **Google Chat** for notifications.
- **AI-powered Analysis:** Uses **LangChain** and **OpenAI**.

## Technologies Used
- **Python (asyncio, MySQL connector, Google APIs)**
- **Firebase**
- **MySQL**
- **LangChain**
- **Google Sheets API**
- **Google Chat Webhook**
- **OpenAI API**
- **Azure Log Analytics** (for KQL queries)

## Project Structure
```
app/
├── services/
│   ├── google_chat/
│   │   ├── send_message.py    # Sends notifications to Google Chat
│   ├── google_sheet/
│   │   ├── sheet.py           # Handles Google Sheets integration
│   ├── mysql_service/
│   │   ├── datasaving.py      # Database interactions
├── utils/
│   ├── config.py              # Configuration settings
│   ├── worker.py              # Worker function for async processing
│   ├── scraper_page.py        # Web scraping logic
│   ├── constants.py           # Global constants
├── main.py                     # Entry point for execution
```

## Workflow
1. **Run KQL Query:** Fetch URLs and cluster names from Azure Log Analytics.
2. **Fetch URLs from MySQL:** Retrieve unprocessed URLs from the database.
3. **Queue Processing:**
   - URLs are added to an `asyncio.Queue`.
   - `worker` functions pick URLs and process them asynchronously.
   - Each URL is analyzed for phishing characteristics.
4. **Data Storage and Logging:**
   - Phishing results are stored in **MySQL**.
   - Logs are added to **Google Sheets**.
5. **Error Handling & Retry:**
   - Failed URLs are retried up to two times.
   - Errors are logged and reported via **Google Chat**.
6. **Notification & Cleanup:**
   - Phishing reports are sent to **Google Chat**.
   - Processed records are deleted from the database.

## Installation
1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <project-folder>
   ```
2. Set up Python virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure **Google Sheets API**, **Google Chat Webhook**, and **OpenAI API**.
5. Set up **MySQL** and **Firebase** configurations in `config.py`.
6. Run the main script:
   ```sh
   python main.py
   ```

## Environment Variables
Ensure the following environment variables are set:
```sh
  add env variables
```

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push to branch: `git push origin feature-name`.
5. Open a Pull Request.

## License
MIT License

## Contact
For any issues or questions, contact **[Your Name]** at **your.email@example.com**.

# 🌈 **Automated URL Scraping and Analysis Workflow**

Automate your URL scraping, content analysis, and security monitoring with a seamless, end-to-end solution. This workflow captures unique URLs from **Choreo Webapps logs**, processes them through a web scraping API, generates insightful analyses with **OpenAI** using **LangChain**, and sends responses.

---

## 📊 **Workflow Overview**

This automation consists of **primary trigger**:

1. **URL Analysis Automation**

---

## 🖍️ **Step-by-Step Process**

### 🔍 **1. URL Analysis Automation**

1. **Trigger Web Scraping API**

   - Processes each URL through the **web scraping API**.

2. **Web Scraper Endpoint**

   - Hosted on an **Azure VM**, the scraper extracts:
     - ✅ **Text Content**
     - ✅ **HTML Content**
     - ✅ **Screenshots** of the webpage
   - **Screenshots are stored** in **Firebase Image Storage**.

3. **Generate Analysis with OpenAI and LangChain**

   - Processes the extracted content using **OpenAI** and **LangChain** to generate concise summaries for each URL.

---

## 📂 **Folder Structure**

```
.
├── app/
│   ├── main.py                  # Entry point for the FastAPI application
│   ├── utils/                   # Utility functions and constants
│   │   ├── constants.py         # Constants and configurations
│   │   ├── scraper_page.py      # Web scraping logic
│   │   ├── html_context.py      # HTML content processing
│   │   ├── image_context.py     # Image processing utilities
│   │   ├── prompt_template.py   # LangChain prompt templates
│   ├── services/                # External service integrations
│   │   ├── firebase_service/    # Firebase storage and Firestore integration
│   │   ├── openai_service/      # OpenAI and LangChain integration
│
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── Dockerfile                   # Docker configuration
├── .dockerignore                # Docker ignore file
├── openapi.yaml                 # OpenAPI specification
└── README.md                    # Project documentation
```

---

## ⚙️ **Setup and Installation**

### 🛠️ **1. Install Dependencies**

```bash
pip install -r requirements.txt
```

### 🔒 **2. Set Up Environment Variables**

Create a `.env` file in the project root with these variables:

```env
FIREBASE_CREDENTIALS=path/to/serviceAccountKey.json
OPENAI_API_KEY=your_openai_api_key
BUCKET_NAME=your_firebase_bucket_name
COLLECTION_NAME=your_firestore_collection_name
```

### 🚀 **3. Run Automation Scripts**

1. **URL Analysis Automation**:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🌐 **Endpoints**

### **Web Scraper API**

- **URL**: `http://localhost:8003/status`

- **Method**: `GET`

- **Response Example**:

  ```json
  {
    "status": "running"
  }
  ```

- **URL**: `http://localhost:8000/scrape`

- **Method**: `POST`

- **Payload Example**:

  ```json
  {
    "url": "https://example.com"
  }
  ```

---

## 📦 **Dependencies**

### `requirements.txt`

```txt
fastapi
uvicorn
pydantic
playwright
beautifulsoup4
pillow
python-dotenv
requests
firebase-admin
lxml
openai
langchain
langchain-openai
PyYAML
```

---

## 🚀 **Future Improvements**

🌟 **Enhance Your Automation**:

- **Error Handling**: Add robust error handling for failed web scraping tasks.
- **Retry Logic**: Implement retries for failed API calls.
- **Logging**: Improve logging to enhance traceability and debugging.
- **Dynamic Prompt Templates**: Allow dynamic customization of LangChain prompts based on input data.
- **Scalability**: Optimize the workflow for handling large volumes of URLs.

---

## 📧 **Contact**

For support or inquiries, please reach out to the **SOC Team - WSO2 LLC**.\
**Developed by Vipun Sanjana**

