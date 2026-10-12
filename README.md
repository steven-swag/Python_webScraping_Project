 Country Data Pipeline

 About the Project
In this project, I scraped data for the first 20 countries from Scrape This Site using Python. I stored the data in an SQLite database and created a REST API to access and manage the country details.

I also created a client script to fetch data from the API, display it using Pandas, export it to a CSV file, and generate a scatter plot.

 Technologies Used
- Python
- Requests and BeautifulSoup
- SQLite
- FastAPI
- Pandas
- Matplotlib

 How to Run

Install the required packages:

```bash
pip install -r requirements.txt
```

Scrape the country data:

```bash
python scraper.py
```

Start the API server:

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs to test the API.

In a second terminal, run:

```bash
python client.py
```

## Output
- `countries.db` – stores country data
- `exported_countries.csv` – exported country records
- `population_vs_area.png` – scatter plot of population and area
