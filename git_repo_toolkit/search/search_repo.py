"""

REST API endpoints for search: https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28#search-code

A Whole New Code Search: https://github.com/search/advanced
Blog: https://github.blog/news-insights/product-news/a-whole-new-code-search/

"""
import os

import requests

from git_repo_toolkit.constants import SEARCH_OUTPUT_FILE_NAME, SEARCH_OUTPUT_CSV_FILE_NAME
from git_repo_toolkit.utils.file_utils import save_in_file

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ORG_NAME = os.getenv('ORG_NAME')
SEARCH_QUERY = os.getenv('SEARCH_QUERY')
SEARCH_API_URL = 'https://api.github.com/search/code'

headers = {
    'Accept': 'application/vnd.github+json',
    # 'Accept': 'application/vnd.github.text-match+json',
    'Authorization': f'Bearer {GITHUB_TOKEN}',
    'X-GitHub-Api-Version': '2022-11-28'
}


def search_code_in_repos(query):

    url = f'{SEARCH_API_URL}?q={query}'
    all_items = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json()
        all_items.extend(result['items'])
        url = result.get('next', None)
    return all_items


query_string = f'org:{ORG_NAME} extension:py "{SEARCH_QUERY}"'
results = search_code_in_repos(query_string)
repositories = {item['repository']['full_name']: item for item in results}

repos_dictionary = {}
for key, repo in repositories.items():
    repos_dictionary[f"'{key.split('/')[-1]}'"] = repo

print(f"search count: {len(results)}")
print(f"repos count: {len(repos_dictionary.keys())}")

query_string = f'org:{ORG_NAME} extension:py fork:true "{SEARCH_QUERY}"'
results = search_code_in_repos(query_string)
repositories = {item['repository']['full_name']: item for item in results}

for key, repo in repositories.items():
    repos_dictionary[f"'{key.split('/')[-1]}'"] = repo

print(f"forked repos search count: {len(results)}")
print(f"Updated repos count: {len(repos_dictionary.keys())}")

output_string = ', '.join(repos_dictionary.keys())
print("-------")
print("Output:")
print("-------")
print(output_string)

save_in_file(SEARCH_OUTPUT_FILE_NAME, output_string)

output_string = "repo, repo_url, searched_file_url\n"
for key, repo in repos_dictionary.items():
    stripped_key = key.strip("'")
    output_string += (f"{stripped_key}"
                      f",{repo['repository']['html_url']}"
                      f",{repo['html_url']}"
                      f"\n")
save_in_file(SEARCH_OUTPUT_CSV_FILE_NAME, output_string)
