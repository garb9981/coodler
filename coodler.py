import urllib.request
from time import sleep
from random import uniform
import requests



PAGE_WAIT_TIME = 2.0
POST_WAIT_TIME = 2.0
DL_WAIT_TIME = 2.0
MAX_DIFF = 1.0

def download(url, video_num, name_length=10, num_tries=10):
    print("Downloading " + url + "...")
    name = str(video_num).zfill(4) + '.' +  url.split(".")[-1]
    for i in range(num_tries):
        try:
            sleep(DL_WAIT_TIME + uniform(-MAX_DIFF, MAX_DIFF))
            r = requests.get(url, allow_redirects=True, stream=True)
        except requests.exceptions.RequestException as _:
            print("Download error, trying again ("+str(i+1)+" of "+str(num_tries)+")")
            continue
        break
    open(name, "wb").write(r.content)


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
done_posts = []
url = input("URL: ").split("?")[0]
page_num = 0
video_num = 1

while True:
    page_url = url + "?o=" + str(page_num)
    sleep(PAGE_WAIT_TIME + uniform(-MAX_DIFF, MAX_DIFF))
    request =  urllib.request.Request(page_url, headers=headers)
    response = str(urllib.request.urlopen(request).read())
    posts = response.split("/post/")
    post_prefix = "https://coomer.su" + posts[0].split("\"")[-1]
    posts.pop(0)

    for post in posts:
        post_url = post_prefix + "/post/" + post.split("\"")[0]
        if post_url in done_posts:
            break
        done_posts.append(post_url)
        sleep(POST_WAIT_TIME + uniform(-MAX_DIFF, MAX_DIFF))
        post_request =  urllib.request.Request(post_url, headers=headers)
        post_response = str(urllib.request.urlopen(post_request).read())
        video_links = post_response.split("type=\"video/")
        if len(video_links) < 2: 
            continue
        video_links.pop()
        for video_link in video_links:
            video_link = video_link.split("src=\"")[-1].split("\"")[0]
            download(video_link, video_num)
            video_num += 1
    else:
        page_num += 50
        continue
    break
