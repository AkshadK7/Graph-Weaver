from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
from neo4j import GraphDatabase
import datetime

class WebScraperGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, name, url):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.driver.session() as session:
            session.run("""
                MERGE (n:WebPage {name: $name, url: $url, current_date: $current_date})
                """, name=name, url=url, current_date=current_date)

    def create_relationship(self, parent_url, child_url):
        with self.driver.session() as session:
            session.run("""
                MATCH (parent:WebPage {url: $parent_url})
                MATCH (child:WebPage {url: $child_url})
                MERGE (parent)-[:HAS_CHILD]->(child)
                """, parent_url=parent_url, child_url=child_url)

    def scrape_and_build_graph(self, start_url):
        visited = set()
        root_domain = urlparse(start_url).netloc

        def scrape_links(url):
            if url in visited:
                return []

            visited.add(url)
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                self.create_node(name=urlparse(url).path or "Home", url=url)

                links = set()
                for a_tag in soup.find_all('a', href=True):
                    link = urljoin(url, a_tag['href'])
                    if urlparse(link).netloc == root_domain:
                        links.add(link)

                return links
            except Exception as e:
                print(f"Failed to scrape {url}: {e}")
                return []

        def build_graph_recursive(url):
            child_links = scrape_links(url)
            for child_url in child_links:
                self.create_node(name=urlparse(child_url).path or "Child", url=child_url)
                self.create_relationship(parent_url=url, child_url=child_url)
                build_graph_recursive(child_url)

        build_graph_recursive(start_url)

# Example usage
if __name__ == "__main__":
    # Connect to Neo4j (make sure your Neo4j server is running and credentials are correct)
    neo4j_uri = "bolt://localhost:7687"
    neo4j_user = "neo4j"
    neo4j_password = "password"  # Replace with your password

    scraper = WebScraperGraph(neo4j_uri, neo4j_user, neo4j_password)

    try:
        start_url = "https://example.com"  # Replace with the URL you want to scrape
        scraper.scrape_and_build_graph(start_url)
    finally:
        scraper.close()
