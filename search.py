from base64 import b64decode
from github.MainClass import Github

ignore_words = ('Mock', 'Test', '_test')


def is_interesting_result(result):
    for w in ignore_words:
        if w in result.name:
            return False
    return True


def search(language, query, count):
    """Search popular repo's for code"""
    client = Github()
    r = client.search_repositories(query='', sort='stars', order='desc', language=language, stars='>=100')
    for repo in r:
        r = client.search_code(query, language=language, size='>=100', repo=repo.full_name)
        for search_result in r:
            if is_interesting_result(search_result):
                print('FILE:', search_result.repository.full_name, search_result.path)
                print(b64decode(search_result.content).decode('utf-8'))
                count -= 1
                if count == 0:
                    return


if __name__ == "__main__":
    search('php', 'session uniqid', 10)
