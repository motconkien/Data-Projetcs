from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


driver = webdriver.Safari()
driver.maximize_window()
url = 'https://www.coursera.org/courses?query=free&page=1'
driver.get(url)

#find links container
# href= ''
links_container = driver.find_elements(By.CLASS_NAME,value = 'cds-119.cds-113.cds-115.cds-CommonCard-titleLink.css-si869u.cds-142')
for link in links_container:
    link.click()
    base_url = link.get_attribute('href')

    driver.switch_to.window(driver.window_handles[-1])  # Switch to curent tab -> want to back: driver.switch_to.window(driver.window_handles[0])

    time.sleep(5)

    #create dict to save data
    data ={
            "title": None,
            "star": None,
            "unit":None,
            "total reviews": None,
            "level": None,
            "reviews": None
        }
    try:
        h1 = driver.find_element(by=By.TAG_NAME,value = 'h1').text
        # print(h1)
        img = driver.find_element(by=By.CLASS_NAME,value='css-1f9gt0j')
        unit = img.get_attribute('alt')
        # print(img.get_attribute('alt'))
        data['title'] = h1
        data['unit'] = unit
        star = driver.find_element(by=By.XPATH,value='//div[@class="cds-119 cds-Typography-base css-h1jogs cds-121"]').text
        # print(star)
        data['star'] = star

        total_reviews = driver.find_element(by=By.XPATH,value='//div/p[@class=" css-vac8rf"]').text.strip('(').strip(')')
        # print(total_reviews)
        data['total reviews'] = total_reviews

        level = driver.find_element(by=By.XPATH,value='//div[@class=" css-fk6qfz"]').text
        # print(level)
        data['level'] = level

        # review path. because reviews path when clicking in the same tab -> no need to switch
        review_url = base_url + '/reviews'
        driver.get(review_url)

        # Wait for the review page to load
        time.sleep(10)  #add time to load page

        # Extract review information
        review_container = driver.find_elements(By.CLASS_NAME, 'cds-9.css-o7qc23.cds-11.cds-grid-item.cds-80')
        reviews =[]
        for review in review_container:
            review_data = {
                "Starts": None,
                "Reviewer": None,
                "Date": None,
                "Content": None
            }
            try:
                star = review.find_elements(by=By.XPATH,value='//*[@id="rendered-content"]/div/div/div[1]/div[4]/div[2]/div[1]/div[1]/div[1]/div/span[1]')
                reviewer = review.find_element(By.CLASS_NAME, 'reviewerName').text
                date = review.find_element(By.CLASS_NAME, 'dateOfReview').text
                content = review.find_element(By.CLASS_NAME, 'css-140m8il').text
                review_data['Starts'] = len(star)
                review_data['Reviewer'] = reviewer
                review_data['Date'] = date
                review_data['Content'] = content
            except Exception as e:
                print(f"An error occurred: {e}")  
            finally:
                reviews.append(review_data)
        else:          
            data['reviews'] = reviews

    except Exception as e:
        print(f'An error occured: {e}')
    
    finally:
        with open('course.json','a') as file:
            json.dump(data,file,indent=4)
        print('Data written to course.json')
        driver.close()
    break
    
