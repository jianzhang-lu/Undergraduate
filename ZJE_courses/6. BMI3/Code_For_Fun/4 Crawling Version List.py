import re
def CrawlVersion(text):
    pattern = re.compile(r'<Key>([\d|\.]+)/')
    versions = pattern.findall(text)
    result = []
    for version in versions:
        if version not in result:
            result.append(version)
    return result


