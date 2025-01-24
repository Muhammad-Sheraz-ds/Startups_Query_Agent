
# Startups Query Agent

Startups Query Agent is a comprehensive platform that collects, processes, and queries startup-related data with a focus on intelligent querying and user-friendly interaction. The platform leverages tools like Scrapy for web scraping, OpenAI's SQL Agent for natural language queries, Streamlit for an interactive frontend, and FastAPI for backend API services. The data pipeline is designed to be robust, modular, and easy to set up.

---

## Features

- **Data Scraping**: Efficiently scrapes structured data of startups from Y Combinator using Scrapy.  
- **ETL Pipeline**: Extracts, transforms, and loads data into an SQLite database for querying.  
- **SQL Agent Integration**: Leverages OpenAI’s SQL Agent for seamless natural language queries.  
- **Interactive Frontend**: Provides a Streamlit-based user interface for insights and queries.  
- **Scalable Backend**: Uses FastAPI to handle API requests between the frontend and database.  
- **Docker Support**: Fully containerized for easy deployment and scaling.

---

## Project Structure

```
Startups-Query-Agent/
├── Untitled.ipynb                  # Jupyter Notebook for prototyping and testing
├── .gitignore                      # Git ignore file
├── docker-compose.yml              # Docker Compose configuration
├── setup.sh                        # Script to set up the virtual environment and dependencies
├── requirements.txt                # General dependencies for the project
├── README.md                       # Project documentation
├── LICENSE                         # License file
├── Dockerfile                      # Dockerfile for backend services
├── a.py                            # Script to print folder structure
├── backend/                        # Backend service folder
│   ├── db_setup.py                 # Database setup and migration script
│   ├── requirements.txt            # Backend-specific dependencies
│   ├── etl.py                      # ETL script for transforming scraped data
│   ├── app.py                      # FastAPI application file
│   ├── query_agent.py              # SQL Agent setup using OpenAI
├── data/                           # Folder containing database files
│   ├── database.db                 # SQLite database for processed data
├── YC-Scraper/                     # Folder for scraping-related code
│   ├── .gitignore                  # Git ignore file for the scraper
│   ├── requirements.txt            # Scraper-specific dependencies
│   ├── README.md                   # Scraper-specific documentation
│   ├── scraper/                    # Scraper implementation folder
│   │   ├── scrapy.cfg              # Scrapy configuration file
│   │   ├── Dockerfile              # Dockerfile for the scraper
│   │   ├── data/                   # Folder for input and raw data
│   │   │   ├── start_urls.txt      # List of URLs to scrape
│   │   ├── scripts/                # Additional utility scripts
│   │   │   ├── yc_links_extractor.py  # Script to extract Y Combinator links
│   │   ├── scraper/                # Scraper output data folders
│   │   │   ├── data/
│   │   │   │   ├── raw/            # Folder for raw scraped data
│   │   │   │   │   ├── scraped_data.csv
│   │   │   │   ├── processed/      # Folder for processed data
│   │   │   │   │   ├── processed_data.csv
│   │   ├── ycombinator/            # Y Combinator-specific scraper logic
│   │   │   ├── pipelines.py
│   │   │   ├── items.py
│   │   │   ├── middlewares.py
│   │   │   ├── settings.py
│   │   │   ├── __init__.py
│   │   │   ├── spiders/            # Spider definitions
│   │   │   │   ├── yscraper.py
│   │   │   │   ├── __init__.py
├── backup/                         # Backup of older data or experiments
│   ├── 2023-02-27-yc-companies.csv
│   ├── scraped_data.csv
├── frontend/                       # Frontend service folder
│   ├── requirements.txt            # Frontend-specific dependencies
│   ├── app.py                      # Streamlit application file
```

---

## Installation and Setup

### Prerequisites

- Python 3.10+
- pip
- Docker (optional for containerized setup)
- OpenAI API Key (for SQL Agent)

---

### Step 1: Clone the Repository

```bash
git clone git@github.com:YourUsername/Startups-Query-Agent.git
cd Startups-Query-Agent
```

---

### Step 2: Set Up the Virtual Environment

```bash
bash setup.sh
```

---

### Step 3: Provide the OpenAI API Key

Add your OpenAI API key to the environment by creating a `.env` file in the `backend/` directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Alternatively, you can export the key directly:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

---

### Step 4: Run the Scraper

Navigate to the scraper directory and run the Scrapy crawler:

```bash
cd YC-Scraper/scraper
scrapy crawl yscraper
```

This will save the raw scraped data in `YC-Scraper/scraper/scraper/data/raw/scraped_data.csv`.

---

### Step 5: Process the Data

Run the ETL script to process and save data into the SQLite database:

```bash
cd ../..
python3 backend/etl.py
```

---

### Step 6: Start Backend API

Run the FastAPI backend:

```bash
cd backend
python3 app.py
```

The API will be accessible at `http://127.0.0.1:8000`.

---

### Step 7: Start Frontend

Launch the Streamlit frontend:

```bash
cd frontend
streamlit run app.py
```

Access the Streamlit app at `http://127.0.0.1:8501`.

---

## Usage

- Query startups via the Streamlit app using natural language (e.g., "List all startups founded in 2020").
- Access API endpoints for more advanced use cases.



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## **Contributing**
1. Fork the repository.
2. Create a new branch.
3. Submit a pull request.

