import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


class Scraper:
    
    allowed_domains = {"www.ics.uci.edu", "www.cs.uci.edu" ,"www.informatics.uci.edu", "www.stat.uci.edu"}
    discovered_urls = set()
    longest_page = tuple() # (page name, length)
    common_words = dict() # {word:times seen}
    @staticmethod
    def is_valid(url):
        # Decide whether to crawl this url or not. 
        # If you decide to crawl it, return True; otherwise return False.
        # There are already some conditions that return False.
        try:
            if url not in Scraper.discovered_urls and url:
                try:
                    parsed = urlparse(url)
                    if parsed.scheme not in set(["http", "https"]):
                        return False
                    return not re.match(
                        r".*\.(css|js|bmp|gif|jpe?g|ico"
                        + r"|png|tiff?|mid|mp2|mp3|mp4"
                        + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
                        + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
                        + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
                        + r"|epub|dll|cnf|tgz|sha1"
                        + r"|thmx|mso|arff|rtf|jar|csv"
                        + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

                except TypeError:
                    print ("TypeError for ", parsed)
                    raise
        except Exception as e:
            print(e)
            
    def __init__(self):
        pass
    
    def scrape(self, url, resp):
        to_frontier_list = []
        links = self.extract_next_links(url, resp) #list of possilbe url paths
        for link in links:

            if self.is_valid(link):
                Scraper.discovered_urls.add(link)
                to_frontier_list.append(link)
        return to_frontier_list #returns valid url paths that havent been seen yet

    def extract_next_links(self, url, resp):
        # Implementation required.
        # url: the URL that was used to get the page
        # resp.url: the actual url of the page
        # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
        # resp.error: when status is not 200, you can check the error here, if needed.
        # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
        #         resp.raw_response.url: the url, again
        #         resp.raw_response.content: the content of the page!
        # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
        ret_link = []
        if resp and resp.status == 200:
            soup = BeautifulSoup(resp.raw_response.text, 'html.parser') # soup object
            # words = re.findall("[a-zA-Z0-9]+", soup.get_text().strip()) #n for each line, iterates through each character
            # for word in words:                
                # print("|", word.lower(), "|", sep='')
            for link in soup.find_all('a', href=True):
                new_link = urljoin(resp.url, link.get('href'), allow_fragments=False)
                if re.match(r"^(www\.).*(ics|cs|informatics|stat)\.uci\.edu$", urlparse(new_link).netloc):
                    pound_ind = new_link.find('#')
                    if pound_ind != -1:
                        new_link = new_link[:pound_ind]
                    ret_link.append(new_link)
        return ret_link

