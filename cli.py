import sys
import os
import argparse
import analytical.github_api_client as ga
from dotenv import load_dotenv
from req_response import resp_json

load_dotenv()

token = os.getenv("TOKEN")

try:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_path", nargs="?")
    namespace = parser.parse_args()
except Exception:
    print("An error occurred, too many arguments were passed")
    print('Pass the link or "owner/repository_name" as an argument')
    print('"https://github.com/Vi-812/git_check_alive" or "vi-812/git_check_alive"')
    sys.exit()

if not namespace.repository_path:
    print('Pass the link or "owner/repository_name" as an argument')
    print('"https://github.com/Vi-812/git_check_alive" or "vi-812/git_check_alive"')
    sys.exit()

instance_g_a_c = ga.GithubApiClient(token)
instance_g_a_c.get_new_report(namespace.repository_path)

print(resp_json.repository_info.name)
print(resp_json.json())
