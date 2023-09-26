from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from handler import GETPlarioAnswerAPI
import time
from colorama import Fore, Back, Style
from bs4 import BeautifulSoup



options = webdriver.EdgeOptions()
browser = webdriver.Edge(options=options)
action = ActionChains(browser)


class LoginManager:
    def __init__(self, email:str, password:str, course_url:str) -> None:
        print(Fore.BLACK + Back.GREEN + '\nAttempting Login' + Style.RESET_ALL)
        self.email = email
        self.password = password
        self.course_url = course_url


    def login_to_moodle(self):
        try:
            print(Fore.BLUE + Back.CYAN + '\nTrying to login to moodle' + Style.RESET_ALL)

            try:
                # Already logged in to moodle
                browser.get("https://moodle.tsu.ru/")
                WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.ID, "usermenu")))

                print(Fore.BLACK + Back.GREEN + '\nAlready logged in' + Style.RESET_ALL)
            except:
                # Login to moodle 
                print(Fore.RED + Back.YELLOW + '\nLogging in with TSU account' + Style.RESET_ALL)

                logbutton = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-login"))) 
                logbutton.click()
                
                logbutton = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "aclogin")))
                logbutton.click()

                try:
                    # Already logged in to TSU a/c
                    logbutton = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-lg")))
                    logbutton.click()
                    print(Fore.BLACK + Back.GREEN + '\nAlready logged in with TSU account' + Style.RESET_ALL)
                except :
                    # Login to TSU a/c
                    print(Fore.GREEN + Back.MAGENTA + '\nLogging in with TSU account email and password' + Style.RESET_ALL)

                    logfield = WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.NAME, "Email")))
                    logfield.send_keys(self.email)
                
                    passfield = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.NAME, "Password")))
                    passfield.send_keys(self.password)
                
                    logbutton = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))
                    logbutton.click()

            print(Fore.MAGENTA + Back.YELLOW + '\n# Moodle login successful' + Style.RESET_ALL + '\n\n')
        except Exception as err:
            print("error LoginManager.login_to_moodle() : ", err)
                

    def login_to_plario(self):
        try:
            print(Fore.BLUE + Back.CYAN + '\nTrying to login to plario' + Style.RESET_ALL)

            original_window = browser.current_window_handle
            browser.get(self.course_url)
            WebDriverWait(browser, 2).until(EC.number_of_windows_to_be(2))

            for window_handle in browser.window_handles:
                if window_handle != original_window: 
                    browser.switch_to.window(window_handle)
                else:
                    browser.close()

            subjectdrop = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[1]/p-dropdown[2]")))
            subjectdrop.click()

            subjectitem = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[1]/p-dropdown[2]/div/div[3]/div/ul/p-dropdownitem[1]/li")))
            subjectitem.click()

            continuebutton = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[2]/button")))
            continuebutton.click()

            print(Fore.MAGENTA + Back.YELLOW + '\n# Plario login successful' + Style.RESET_ALL + '\n\n')

            return browser.current_window_handle
        except Exception as err:
            print("Error LoginManager.login_to_plario() : ", err)

class AttemptManager:
    def __init__(self, plario_tab) -> None:
        self.plario_tab = plario_tab
        self.count = 0

    def start_test(self):
        try:
            print(Fore.RED + Back.BLUE + '\nStarting the test' + Style.RESET_ALL)
            time.sleep(8)
            startbutton = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-layout/div/section/app-dashboard/div/div/div[1]/app-modules/div/section/div[1]/app-module-card/div/div[2]/button")))
            startbutton.click()
            print(Fore.MAGENTA + Back.YELLOW + '\n# Test started' + Style.RESET_ALL + '\n\n')


            input("Please change the math render and then press Any key to continue : ")
            time.sleep(5)


        except Exception as err:
            print("Error AttemptManager.start_test() : ", err)

    def get_plario_credentials(self) -> dict:
        print("\nGetting the credentials")
        local_storage = browser.execute_script("return window.localStorage;")

        return {
            'module_id' : browser.execute_script("return window.localStorage.getItem('plario.selectedModuleId');"),
            'teacher_course_id' : browser.execute_script("return window.localStorage.getItem('plario.selectedCourseId');"),
            'attempt_id' : PUT_YOUR_ATTEMPT_ID, # ( a 7 digit int) , # browser.execute_script("return window.localStorage.getItem('key');"),
            'auth_token' : browser.execute_script("return window.localStorage.getItem('plario.access_token');")
        }

    def submit_answer(self)-> int:

        self.count += 1
        print(Fore.RED + Back.YELLOW + f'\nAnswering question ({self.count})' + Style.RESET_ALL)

        try:
            browser.switch_to.window(self.plario_tab)
            answers = WebDriverWait(browser, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "answer__item")))


            plario_credentials = self.get_plario_credentials()
            module_id = plario_credentials['module_id']
            teacher_course_id = plario_credentials['teacher_course_id']
            attempt_id = plario_credentials['attempt_id']
            auth_token = plario_credentials['auth_token'].replace('"', '')

            total_answers = len(answers)

            print(Fore.GREEN + Back.MAGENTA + f'\nGetting the answer ({self.count})' + Style.RESET_ALL)
            answer_data = GETPlarioAnswerAPI(module_id=module_id, teacher_course_id=teacher_course_id, attempt_id=attempt_id, auth_token=auth_token)
            answer_data = answer_data.get_answer()

            if answer_data == False:
                print("Answer API call failed")
            else:
                print(Fore.WHITE + Back.GREEN + f'\nAnswer received ({self.count})' + Style.RESET_ALL)

            correct_answer_text = answer_data['answer_text']
            formatted_text = BeautifulSoup(correct_answer_text, 'html.parser').get_text()

            ## Note : I'm using this crappy code just for faster dev, use regex or some customized
            ##        parser to parse the data from API and the DOM element (answer)
            ### REWRITE USING REGEX START #
            formatted_text = formatted_text.replace(" ", "")
            formatted_text = formatted_text.replace("\(", "")
            formatted_text = formatted_text.replace("\)", "")
            formatted_text = "".join(formatted_text.split())
            ### REWRITE USING REGEX END ###


            print(f"o:{formatted_text}")
            for index in range(0, total_answers):
                ans = answers[index].get_attribute('innerText').replace(" ","")
                print(f"p:{ans}")
                if formatted_text == ans:

                    # answers[index].click()
                    browser.execute_script(f"document.getElementsByClassName('answer__item')[{index}].click()")
                    browser.execute_script("document.getElementsByClassName('mat-confirm')[0].click()")
                    time.sleep(2)
                    
                    browser.execute_script("document.getElementsByClassName('mat-raised-button')[0].click()")

                    print('\n' + Fore.GREEN + Back.LIGHTGREEN_EX, f'Answered/Solved ({self.count})' + Style.RESET_ALL + '\n\n')
                    time.sleep(3)
                    return 1
                
            print(Fore.WHITE + Back.RED, f'\nAnswer Failed ({self.count})' + Style.RESET_ALL + '\n\n')
            return -1
        except Exception as err:
            print("Error AttemptManager.submit_answer() : ", err)
            while True:
                try:
                    understood = WebDriverWait(browser, 1).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-layout/div/section/app-exercise/div/app-answer-exercise/app-loader/div/div/app-lesson/div/div/div[2]/button")))
                    understood.click()
                except:
                    break
            return -1
def initiate_the_buzz(email:str, password:str, course_url:str) -> bool:
    try:
        print("\n-------Started------\n")
        login_manager = LoginManager(email=email, password=password, course_url=course_url)
        login_manager.login_to_moodle()
        plario_login = login_manager.login_to_plario()

        attempt_manager = AttemptManager(plario_tab=plario_login)
        attempt_manager.start_test()
        for i in range(0, 20):
            i += attempt_manager.submit_answer()
        return True
    
    except Exception as err:
        print("Error buzz_main : ", err)
        return False

if __name__ == "__main__":

    # YOUR TSU ACCOUNT EMAIL
    EMAIL = "EMAIL"

    # YOUR TSU ACCOUNT PASSWORD
    PASSWORD = "PASSWORD"

    # MOODLE COURSE URL
    COURSE_URL = "https://moodle.tsu.ru/mod/lti/view.php?id=364399"
        
    work = initiate_the_buzz(EMAIL, PASSWORD, COURSE_URL)

    if work:
        print("You nailed it :)")
    else:
        print("Something went wrong :(")



