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
soc-phishing-analyzer/
├── app/
│   ├── services/
│   │   ├── firebase_service/   # Firebase storage and Firestore integration
│   │   ├── google_chat/        # Sends notifications to Google Chat
│   │   ├── google_sheet/       # Handles Google Sheets integration
│   │   ├── mysql_service/      # Database interactions
│   │   ├── openai_service/     # OpenAI and LangChain integration
│   ├── utils/
│   │   ├── config.py           # Configuration settings
│   │   ├── constants.py        # Global constants
│   │   ├── worker.py           # Worker function for async processing
│   │   ├── scraper_page.py     # Web scraping logic
│   │   ├── html_context.py     # HTML content processing
│   │   ├── image_context.py    # Image processing utilities
│   │   ├── prompt_template.py  # LangChain prompt templates
│   ├── main.py                 # Entry point for execution
│
├── venv/                       # Python virtual environment
├── .dockerignore               # Docker ignore file
├── .gitignore                  # Git ignore file
├── .env                        # Environment variables
├── Dockerfile                  # Docker configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
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
   cd soc-phishing-analyzer
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
Ensure the environment variables are set in the `.env` file:


## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m "Add feature"`.
4. Push to branch: `git push origin feature-name`.
5. Open a Pull Request.

## Contact
For any issues or questions, contact **SOC Team - WSO2 LLC**.
**Developed by Vipun Sanjana**.