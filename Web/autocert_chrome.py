#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 14:59:01 2021

@author: cristian
"""


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt


date = dt.now()
day = date.day+7
month = date.month
year = date.year

gform_faculty_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[1]/div[1]/span'
gform_faculty = "//*[@id='mG61Hd']/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[2]/div[8]/span"
gform_name = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
gform_surname = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
gform_building_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div[1]/div[1]/span'
gform_building = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[2]/div[90]/span'
gform_hour_menu = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div[1]/div[1]'
gform_hour = '/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[2]/div[6]/span'
gform_consent = '/html/body/div[1]/div[2]/form/div[2]/div/div[2]/div[9]/div/div/div[2]/div[1]/div/label/div/div[1]/div[2]'
gform_enter = '/html/body/div[1]/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div[2]/span/span'

option = webdriver.ChromeOptions()
#option.add_argument("-incognito")
# option.add_argument("--headless")
# option.add_argument("disable-gpu")
option.add_argument("user-data-dir=/home/cristian/.config/google-chrome/Default");
browser = webdriver.Chrome(executable_path='/home/cristian/PhD/autocertificazioni/chromedriver', options=option)
browser.get("https://docs.google.com/forms/d/e/1FAIpQLSdAG_KegcP-AIyDqb875yaFw3dd9xn8k65zDTOXsjtIoLTFKQ/viewform")
firstnextbutton=browser.find_element(By.XPATH, "//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div[1]/span")
firstnextbutton.click()
secondtext=browser.find_elements(By.CLASS_NAME,"quantumWizTextinputPaperinputInput")
secondtext[0].send_keys("cristian")
secondtext[1].send_keys("bocciarelli")


gform_faculty_menu_element = browser.find_element('xpath', gform_faculty_menu)
browser.execute_script("arguments[0].click();", gform_faculty_menu_element)
WebDriverWait(browser, 20).until(EC.element_to_be_clickable(('xpath', gform_faculty))).click()




secondtext[2].send_keys(month)
secondtext[2].send_keys(day)
secondtext[2].send_keys(year)

gform_hour_menu_element = browser.find_element('xpath', gform_hour_menu)
browser.execute_script("arguments[0].click();", gform_hour_menu_element)
WebDriverWait(browser, 20).until(EC.element_to_be_clickable(('xpath', gform_hour))).click()

gform_building_menu_element = browser.find_element('xpath', gform_building_menu)
browser.execute_script("arguments[0].click();", gform_building_menu_element)
WebDriverWait(browser, 20).until(EC.element_to_be_clickable(('xpath', gform_building))).click()



gform_consent_element = browser.find_element('xpath', gform_consent)
browser.execute_script("arguments[0].click();", gform_consent_element)

submit=browser.find_element(By.XPATH,"//*[@id='mG61Hd']/div[2]/div/div[3]/div[1]/div[1]/div[2]")
submit.click()