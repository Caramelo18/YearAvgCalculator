from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import getpass

url = "https://sigarra.up.pt/feup/pt/web_page.inicial"
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
    #course = courses[0]
        year = course.find_element_by_css_selector(':first-child').get_attribute('innerHTML')
        semester = course.find_element_by_css_selector(':nth-child(2)').get_attribute('innerHTML')
        link = course.find_element_by_css_selector(':nth-child(3) a').get_attribute('href')
        name = course.find_element_by_class_name('uc').text

        id = link.split('=')[1]
        print(year, semester, name)

        analyze_course(id)


def analyze_course(id):
    cookies = browser.get_cookies()
    #migrate cookies from browser to BeautifulSoup
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    results_url = 'https://sigarra.up.pt/feup/pt/est_geral.dist_result_ocorr_detail?pv_ocorrencia_id=' + id

    r = session.get(results_url)

    data = r.text
    soup = BeautifulSoup(data, "lxml")

    base_id = 'tbl_estat_table_dist_result_ocorr_detail_' + id + '__S'
    table = soup.find(id=base_id)

    results = soup.find_all("tr", class_="d")

    num_approved = 0
    sum_notes = 0

    for result in results:
        soup = BeautifulSoup(str(result), "lxml")
        grade = soup.select('td:nth-of-type(1)')
        ammount = soup.select('td:nth-of-type(3)')
        soup = BeautifulSoup(str(grade), "lxml")

        grade = soup.text.replace("[", "")
        grade = grade.replace("]", "")

        if grade == "RFE" or grade == "RFF" or grade == "RFC" or grade == "RD":
            continue

        grade = int(grade)

        soup = BeautifulSoup(str(ammount), "lxml")
        ammount = soup.text.replace("[", "")
        ammount = int(ammount.replace("]", ""))


        if grade >= 10:
            num_approved += ammount
            sum_notes += ammount * grade


    average = sum_notes/num_approved
    print(average)
    #print("\n")


def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    login(username, password)

    go_to_student_page()
    navigate_courses()


main()
