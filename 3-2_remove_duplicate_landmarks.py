try:
    with open('crawling_data/website_addresses_for_landmarks.txt', 'rt') as f:
        landmark_urls = f.read().splitlines()
except FileNotFoundError:
    with open('3-1_crawl_website_addresses_for_landmarks.py', 'rt') as f:
        exec(f.read())

landmark_urls = list(set(landmark_urls))

with open('crawling_data/distinct_website_addresses_for_landmarks.txt', 'wt') as f:
    for landmark_url in landmark_urls:
        f.write('%s\n' % landmark_url)
