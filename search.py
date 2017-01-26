from base64 import b64decode
from github.MainClass import Github

ignore_words = ('Mock', 'Test', '_test', 'test_', 'test/', 'tests/')


def is_interesting_result(result):
    for w in ignore_words:
        if w in result.path:
            return False
    return result.repository.stargazers_count > 20


def search(token, language, query, count):
    """Search popular repo's for code"""
    client = Github(token, user_agent='Sjord githubsearch')
    r = client.search_repositories(query='', sort='stars', order='desc', language=language, stars='>=100')
    for repo in r:
        print(repo.full_name)
        r = client.search_code(query, language=language, size='>=100', repo=repo.full_name)
        for search_result in r:
            if is_interesting_result(search_result):
                print('FILE:', search_result.repository.full_name, search_result.path)
                print(b64decode(search_result.content).decode('utf-8'))
                count -= 1
                if count == 0:
                    return


def search2(token, language, query, count):
    """Search popular repo's for code"""
    client = Github(token, user_agent='Sjord githubsearch')
    r = client.search_code(query, language=language, size='>=100')
    for search_result in r:
        if is_interesting_result(search_result):
            print('FILE:', search_result.repository.full_name, search_result.path)
            print(search_result.html_url)
            # print(b64decode(search_result.content).decode('utf-8'))
            count -= 1
            if count == 0:
                return




if __name__ == "__main__":
    with open('token.txt') as fp:
        token = fp.read().strip()

    search2(token, 'php', 'HTTP_X_FORWARDED_FOR', 20)
