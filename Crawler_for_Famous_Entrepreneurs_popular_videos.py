import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import random


if __name__ == '__main__':


    url_list = ["https://www.youtube.com/results?search_query=elon+musk","https://www.youtube.com/results?search_query=jack+dorsey",
                "https://www.youtube.com/results?search_query=bill+gates","https://www.youtube.com/results?search_query=marc+andreessen",
                "https://www.youtube.com/results?search_query=garyvee", "https://www.youtube.com/results?search_query=Reid+Hoffman",
                "https://www.youtube.com/results?search_query=jeff+bezos","https://www.youtube.com/results?search_query=naval+ravikant",
                "https://www.youtube.com/results?search_query=charlie+munger","https://www.youtube.com/results?search_query=mark+cuban",
                "https://www.youtube.com/results?search_query=sam+altman", "https://www.youtube.com/results?search_query=tim+cook",
                "https://www.youtube.com/results?search_query=Ben+Horowitz", "https://www.youtube.com/results?search_query=Lary+Page",
                "https://www.youtube.com/results?search_query=andrew+chen","https://www.youtube.com/results?search_query=Sergey+Brin",
                "https://www.youtube.com/results?search_query=masayoshi+son","https://www.youtube.com/results?search_query=steve+jobs",
                "https://www.youtube.com/results?search_query=ray+dalio","https://www.youtube.com/results?search_query=WARREN+BUFFETT",
                "https://www.youtube.com/results?search_query=justin+kan","https://www.youtube.com/results?search_query=RICHARD+BRANSON",
                "https://www.youtube.com/results?search_query=yuval+noah+harari","https://www.youtube.com/results?search_query=peter+thiel",
                "https://www.youtube.com/results?search_query=paul+graham","https://www.youtube.com/results?search_query=Vinod+Khosla",
                "https://www.youtube.com/results?search_query=brian+armstrong", "https://www.youtube.com/results?search_query=patrick+collison+","https://www.youtube.com/results?search_query=boyan+slat"
                ]
    #crawl these page and find the top 3 views and then randomly choose one to open


    try:
        # activate Webdriver
        driver = webdriver.Chrome(executable_path='chromedriver')
        driver.maximize_window()  # open the browser and maximize it
        driver.set_page_load_timeout(60)  # wait for 60s, which is safe
        url = random.choice(url_list)
        driver.get(url)  # go to the url
        time.sleep(30)

        split1 = url.split("=")
        wrong_name = split1[1]
        Name = wrong_name.replace("+"," ")

        soup = BeautifulSoup(driver.page_source, 'html5lib')
        all_videos = soup.find_all("ytd-video-renderer", "style-scope ytd-item-section-renderer")
        video_dict = {}
        for video in all_videos:
            view_num1 = video.find("span", "style-scope ytd-video-meta-block").text.replace("觀看次數：","") # "觀看次數" means "views" in Mandarin
            if "萬" in list(view_num1):
                if "." in list(view_num1):
                    view_num2 = view_num1.replace(".","")
                    Real_num = view_num2.replace("萬次", "") + "000" # "萬次" means "10000 times" in Mandarin
                else:
                    Real_num = view_num1.replace("萬次","") + "0000"
            else:
                Real_num = view_num1.replace("次", "") #"次"means "times" in Mandarin
            video_dict[Real_num] = "https://www.youtube.com/"+video.a["href"]

        new_list = []
        Top_3_video_list = []

        for a in video_dict.keys():
            new_list.append(int(a))

        new_list.sort(reverse=True)

        for view_num in new_list[0:3]:
            Top_3_video_list.append(view_num)

        print("Top 3 videos of",Name.title(),":")

        for i in Top_3_video_list:
            print(video_dict[str(i)])

        the_one = video_dict[str(random.choice(Top_3_video_list))]

        #print("Watch this: ", the_one)

        driver.get(the_one)  
        time.sleep(8)

        try:
            element = driver.find_element_by_class_name("ytp-ad-skip-button-container")
            print("Skipped the ad.")
            if element:
                element.click()
        except:
            print("No ads today.")


    finally:
        print("Watch this: ", the_one)
        driver.quit()
        soup = BeautifulSoup(driver.page_source, 'html5lib')
        title = soup.find("yt-formatted-string", "style-scope ytd-video-primary-info-renderer").text.strip()
        print("Now Playing：", title)
