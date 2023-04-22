import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class Scraper:
    def __init__(self):
        self.discovered_urls = {}
    
    def scrape(self, url, resp):
        links = self.extract_next_links(url, resp) #list of possilbe url paths
        
        return [link for link in links if self.is_valid(link)] #returns valid url paths that havent been seen yet

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
        #https://www.ics.uci.edu,https://www.cs.uci.edu,https://www.informatics.uci.edu,https://www.stat.uci.edu
        soup = BeautifulSoup(resp.raw_response.text, 'html.parser') # soup object
        for anchor in soup.find_all('a', href=True): #for loop that iterates through a list of all <a href = URL>
            if re.match(r'^\/*(https:|http:)?\/\/(www\.)(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu)\b([-a-zA-Z0-9()@:%+.~#?&\/\/=_]*)?$', anchor.get('href', '/')): 
                if re.match(r'^.*https?.*$', anchor.get('href', '/')):
                    curr = anchor.get('href', '/')
                    print(curr)
                    self.discovered_urls.add(curr) # add to discovered set
                else:
                    curr = "https:"+ anchor.get('href', '/')
                    print(curr)
                    self.discovered_urls.add(curr) # add to discovered set
            else:
                #if(wrong site then dont do anything)
                relative = anchor.get('href', '/')
                if (re.match(r'www\.', relative) or re.match(r'https?', relative) or re.match(r'\/\/', relative[0:2])) and not (re.match(r'^\/*(https:|http:)?\/\/(www\.)(ics\.uci\.edu|cs\.uci\.edu|informatics\.uci\.edu|stat\.uci\.edu)\b([-a-zA-Z0-9()@:%+.~#?&\/\/=_]*)?$', relative)):
                    continue
                elif relative[0] == '/':
                    relative = relative[1:]
                try:
                    if curr[-1] != '/':
                        curr += '/'
                    print(curr + relative)
                    self.discovered_urls.add(curr + relative) # add to discovered set
                except:
                    if url[-1] != '/':
                        url += '/'
                    print(url + relative)
                    self.discovered_urls.add(curr + relative) # add to discovered set
        return list()

    def is_valid(self, url):
        # Decide whether to crawl this url or not. 
        # If you decide to crawl it, return True; otherwise return False.
        # There are already some conditions that return False.
        try:
            if url not in self.discovered_urls:
            
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
