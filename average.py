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

    sum_credits = 0
    total_notes = 0
    grades = dict()
    year_grades = dict()

    for course in courses:
    #course = courses[0]
        year = course.find_element_by_css_selector(':first-child').get_attribute('innerHTML')
        semester = course.find_element_by_css_selector(':nth-child(2)').get_attribute('innerHTML')
        link = course.find_element_by_css_selector(':nth-child(3) a').get_attribute('href')
        name = course.find_element_by_class_name('uc').text
        credits = course.find_element_by_css_selector(':nth-child(6)').get_attribute('innerHTML')
        credits = float(credits.replace(",", "."))
        own_grade = int(get_own_grade(course))

        id = link.split('=')[1]
        print(year, semester, name, credits, own_grade)

        course_average = analyze_course(id, own_grade)
        sum_credits += credits
        total_notes += credits * course_average

        year_semester = year + 'A ' + semester
        if year_semester in grades:
            grades[year_semester] = grades[year_semester] + (course_average * credits)
        else:
            grades[year_semester] = course_average * credits

        if year in year_grades:
            year_grades[year] = year_grades[year] + (course_average * credits)
        else:
            year_grades[year] = course_average * credits

    total_course_average = round(total_notes/sum_credits, 2)
    print("Course average:", total_course_average)

    for semester in grades:
        semester_average = round(int(grades[semester])/30,2)
        print(semester, "-", semester_average)

    print("\n")

    for year in year_grades:
        year_average = round(int(year_grades[year])/60, 2)
        print(year, "year -" , year_average)


def analyze_course(id, own_grade):
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
    num_below = 0
    num_above = 0
    num_same = 0

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

            if grade < own_grade:
                num_below += ammount
            elif grade == own_grade:
                num_same += ammount
            else:
                num_above += ammount


    average = sum_notes/num_approved
    average = round(average, 2)
    percentage_below = round(num_below/num_approved * 100, 2)
    percentage_same = round(num_same/num_approved * 100, 2)
    percentage_above = round(num_above/num_approved * 100, 2)
    print("Course average:", average)
    print("Your grade is better than ", percentage_below, "%")
    print(percentage_same, "% have the same grade")
    print("Your grade is worse than ", percentage_above, "% \n")
    return average

def get_own_grade(course):
    own_grade = course.find_element_by_css_selector(':nth-child(7)').get_attribute('innerHTML')

    if own_grade == "&nbsp;":
        own_grade = course.find_element_by_css_selector(':nth-child(9)').get_attribute('innerHTML')

    if own_grade == "&nbsp;":
        own_grade = course.find_element_by_css_selector(':nth-child(11)').get_attribute('innerHTML')

    return own_grade


def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    login(username, password)

    go_to_student_page()
    navigate_courses()


main()
