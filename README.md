# Graph Weaver

A Python application to recursively crawl websites, extract internal links, and build a hierarchical graph representation of the site structure using Neo4j. Each webpage is modeled as a node with metadata, and child links are represented as relationships, enabling visualization and analysis of website connectivity.

## Features

- Recursively crawls websites and identifies all internal links.
- Filters out external links and focuses on the same root domain.
- Builds a hierarchical graph in Neo4j with nodes representing webpages.
- Nodes include metadata: `name`, `url`, and `current_date`.
- Relationships between nodes are represented as `HAS_CHILD`.

## Requirements

- Python 3.7+
- Neo4j (Community or Enterprise Edition)
- Libraries: `beautifulsoup4`, `requests`, `neo4j`

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/graph-weaver.git
    cd graph-weaver
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Neo4j:
    - Install and run Neo4j.
    - Create a database and note the connection credentials.

4. Update the script:
    - Modify the `neo4j_uri`, `neo4j_user`, and `neo4j_password` in the script to match your setup.

## Usage

1. Run the script with a starting URL:
    ```bash
    python web_scraper_graph.py
    ```
2. Replace the `start_url` variable in the script with your desired root URL to crawl.

## Example

For a starting URL `https://example.com`, Graph Weaver will:
- Crawl all pages within `example.com`.
- Build a Neo4j graph where:
  - Each page is a node with properties (`name`, `url`, `current_date`).
  - Links between pages are represented by `HAS_CHILD` relationships.

## Graph Model in Neo4j

- **Nodes**: Represent webpages with properties:
  - `name`: Path or identifier of the page.
  - `url`: Full URL of the page.
  - `current_date`: Date when the node was created.
- **Relationships**:
  - `HAS_CHILD`: Represents links between pages.

## Contributing

Contributions are welcome! Please fork the repository, create a branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Enjoy mapping the web with Graph Weaver! 🚀
