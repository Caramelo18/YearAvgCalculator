from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import getpass

url = "https://sigarra.up.pt/feup/pt/web_page.inicial"
#r = requests.get(url)

chromedriver = 'chromedriver'
browser = webdriver.Chrome(chromedriver)
browser.get(url)



def login(username, password):
    username_field = browser.find_element_by_name('p_user')
    password_field = browser.find_element_by_name('p_pass')

    username_field.send_keys(username)
    password_field.send_keys(password)

    browser.find_element_by_css_selector('button').click()


def go_to_student_page():
    browser.find_element_by_class_name('nomelogin').click()
    browser.find_element_by_css_selector('a[title="Visualizar informações no contexto do curso"]').click()

def navigate_courses():
    table = browser.find_element_by_css_selector('.dadossz tbody')

    courses = table.find_elements_by_css_selector('.i, .p')

    for course in courses:
        year = course.find_element_by_css_selector(':first-child').get_attribute('innerHTML')
        semester = course.find_element_by_css_selector(':nth-child(2)').get_attribute('innerHTML')
        link = course.find_element_by_css_selector(':nth-child(3) a').get_attribute('href')
        name = course.find_element_by_class_name('uc').text

        print(link)
        print(year, semester, name)

        #browser.back()
        #browser.execute_script("window.history.go(-1)")

def analyze_course():
    results_url = 'https://sigarra.up.pt/feup/pt/est_geral.dist_result_ocorr_detail?pv_ocorrencia_id='

def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    login(username, password)

    go_to_student_page()
    navigate_courses()

main()
