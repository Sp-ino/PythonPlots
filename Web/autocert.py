#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 19:14:14 2021

@author: spino
"""

from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt


def main():
    #chromedriver_path = "/home/spino/Downloads/chromedriver"   #If one prefers to use chromium/chrome
    #driver = wd.Chrome(chromedriver_path)
    
    google_site = 'https://docs.google.com/forms/d/e/1FAIpQLSdAG_KegcP-AIyDqb875yaFw3dd9xn8k65zDTOXsjtIoLTFKQ/viewform'
    sapienza_site = 'https://login.uniroma1.it/SSOLoginUniN/ProcessResponseServlet?SAMLRequest=fVLLTsMwELwj8Q%2BW70magASymqACQlTiEdGUAzfH2aSmjjd4nRb%2BnjQFAQd6Hc%2FOY73Ti%2FfWsA040mhTHocTzsAqrLRtUr4sboJzfpEdH01JtqYTs96v7BO89UCeDZOWxPiQ8t5ZgZI0CStbIOGVWMzu70QSTkTn0KNCw9n8OuUSEMuuqqvG1utGrxtZtg0arKrSlJ2Sxq7W%2BFqvOHv%2BjpXsYs2Jephb8tL6AZokcRAnQXxSJImIz8Tp5IWz%2FMvpUtt9g0Oxyj2JxG1R5EH%2BuChGgY2uwD0M7JQ3iI2BUGG7s88lkd4McC0NAWczInB%2BCHiFlvoW3ALcRitYPt2lfOV9RyKKtttt%2BCMTyai32mEr41D7SCri2bhaMbZzv3Z6OLv89ubZj%2Fo0%2BiWVfX3Zrsn8Okej1QebGYPbKwfSDzW864cWN%2Bha6f93i8N4RHQV1CNV9JY6ULrWUHEWZXvXv7cxXMwn&RelayState=https%3A%2F%2Faccounts.google.com%2FCheckCookie%3Fcontinue%3Dhttps%253A%252F%252Fdocs.google.com%252Fforms%252Fd%252Fe%252F1FAIpQLSdAG_KegcP-AIyDqb875yaFw3dd9xn8k65zDTOXsjtIoLTFKQ%252Fviewform%26service%3Dwise%26ltmpl%3Dforms%26ifkv%3DAU9NCcx62hSVxLlkGekIx3XI9KFlvRR4MEQ5TxhlH7-MFhegXG7nWuNx3Myimq31Xy_7uGYM4ckZMQ'
    
    
    #read credentials from file
    with open("/home/spino/.sapaccess", 'r') as reader:
        credentials = reader.readlines()
    
    
    #get info that will be used to fill the form
    email = credentials[0]
    pw = credentials[1]
    name = credentials[2]
    surname = credentials[3]
    date = dt.now()
    day = date.day
    month = date.month
    year = date.year
    
    
    #set variables with xpath
    google_login = '//*[@id="identifierId"]'
    google_continue = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/span'
    sapienza_login = '//*[@id="username"]'
    sapienza_pw = '//*[@id="password"]'
    sapienza_continue = '/html/body/div[1]/div/div[2]/div/div/div/div[2]/form/table/tbody/tr[3]/td[2]/input'
    gform_continue = '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
    gform_faculty_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[1]/span'
    gform_faculty = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[8]'
    gform_name = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    gform_surname = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    gform_building_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div[1]/div[1]/span'
    gform_building = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[90]/span'
    gform_hour_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div[1]/div[1]'
    gform_hour = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[6]/span'
    gform_day = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div/div[1]/input'
    gform_month = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[3]/div/div[2]/div[1]/div/div[1]/input'
    gform_year = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div/div[5]/div/div[2]/div[1]/div/div[1]/input'
    gform_consent = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[9]/div/div/div[2]/div[1]/div/label/div/div[1]/div[2]'
    gform_enter = '/html/body/div[1]/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span'
    
    
    #start driver
    driver = wd.Firefox()   #start driver
    
    
    #-------------------------------------Perform actions--------------------------
    #specify google email address
    driver.get(google_site)
    driver.find_element(by = 'xpath', value = google_login).send_keys(email)
    google_continue_element = driver.find_element('xpath', google_continue)
    driver.execute_script("arguments[0].click();", google_continue_element)
    
    #sign in with sapienza account
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', sapienza_login))).send_keys(email)
    driver.find_element(by = 'xpath', value = sapienza_pw).send_keys(pw)
    sapienza_continue_element = driver.find_element('xpath', sapienza_continue)
    driver.execute_script("arguments[0].click();", sapienza_continue_element)
    
    #continue to the actual form
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', gform_continue)))
    gform_continue_element = driver.find_element('xpath', gform_continue)
    driver.execute_script("arguments[0].click();", gform_continue_element)
    
    #send name and surname
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', gform_name))).send_keys(name)
    driver.find_element(by = 'xpath', value = gform_surname).send_keys(surname)
    
    #choose faculty
    gform_faculty_menu_element = driver.find_element('xpath', gform_faculty_menu)
    driver.execute_script("arguments[0].click();", gform_faculty_menu_element)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', gform_faculty))).click()
    
    #choose hour
    gform_hour_menu_element = driver.find_element('xpath', gform_hour_menu)
    driver.execute_script("arguments[0].click();", gform_hour_menu_element)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', gform_hour))).click()
    
    #choose building
    gform_building_menu_element = driver.find_element('xpath', gform_building_menu)
    driver.execute_script("arguments[0].click();", gform_building_menu_element)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(('xpath', gform_building))).click()
    
    #send day, month, year
    driver.find_element(by = 'xpath', value = gform_day).send_keys(day)
    driver.find_element(by = 'xpath', value = gform_month).send_keys(month)
    driver.find_element(by = 'xpath', value = gform_year).send_keys(year)
    
    #give consent
    gform_consent_element = driver.find_element('xpath', gform_consent)
    driver.execute_script("arguments[0].click();", gform_consent_element)
    
    #enter
    gform_enter_element = driver.find_element('xpath', gform_enter)
    driver.execute_script("arguments[0].click();", gform_enter_element)
    #------------------------------------------------------------------------------
    
    
if __name__ == "__main__":
    main()