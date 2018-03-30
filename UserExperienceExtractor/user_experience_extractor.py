"""
Linkedin Profile Extractor :

Given a linkedin username, fetches the users experiences and company details.
"""
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def time_divide(string):
    """
    :param string: takes the entire time and duration string and splits it
    :return: start year, end year and duration
    """

    duration = re.search(r"\((.*?)\)", string)

    if duration:

        duration = duration.group(0)
        string = string.replace(duration, "").strip()

    else:

        duration = "()"

    times = string.split("–")

    return (times[0].strip(), times[1].strip(),
            duration[1:-1])


def experience(from_date=None, to_date=None, position_title=None, institution_name=None):
    """
    :param from_date: start date
    :param to_date: end date
    :param position_title: position description
    :param institution_name: name of the institution
    :return: string consisting of start date end date and duration
    """

    from_date = from_date
    to_date = to_date
    position_title = position_title

    return ("{position_title} at {company} from {from_date} to {to_date}"
            .format(from_date=from_date, to_date=to_date, position_title=position_title,
                    company=institution_name))


def main():
    """
    :return: Null
    """

    username = input("E-Mail   : ")
    password = input("Password : ")

    experiences = []

    # Initializing the browser and logging in

    driver = webdriver.Chrome()

    driver.get('https://www.linkedin.com/')

    driver.find_element_by_id('login-email').send_keys(username)
    driver.find_element_by_id('login-password').send_keys(password)
    driver.find_element_by_id('login-submit').click()

    name = input("Enter the profile name to be searched ")

    # Fetching the linkedin profile content of the entered name

    driver.get("https://www.linkedin.com/in/"+name)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    # Fetching the UName

    name = driver.find_element_by_class_name("pv-top-card-section__name").text
    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located(
        (By.ID, "experience-section")))

    # Fetching experience

    exp = driver.find_element_by_id("experience-section")

    for position in exp.find_elements_by_class_name("pv-position-entity"):

        position_title = position.find_element_by_tag_name("h3").text
        company = position.find_element_by_class_name("pv-entity__secondary-title").text

        try:

            times = position.find_element_by_class_name("pv-entity__date-range").text
            from_date, to_date, duration = time_divide(times)

        except ValueError:

            from_date, to_date = (None, None)

        expe = experience(position_title=position_title, from_date=from_date,
                          to_date=to_date, institution_name=company)

        experiences.append(expe)

    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "education-section")))

    # Displaying the experiences

    if experiences:
        for i in experiences:
            i = i.split()
            print(*i[0:i.index("from")])
            print(*i[i.index("Employed")+1:len(i)])
    else:
        print("No prior experiences")

    """# Company details

    driver.get("https://www.linkedin.com/company/amazon/")

    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'nav-main__content')))
    _ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//h1[@dir="ltr"]')))

    c_name = driver.find_element_by_xpath('//h1[@dir="ltr"]').text
    about_us = driver.find_element_by_class_name("org-about-us-organization-description__text").text
    specialities = " ".join(driver.find_element_by_class_name("org-about-company-module__specialities")
                    .text.split(", "))
    website = driver.find_element_by_class_name("org-about-us-company-module__website").text
    headquarters = driver.find_element_by_class_name("org-about-company-module__headquarters").text
    industry = driver.find_element_by_class_name("company-industries").text
    company_size = driver.find_element_by_class_name("org-about-company-module__company-staff-count-range").text

    driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

    print(c_name)
    print(about_us)
    print(specialities)
    print(website)
    print(headquarters)
    print(industry)
    print(company_size)
    """

if __name__ == "__main__":
    main()
