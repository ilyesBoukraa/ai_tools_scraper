# ai_tools_scraper

## Overview
AI Tools Scraper is a Python script that enables you to scrape data from the "[Top AI Tools](https://topai.tools/browse)" website. The script uses Selenium,
a powerful web automation library, to navigate the website and extract information about various AI tools available on the platform.

## Features
- **Efficient Web Scraping:** The script utilizes Selenium to efficiently scrape data from the website, even from pages with infinite scrolling, allowing you to collect a substantial amount of AI tool data.
- **Data Extraction:** The script extracts essential information for each AI tool, including its name, URL, description, pricing, tags, and use cases.
- **Saving to CSV:** The extracted data is saved to a CSV file, making it easy to analyze and use for further processing.

## How to Use
1. Clone the repository or download the script directly.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Ensure you have Microsoft Edge WebDriver installed and placed in the system's PATH.
4. Open the script (`ai_tools_scraper.py`).
5. Run the script: `python ai_tools_scraper.py`.
6. The script will automatically open the Microsoft Edge browser, navigate to the specified URL, and start scraping AI tool data.
7. Once the scraping is complete, the extracted data will be saved to a CSV file named `ai_tools.csv` by default. You can specify a different output file name by modifying the `output_file_name` variable in the `main` function.
