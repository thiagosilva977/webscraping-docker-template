import logging
import os

import click
from scrapy.crawler import CrawlerProcess

from project_scraper.spiders.my_spider import MySpiderSpider

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


@click.command("scrape-url")
@click.option("--url", type=click.STRING, help="Website url to scrape data", default=None)
@click.option("--output-path", type=click.STRING, help="Your local path to save files", default=".")
def main(url: str, output_path: str):
    """
    Main program execution.
    https://www.randomlists.com/urls

    bash to output docker files
    docker run -it -v /path/to/local/folder:/data scrapy-image scrapy crawl spider_name -o /data/output.json


    :param output_path:
    :type url: url to search
    :return: .json file
    """
    logging.debug(str(f"Initializing data collector"))
    logging.info(str(f"Searching url: {url}"))
    logging.info(str(f"Output path: {output_path}"))

    try:
        os.remove('collected_website_data.json')
    except FileNotFoundError:
        pass

    process = CrawlerProcess(settings={'BOT_NAME': 'project_scraper',
                                       'ROBOTSTXT_OBEY': False,
                                       'CONCURRENT_ITEMS': 32,
                                       'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
                                       'CONCURRENT_REQUESTS_PER_IP': 16,
                                       'DOWNLOAD_TIMEOUT': 6,
                                       'FEED_EXPORT_ENCODING': 'utf-8',
                                       'NEWSPIDER_MODULE': 'project_scraper.spiders',
                                       'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
                                       'RETRY_ENABLED': False,
                                       'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408],
                                       'RETRY_TIMES': 5,
                                       'FEED_FORMAT': 'json',
                                       'FEED_URI': str(f"{output_path}/collected_website_data.json"),
                                       'SPIDER_MODULES': ['project_scraper.spiders'],
                                       'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
                                       'ITEM_PIPELINES': {
                                           'project_scraper.pipelines.ProjectScraperPipeline': 300,
                                       }
                                       }

                             )

    process.crawl(MySpiderSpider, url)
    process.start()


if __name__ == '__main__':
    main()
