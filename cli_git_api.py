from github import Github, GithubException, UnknownObjectException, RateLimitExceededException
import sys
import argparse
import re


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', nargs='?')
    return parser


parser = createParser()
namespace = parser.parse_args()

if not namespace.repository:
    print('Укажите ссылку либо имя репозитория')
    sys.exit()
if namespace.repository == '1':
    namespace.repository = 'https://github.com/Vi-812/git_check_alive'

adress = re.search('([^/]+/[^/]+)$', namespace.repository)
if adress:
    adress = adress.group(1)
if not adress:
    print('Ссылка не корректна, введите ссылку в формате')
    print('"https://github.com/Vi-812/GIT" либо "Vi-812/GIT"')
    sys.exit()

try:
    g = Github()
    repo = g.get_repo(adress)
    print(f'Наименование: {repo.name}')
    print(f'Описание: {repo.description}')
    print(f'Рейтинг: {repo.stargazers_count}')

    open_issues = repo.get_issues(state='open')   # closed
    count_issues = count_bug_issues = 0
    for issu in open_issues:
        print(issu)
        if 'bug' in issu.labels:
            print('11')

    labels = repo.get_labels()
    for label in labels:
        print(label)




except UnknownObjectException as error:
    print('Указанного вами репозитория не существует')
    print(error.__class__)
    print(error)

except RateLimitExceededException as error:
    print('Превышен лимит запросов, попробуйте повторить через некоторое время')
    print(error.__class__)
    print(error)

except GithubException as error:
    print('Ошибка PyGithub')
    print(error.__class__)
    print(error.__context__)
    print('-----------------')
    print(error)

except Exception as error:
    print('Неизвестная ошибка')
    print(error.__class__)
    print(error.__context__)
    print('-----------------')
    print(error)

