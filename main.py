# author: jake suddreth
# using web automation to create a tool that finds the best deals on flights
import time
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# define flight class to create objects
class Flight:
    def __init__(self):
        self.airline = ''
        self.departure_time = ''
        self.arrival_time = ''
        self.num_stops = 0
        self.layover_location = ''
        self.duration = ''
        self.expense = []


# disguise web browser from driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options, executable_path=r"C:\Users\kenet\FlightAPI\chromedriver.exe")
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


def find_day(d, n, x):
    found_day = False
    for r in range(2, 8):
        if not found_day:
            for c in range(1, 8):
                try:
                    temp = d.find_element_by_xpath(
                        "//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[2]/div[" + str(
                            x) + "]/div[2]/table/tbody/tr[" + str(
                            r) + "]/td[" + str(c) + "]/a")
                    if temp.text == n:
                        temp.click()
                        found_day = True
                        break
                except selenium.common.exceptions.NoSuchElementException:
                    pass


def find_month(d, m_n, d_n):
    month_str = months[m_n - 1]
    found_dep_month = False
    while not found_dep_month:
        month = d.find_element_by_xpath(
            "//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[2]/div[1]/div[1]/div/span[1]")
        if month.text == month_str:
            found_dep_month = True
            find_day(driver, d_n, 1)
        elif d.find_element_by_xpath(
                "//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[2]/div[2]/div[1]/div/span[1]").text == month_str:
            found_dep_month = True
            find_day(d, d_n, 2)
        else:
            arrow = d.find_element_by_xpath(
                "//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[1]/a[2]/span")
            arrow.click()


# pull data from Delta Airlines
def delta(d, a, d_d, r_d, n):
    driver.get("https://www.delta.com")
    driver.maximize_window()  # maximized for testing purposes only
    time.sleep(1)
    dep = driver.find_element_by_xpath("//*[@id=\"fromAirportName\"]/span[1]")
    dep.click()
    dep = driver.find_element_by_xpath("//*[@id=\"search_input\"]")
    dep.click()
    dep.send_keys(d)
    time.sleep(1)
    dep = driver.find_element_by_xpath("//*[@id=\"airport-serach-panel\"]/div/div[2]/div/ul/li[1]/a/span[2]")
    dep.click()
    arr = driver.find_element_by_xpath("//*[@id=\"toAirportName\"]/span[1]")
    arr.click()
    arr = driver.find_element_by_xpath("//*[@id=\"search_input\"]")
    arr.click()
    arr.send_keys(a)
    time.sleep(1)
    arr = driver.find_element_by_xpath("//*[@id=\"airport-serach-panel\"]/div/div[2]/div/ul/li[1]/a/span[2]")
    arr.click()
    time.sleep(1)
    dep = driver.find_element_by_xpath("//*[@id=\"calDepartLabelCont\"]/span[2]")
    dep.click()
    month_num = int(d_d.split('/')[0])
    day_num = d_d.split('/')[1]
    find_month(driver, month_num, day_num)
    month_num = int(r_d.split('/')[0])
    day_num = r_d.split('/')[1]
    find_month(driver, month_num, day_num)
    done = driver.find_element_by_xpath("//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[3]/date-selection-view/div/div/div/div/div[4]/div/div[3]/button[2]")
    done.click()
    pas = driver.find_element_by_xpath("//*[@id=\"booking\"]/form/div[1]/div/div[1]/div[1]/div[4]/span/span[1]")
    pas.click()
    time.sleep(0.5)
    num_pas = driver.find_element_by_xpath("//*[@id=\"ui-list-passengers" + str(int(n)-1) + "\"]")
    num_pas.click()
    search = driver.find_element_by_xpath("//*[@id=\"btn-book-submit\"]")
    search.click()
    # read flight options
    exists = True
    while exists:
        try:
            pass
        except selenium.common.exceptions.NoSuchElementException:
            exists = False


# pull data from Southwest Airlines
def southwest(d, a, d_d, r_d, n):
    driver.get("https://www.southwest.com")
    dep = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_originationAirportCode\"]")
    dep.click()
    dep.send_keys(d, Keys.ENTER)
    arr = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_destinationAirportCode\"]")
    arr.click()
    arr.send_keys(a, Keys.ENTER)
    dep_date = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_departureDate\"]")
    dep_date.click()
    dep_date.send_keys(d_d)
    ret_date = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_returnDate\"]")
    ret_date.click()
    ret_date.send_keys(r_d)
    pas = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_adultPassengersCount\"]")
    pas.click()
    num_pas = driver.find_element_by_xpath(
        "//*[@id=\"LandingAirBookingSearchForm_adultPassengersCount--item-" + str(int(n) - 1) + "\"]/button")
    num_pas.click()
    time.sleep(1)
    search = driver.find_element_by_xpath("//*[@id=\"LandingAirBookingSearchForm_submit-button\"]")
    search.click()
    i = 1
    # read departing flights options
    exists = True
    while exists:
        try:
            flight_data = driver.find_element_by_xpath(
                "//*[@id=\"air-booking-product-0\"]/div[6]/span/span/ul/li[" + str(i) + "]").text.split("\n")
            flight = Flight()
            flight.airline = "Southwest"
            flight.departure_time = time.strptime(flight_data[1], '%I:%M%p')
            flight.arrival_time = time.strptime(flight_data[2][0:5], '%I:%M%p')
            if flight_data[2][6] == N:
                flight.num_stops = 0
                flight.layover_location = 'N/A'
            else:
                flight.num_stops = flight_data[2][6]
                flight.layover_location = flight_data[3][14:16]
            flight.duration = flight_data[4].replace(' ', ':').replace('h', '').replace('m', '')
            flight.expense = flight_data[6:9].reverse()
            departing_flights.append(flight)
            i += 1
        except selenium.common.exceptions.NoSuchElementException:
            exists = False


# depart = input("Enter the airport code from which you would like to depart:\n")
# depart_date = input("Enter the date from which you would like to depart (MM/DD):\n")
# arrive = input("Enter the airport code from which you would like to arrive:\n")
# return_date = input("Enter the date from which you would like to return (MM/DD):\n")
# num_passengers = input("Enter the number of passengers that will be traveling:\n")
# southwest(depart, arrive, depart_date, return_date, num_passengers)

# store months of the year to access by index
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]

# store flight objects
departing_flights = []
arriving_flights = []

# call function for testing
# only works currently with round-trip flights
# current roadblock, delta airlines provides one price for round-trip, Southwest provides departing and arriving options
delta("ORD", "LAX", "9/12", "9/19", "2")

# prompt user and accept input
# call functions that are stored in list
