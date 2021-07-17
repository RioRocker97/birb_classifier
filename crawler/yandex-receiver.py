import json
import sys

from bs4 import BeautifulSoup
import requests

yandex_base_url="https://yandex.com/images/search?from=tabbar&text="

def retrieve_image_url(input_keyword,output_file):
    # Issue: Yandex keep blocking, unable to retrieve all the images
    response = requests.get(yandex_base_url+input_keyword)
    response_html = response.text
    
    if "Please confirm that you and not a robot are sending requests" in response_html:
        print("Yandex is blocking the request.")
        return False

    parsed_html = BeautifulSoup(response_html,features="html.parser")
    print("Image found: {}".format(len(parsed_html.find_all("div", {"class": "serp-item_type_search"}))))
    with open(output_file,"w+") as o_file:
        for img in parsed_html.find_all("div", {"class": "serp-item_type_search"}):
            data = json.loads(img["data-bem"])
            o_file.write(data["serp-item"]["preview"][0]["url"] + "\n")
    return True

if __name__ == '__main__':
    input_keyword = sys.argv[1]
    output_file = sys.argv[2]
    is_crawled = retrieve_image_url(input_keyword,output_file)
    print("Pulling {} into {} with status: {}".format(input_keyword,output_file,is_crawled))