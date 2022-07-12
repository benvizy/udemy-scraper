from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time
import pandas as pd


granular_df = pd.DataFrame(columns=['Section #','Module Title','Time'])
print(granular_df)


# Establish Constants (drivers, etc)
driverPath = "/YOUR DRIVER PATH"
driver = webdriver.Chrome(executable_path=driverPath)
# email = "your-email"
# passy = "your-password"


# URL to scrape
classURL = "https://www.udemy.com/course/the-complete-web-development-bootcamp/"

# Open Window
driver.get(classURL)



# Necessary functions
def inch_up(body):
    for _ in range(10):
        body.send_keys(Keys.UP)

def inch_down(body):
    for _ in range(10):
        body.send_keys(Keys.DOWN)


# Constants & classes
module_title_class = "section--section-title--8blTh"
module_time_class = "section--section-content--9kwnY"

mod_item_title_class = "section--item-title--2k1DQ"
mod_item_time_class = "section--item-content-summary--126oS"

# Click See More if it exists
try:
    see_more = driver.find_element_by_class_name("curriculum--show-more--2tshH")
    see_more.click()
except:
    pass

body = driver.find_element_by_css_selector('body')

# Get List of Sections

module_title_objects = driver.find_elements_by_class_name(module_title_class)
module_time_objects = driver.find_elements_by_class_name(module_time_class)

titles = [title.text for title in module_title_objects]
title_times = [time.text for time in module_time_objects]


# Get Data from First Section

mod_item_title_objects = driver.find_elements_by_class_name(mod_item_title_class)
mod_item_time_objects = driver.find_elements_by_class_name(mod_item_time_class)

section_titles = [title.text for title in mod_item_title_objects]
section_times = [time.text for time in mod_item_time_objects]

section_content = [dict(zip(section_titles, section_times))]
time.sleep(1)
driver.execute_script("arguments[0].scrollIntoView();", module_title_objects[0])
inch_up(body)
time.sleep(1)
module_title_objects[0].click()


time.sleep(1)

print(f'there are {len(titles)} sections')

# Click open, get data, Click Closed, repeat

for i in range(1, len(titles)):
    # Open the new section
    try:
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView();", module_title_objects[i])
        time.sleep(1)
        inch_up(body)
        time.sleep(1)
        module_title_objects[i].click()

        section_titles = [title.text for title in mod_item_title_objects]
        section_times = [time.text for time in mod_item_time_objects]
        new_section = dict(zip(section_titles, section_times))
        time.sleep(1)

        module_title_objects[i].click()

        section_content.append(new_section)
        print(f'appended section {i+1}!')
    except:
        pass

driver.quit()

pprint(section_content)

holistic_df = pd.DataFrame(dict(zip(titles, title_times)).items())
holistic_df.to_csv('section-table.csv')




granular_df = pd.DataFrame(columns=['Section #','Module Title','Time'])

i = 1
for content in section_content:

    content_titles = []
    content_times = []
    section_number = []

    for (key, value) in content.items():
        content_titles.append(key)
        content_times.append(value)
        section_number.append(i)

    c_title_series = pd.Series(content_titles)
    c_time_series = pd.Series(content_times)
    section_number_series = pd.Series(section_number)

    frame = {'Section #': section_number_series, 'Module Title': c_title_series, 'Time': c_time_series}

    new_df = pd.DataFrame(frame)

    # print(new_df)

    granular_df = pd.concat([granular_df, new_df], axis=0, join='outer', ignore_index=True)

    # print(granular_df)

    i += 1

granular_df.to_csv('granule-table.csv')
