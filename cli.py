import sys
import os
import argparse
import analytical.github_api_client as ga
from dotenv import load_dotenv
import asyncio


async def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("repository_path", nargs="?")
        args = parser.parse_args()
    except Exception:
        print("An error occurred, too many arguments were passed")
        print('Pass the link or "owner/repository_name" as an argument')
        print('"https://github.com/Vi-812/git_check_alive" or "vi-812/git_check_alive"')
        sys.exit()

    if not args.repository_path:
        print('Pass the link or "owner/repository_name" as an argument')
        print('"https://github.com/Vi-812/git_check_alive" or "vi-812/git_check_alive"')
        sys.exit()

    await g_cli.get_new_report(args.repository_path)


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("APP_TOKEN")

    g_cli = ga.GithubApiClient(token)

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())
