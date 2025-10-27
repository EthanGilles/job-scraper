from .stripe import scrape_stripe
from .plaid import scrape_plaid
from .digitalocean import scrape_digitalocean
from .atlassian import scrape_atlassian
from .datadog import scrape_datadog
from .databricks import scrape_databricks
from .visa import scrape_visa

SCRAPERS = {
    "stripe": scrape_stripe,
    "plaid": scrape_plaid,
    "digitalocean": scrape_digitalocean,
    "atlassian": scrape_atlassian,
    "datadog": scrape_datadog,
    "databricks": scrape_databricks,
    "visa": scrape_visa,
}
