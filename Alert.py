from threading import Thread
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys

class Alert(Thread):

    def __init__(self, stop_event, refresh_time, coursecode, classnum):
        Thread.__init__(self)
        self.stopped = stop_event
        self.refresh_time = refresh_time
        self.course_code = coursecode
        self.class_num = classnum
        self.data = []
        o = Options()
        o.add_argument("--headless")
        self.driver = webdriver.Chrome(options=o)
        self.open_class() #just open everything now

    def run(self):
        print("Initializing {} {}".format(self.course_code, self.class_num))
        #self.open_class() #open all of the right pages.

        self.gather_data() #do this so we don't have to wait the full refresh time.
        #then we can go into the loop

        while not self.stopped.wait(self.refresh_time):
            print("Scanning {} {} and then waiting {} seconds.".format(self.course_code, self.class_num,
                                                                           self.refresh_time))
            #now this is where we gather the data...
            self.driver.refresh()
            self.data.clear()
            self.gather_data()

    def print_data(self):
        print()
        print("Printing data for {} {}".format(self.course_code, self.class_num))
        for section in self.data:
            print("Section {}, {}/{}, Class open? {}".format(section[0], section[1], section[2], section[3]))
        print("End of {} {}".format(self.course_code, self.class_num))
        print()


    def update_timer(self, new_refresh_time):
        self.refresh_time = new_refresh_time


    def open_class(self):
        self.driver.get("https://schedule.msu.edu") #open schedule.msu.edu
        select = Select(self.driver.find_element_by_xpath('//*[@id="MainContent_ddlSubject"]'))
        select.select_by_value(self.course_code) #select the class in the drop down menu
        course_num = self.driver.find_element_by_xpath('//*[@id="MainContent_txtCourseNumber"]')
        course_num.clear()
        course_num.send_keys(self.class_num) #type in the course code in the text box
        self.driver.find_element_by_xpath('//*[@id="MainContent_btnSubmit"]').click() #click search

    def gather_data(self):
        #self.driver.refresh() #don't forget to refresh every time
        tables = self.driver.find_elements_by_xpath(
            "//table[@class='col-md-12 table-bordered table-striped table-condensed course-results cf']")
        counter = 1
        for table in tables:
            #xpath = '//*[@id="MainContent_divHeader1_va"]/h3[{}]/a'.format(counter)
            for row in table.find_elements_by_css_selector('tr'):
                section = ""
                currently_enrolled = 0
                max_enrolled = 0
                for cell in row.find_elements_by_tag_name('td'):
                    if cell.get_attribute("class") == "section-number":
                        section = int(cell.text)
                    elif cell.get_attribute("class") == "enrolled-currently":
                        currently_enrolled = int(cell.text)
                    elif cell.get_attribute("class") == "enrollment-limit":
                        max_enrolled = int(cell.text)
                class_open = False if currently_enrolled - max_enrolled >= 0 else True
                if section is not "":
                    l = [section, currently_enrolled, max_enrolled, class_open]
                    self.data.append(l)
            counter += 1