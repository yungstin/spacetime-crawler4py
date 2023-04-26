from threading import Thread

from inspect import getsource
from utils.download import download
from utils import get_logger
import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.worker_scraper = scraper.Scraper()
        # basic check for requests in scraper
        assert {getsource(scraper).find(req) for req in {"from requests import", "import requests"}} == {-1}, "Do not use requests in scraper.py"
        assert {getsource(scraper).find(req) for req in {"from urllib.request import", "import urllib.request"}} == {-1}, "Do not use urllib.request in scraper.py"
        super().__init__(daemon=True)
        
    def write_report(self) -> None:
        with open('report.txt','w') as report:
            report.write(f"Unique webpages: {len(scraper.Scraper.discovered_urls)}\n")
            report.write(f"longest page : {scraper.Scraper.longest_page[0]}, length of page: {scraper.Scraper.longest_page[1]}\n")
            sorted_common_words = sorted(scraper.Scraper.common_words.items(), key = lambda x : (-x[1], x[0]))
            for index in range(0, 50):
                report.write(f'Common Words: {sorted_common_words[index][0]}, Frequency: {sorted_common_words[index][1]}\n')
            sorted_subdomains = sorted(scraper.Scraper.subdomain_frequency.keys())
            report.write(f"Unique subdomains: {len(sorted_subdomains)}\n")
            report.write("Subdomains and frequencies:\n")
            for subdomain in sorted_subdomains:
                report.write(f'{subdomain}, {scraper.Scraper.subdomain_frequency[subdomain]}\n')
               
        
        
    def run(self):
        test_counter = 0 # TEMP
        while True:
            tbd_url = self.frontier.get_tbd_url()
            print('next seed: ', tbd_url)
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                break
            
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = self.worker_scraper.scrape(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
            test_counter += 1 # TEMP
            if test_counter >= 20:
                break
        self.write_report()
            
