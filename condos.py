
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import pandas

# define chrome as our browser
browser = webdriver.Chrome('\\Users\\mpric\\OneDrive\\Desktop\\dev\\Projects\\condo_scraper\\chromedriver')
condo_site = 'https://condos.ca/toronto/condos-for-sale?beds=2-2&size_range=600%2C700&sale_price_range=450000%2C750000&sublocality_id=14%2C20%2C19%2C21%2C22'
maps = 'https://www.google.com/maps/dir/Wellesley+Station,+16+Wellesley+St+E,+Toronto,+ON+M4Y+1G2//@43.665219,-79.4188081,13z/data=!4m9!4m8!1m5!1m1!1s0x882b34b3ade5b6f3:0x7b2bbc3a99a3317!2m2!1d-79.3837889!2d43.6651623!1m0!3e2'

def get_condo_data():
    browser.get(condo_site)
    # let page load
    time.sleep(10)
    # make empty list
    lst = []

    # search for listings
    search = browser.find_element_by_id("listContainer")
    listings = search.find_elements_by_class_name("styles___PreviewContent-sc-54qk44-3.hkTzfk")

    #print(listings[0].text)
    for listing in listings:
    # add listing to lst
        lst.append(listing.text)
    # close the browser
    # check the length of list
    print(len(lst))

    # write data to csv file
    with open('condos.csv', 'w', newline='') as condos:
        writer = csv.writer(condos)
        writer.writerow(['price', 'unit', 'address', 'specifications', 'maintenance', 'mls', 'broker'])
        for item in lst:
            price, addresses, specifications, maintenance, mls, broker = item.split('\n')
            for x in addresses:
                unit, address = addresses.split('-')
            writer.writerow([price, unit, address, specifications, maintenance, mls, broker])
        condos.close()

def condo_distance():
    # open google maps
    browser.get(maps)
    time.sleep(10)
    # open df
    df = pandas.read_csv('condos.csv')
    # create list of addresses
    lst = df['address']
    #print(lst)
    # loop through list adding to google maps
    distances = []
    for address in lst:
        elem = browser.find_element_by_xpath('//*[@id="sb_ifc51"]/input')
        elem.clear()
        elem.send_keys(str(address))
        elem.send_keys(Keys.RETURN)
        time.sleep(3)
        details = browser.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[5]/div[1]/div/div[3]/div[4]/button')
        details.click()
        time.sleep(3)
        distance = browser.find_element_by_xpath('/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[3]/div[1]/h1/span[1]/span[2]/span')
        distances.append(distance.text)
        #print(distance.text)                             
        back = browser.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[1]/button')
        back.click()
    df['distance'] = distances
    df.to_csv('C:\\Users\\mpric\\OneDrive\\Desktop\\dev\\Projects\\condo_scraper\\condos.csv')
get_condo_data()
condo_distance()