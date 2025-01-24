import json
import scrapy



def make_start_urls_list():
    """Returns a list with the start URLs from a plain text file."""
    with open('/home/sheraz/Artificial Intelligence/Projects/yc-scraper-main/YC-Scraper/scraper/data/start_urls.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

import json
import scrapy
import csv
import os


class YCombinator(scrapy.Spider):
    """Crawls ycombinator.com/companies and extracts data about each company."""
    name = 'YCombinatorScraper'
    # Uncomment the line below if you're loading start_urls dynamically
    start_urls = make_start_urls_list()
    #start_urls = ['https://www.ycombinator.com/companies/happenstance']

    # Path for saving the CSV file
    output_file = './scraper/data/raw/scraped_data.csv'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Create or clear the CSV file on spider start
        if not os.path.exists(os.path.dirname(self.output_file)):
            os.makedirs(os.path.dirname(self.output_file))  # Create directories if they don’t exist

        # Write headers to the CSV file
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=[
                'company_id',
                'company_name',
                'short_description',
                'long_description',
                'batch',
                'status',
                'tags',
                'location',
                'country',
                'year_founded',
                'num_founders',
                'founders_names',
                'team_size',
                'website',
                'cb_url',
                'linkedin_url'
            ])
            writer.writeheader()

    def parse(self, response):
        try:
            st = response.css('[data-page]::attr(data-page)').get()
            if st is not None:
                jo = json.loads(st)['props']
                jc = jo['company']

                # Prepare data for writing to the CSV
                data = {
                    'company_id': jc['id'],
                    'company_name': jc['name'],
                    'short_description': jc['one_liner'],
                    'long_description': jc['long_description'],
                    'batch': jc['batch_name'],
                    'status': jc['ycdc_status'],
                    'tags': ', '.join(jc['tags']) if jc['tags'] else None,
                    'location': jc['location'],
                    'country': jc['country'],
                    'year_founded': jc['year_founded'],
                    'num_founders': len(jc['founders']),
                    'founders_names': ', '.join([f['full_name'] for f in jc['founders']]),
                    'team_size': jc['team_size'],
                    'website': jc['website'],
                    'cb_url': jc['cb_url'],
                    'linkedin_url': jc['linkedin_url']
                }

                # Append data to the CSV file
                with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=data.keys())
                    writer.writerow(data)

                # Log successful scrape
                self.logger.info(f"Scraped data for company: {jc['name']}")
            else:
                self.logger.warning(f"No JSON object found on {response.url}")
        except Exception as e:
            self.logger.error(f"Error parsing {response.url}: {e}")


