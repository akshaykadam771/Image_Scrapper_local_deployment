from flask import Flask, render_template, request
import os
import shutil
import time
import requests
from selenium import webdriver

app = Flask(__name__) # initialising the flask app with the name 'app'




@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html')


@app.route('/searchImages', methods=['GET','POST'])
def searchImages():
    if request.method == 'POST':
        print("entered post")
        keyWord = request.form['keyword'] # assigning the value of the input keyword to the variable keyword

    else:
        print("did not enter post")
    print('printing = ' + keyWord)

    def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
        target_folder = os.path.join(target_path, '_'.join(
            search_term.lower().split(' ')))  # make the folder name inside images with the search string

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)  # make directory using the target path if it doesn't exist already

        with webdriver.Chrome(executable_path=driver_path) as wd:
            res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

        counter = 0
        for elem in res:
            persist_image(target_folder, elem, counter)
            counter += 1

    def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
        def scroll_to_end(wd):
            wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_between_interactions)

            # build the google query

        search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

        # load the page
        wd.get(search_url.format(q=query))

        image_urls = set()
        image_count = 0
        results_start = 0
        while image_count < max_links_to_fetch:
            scroll_to_end(wd)

            # get all image thumbnail results
            thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
            number_results = len(thumbnail_results)

            print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

            for img in thumbnail_results[results_start:number_results]:
                # try to click every thumbnail such that we can get the real image behind it
                try:
                    img.click()
                    time.sleep(sleep_between_interactions)
                except Exception:
                    continue

                # extract image urls
                actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
                for actual_image in actual_images:
                    if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                        image_urls.add(actual_image.get_attribute('src'))

                image_count = len(image_urls)

                if len(image_urls) >= max_links_to_fetch:
                    print(f"Found: {len(image_urls)} image links, done!")
                    break
            else:
                print("Found:", len(image_urls), "image links, looking for more ...")
                time.sleep(30)
                return
                load_more_button = wd.find_element_by_css_selector(".mye4qd")
                if load_more_button:
                    wd.execute_script("document.querySelector('.mye4qd').click();")

            # move the result startpoint further down
            results_start = len(thumbnail_results)

        return image_urls

    def persist_image(folder_path: str, url: str, counter):
        try:
            image_content = requests.get(url).content

        except Exception as e:
            print(f"ERROR - Could not download {url} - {e}")

        try:
            f = open(os.path.join(folder_path, str(keyWord) + "_" + str(counter) + ".jpg"), 'wb')
            f.write(image_content)
            f.close()
            print(f"SUCCESS - saved {url} - as {folder_path}")
        except Exception as e:
            print(f"ERROR - Could not save {url} - {e}")

    DRIVER_PATH = './chromedriver'
    search_term = keyWord
    # num of images you can pass it from here  by default it's 10 if you are not passing
    # number_images = 10
    search_and_download(search_term=search_term, driver_path=DRIVER_PATH)  # method to download


    def list_only_jpg_files(folder_name):
        list_of_jpg_files=[]
        list_of_files=os.listdir(folder_name)
        print('list of files==')
        print(list_of_files)
        for file in list_of_files:
            name_array= file.split('.')
            if(name_array[1]=='jpg'):
                list_of_jpg_files.append(file)
            else:
                print('filename does not end withn jpg')
        return list_of_jpg_files


    def delete_existing_image(list_of_images):
        for image in list_of_images:
            try:
                os.remove("./static/pics/"+image)
            except Exception as e:
                print('error in deleting:  ',e)
        return 0

    static_pics = list_only_jpg_files('./static/pics')

    delete_existing_image(static_pics)

    destination = './static/pics/'
    location = '_'.join(keyWord.lower().split(' '))
    target_keyword = './images/' + str(location)
    target_lis = list_only_jpg_files(target_keyword)

    for data in target_lis:
        target = './images/' + str(location) + '/' + str(data)
        shutil.copy(target, destination)

    images_list = os.listdir("./static/pics")
    image_folder = os.path.join('static', 'pics')
    app.config['UPLOAD_FOLDER'] = image_folder


    image_1 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[0])
    image_2 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[1])
    image_3 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[2])
    image_4 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[3])
    image_5 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[4])
    image_6 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[5])
    image_7 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[6])
    image_8 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[7])
    image_9 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[8])
    image_10 = os.path.join(app.config['UPLOAD_FOLDER'], images_list[9])


    return render_template("showing_images.html", image_name1=image_1,image_name2=image_2,image_name3=image_3,image_name4=image_4,image_name5=image_5,image_name6=image_6,image_name7=image_7,image_name8=image_8,image_name9=image_9,image_name10=image_10)







if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000) # port to run on local machine

