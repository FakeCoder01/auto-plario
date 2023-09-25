import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
#from webdriver_manager.firefox import GeckoDriverManager
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import base64 as enddec64
import re

full_auto = True
profile_path = r'C:\Users\Leo Asmanov\FirefoxProfiles\Main'
options = webdriver.FirefoxOptions()
#options.set_preference('profile', profile_path)

options.add_argument("-profile")
options.add_argument(profile_path)
service = Service(executable_path='./geckodriver.exe')
browser = webdriver.Firefox(service=service,options=options)
action = ActionChains(browser)

def highlight(element, effect_time, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("border: {0}px dashed {1};".format(border, color))
    time.sleep(effect_time)
    apply_style(original_style)

etime = 0.5
color = "yellow"
border = 5

def moodle_login():
    try:
        browser.get("https://moodle.tsu.ru/")
        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, "usermenu")))
        print("Already logged in Moodle.")
    except TimeoutException:
        print("Logging into Moodle.")
        
        logbutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-login")))
        highlight(logbutton, etime, color, border)   
        logbutton.click()
        
        logbutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "aclogin")))
        highlight(logbutton, etime, color, border)   
        logbutton.click()
    
        # accounts.tsu.ru
        try:
            logbutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-lg")))
            print("Already logged in TSUAccount.")
            highlight(logbutton, etime, color, border)
            logbutton.click()
        except TimeoutException:
            print("Logging into TSUAccount.")
            logfield = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, "Email")))
            highlight(logfield, etime, color, border)
            logfield.send_keys("asmanovlev@gmail.com")
        
            passfield = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.NAME, "Password")))
            highlight(passfield, etime, color, border)
            passfield.send_keys(enddec64.standard_b64decode(b'MjQwOTA1VHN1ISE=').decode())
        
            logbutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-success")))
            highlight(logbutton, etime, color, border)   
            logbutton.click()
        
    #moodle login done

def login_plario():
    assert len(browser.window_handles) == 1 # N-tabs must be equal 1
    original_window = browser.current_window_handle
    # should open new window
    browser.get("https://moodle.tsu.ru/mod/lti/view.php?id=364399")
    WebDriverWait(browser, 20).until(EC.number_of_windows_to_be(2))
    for window_handle in browser.window_handles:
        if window_handle != original_window: # check that new tab isn't the old tab
            browser.switch_to.window(window_handle)
        else:
            browser.close()

    subjectdrop = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[1]/p-dropdown[2]")))
    highlight(subjectdrop, etime, color, border)
    subjectdrop.click()

    subjectitem = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[1]/p-dropdown[2]/div/div[3]/div/ul/p-dropdownitem[1]/li")))
    highlight(subjectitem, etime, color, border)
    subjectitem.click()

    continuebutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/div/div/p-card/div/div/div/app-select-role/div/div/div[2]/button")))
    highlight(continuebutton, etime, color, border)
    continuebutton.click()
    return browser.current_window_handle

def enter_training():
    startbutton = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-layout/div/section/app-dashboard/div/div/div[1]/app-modules/div/section/div[1]/app-module-card/div/div[2]/button")))
    highlight(startbutton, etime, color, border)
    startbutton.click()

def switch_math_mode():
    input("Please, switch math to plain mode manually")
    return
    question = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "task-body")))
    highlight(question, etime, color, border)
    
    # doing that because menu appers
    mastcard = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "mastery-card")))
    highlight(mastcard, etime, color, border)
    action.move_to_element(mastcard).perform()
    
    evaluation = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "math-tex")))[0]
    action.move_to_element(evaluation).perform()
    highlight(evaluation, etime, color, border)
    action.context_click(evaluation).perform()

    showas = WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "MathJax_MenuItem")))
    time.sleep(1)
    highlight(showas[2], etime, color, border)
    action.move_to_element(showas[2]).perform()

def getQnA(plario_tab):
    browser.switch_to.window(plario_tab)
    question = None
    answers = None
    while True:
        try:
            time.sleep(5)
            question = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "task-body")))
            answers = WebDriverWait(browser, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "answer__item")))
            break
        except TimeoutException:
            if full_auto or input("Seems like there's theory. Wanna skip? ") in ["Y", "y"] or full_auto:
                while True:
                    try:
                        understood = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, "/html/body/app-root/app-layout/div/section/app-exercise/div/app-answer-exercise/app-loader/div/div/app-lesson/div/div/div[2]/button")))
                        highlight(understood, etime, color, border)
                        understood.click()
                    except:
                        break


    """for answer in answers:
        print(answer.text)"""
    return question.text, answers

def setA(plario_tab, answer):
    browser.switch_to.window(plario_tab)
    highlight(answer,etime,color,border)
    answer.click()
    if full_auto or input("Submit answer? ") in ["y","Y"] or full_auto:
        time.sleep(1)
        submit = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "mat-confirm")))
        highlight(submit,etime,color,border)
        submit.click()
        time.sleep(5)
        _, answers = getQnA(plario_tab=plario_tab)
        for answer in answers:
            print(answer.get_attribute('innerHTML'))
            if "failure" in answer.get_attribute('innerHTML'):
                input("There's an error, please, proceed manually")
        
        try:
            submit = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "mat-raised-button")))
            highlight(submit,etime,color,border)
            submit.click()
            time.sleep(5)
        except TimeoutException:
            print("Seems like there's wrong answer")


def openCGPT():
    browser.switch_to.new_window('tab')
    browser.get("https://chat.openai.com")
    return browser.current_window_handle
# <app-answer-option _ngcontent-efj-c222="" class="answer__item failure" _nghost-efj-c221=""><div _ngcontent-efj-c221="" class="column"><div _ngcontent-efj-c221="" class="control-wrapper"><svg _ngcontent-efj-c221="" width="20" height="20"><path _ngcontent-efj-c221="" fill-rule="evenodd" clip-rule="evenodd"></path></svg></div></div><div _ngcontent-efj-c221="" class="column"><span _ngcontent-efj-c221="" class="value ck-editor-content"><p>нет правильного ответа</p>
#</span></div></app-answer-option>
def GenerateAnswer(cgpt_tab, text):
    browser.switch_to.window(cgpt_tab)
    time.sleep(1)
    text_field = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.ID, "prompt-textarea")))
    highlight(text_field, etime, color, border)
    text_field.send_keys(text)
    send_button = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[1]/div[2]/form/div/div[2]/div/button")))
    highlight(text_field, etime, color, border)
    send_button.click()
    #source = browser.getPageSource()
    time.sleep(15)
    """while source != browser.getPageSource():
        time.sleep(2.5)
        print("In generation...")
        source = browser.getPageSource()
    print("Done!")"""
    history=WebDriverWait(browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/main/div[1]/div[1]/div/div/div/div")))
    """e = 0
    for m in history[:-1]:
        print(e, m.text)
        e += 1"""
    return history[-2].text

moodle_login()
plario_tab = login_plario()
enter_training()
#switch_math_mode()
cgpt_tab = openCGPT()
while True:
    if not (full_auto or input("Perform again? ") in ['Y','y']):
        exit(0)
    question, answers = getQnA(plario_tab=plario_tab)
    
    prompt = f"Please, solve following task: {question}; Possible answers: "
    n = 0
    for answer in answers:
        n+=1
        prompt+=f"{n}. {answer.text}; "
    prompt+=" Provide steps to solve and index of final answer in the end. (Example of final answer: \"Final answer is: 0\")"
    
    
    try:
        response = GenerateAnswer(cgpt_tab=cgpt_tab, text=prompt)
        response = response.split("\n")
        response = response[len(response)-1]

        response = re.sub(r"\D", "", response)
        print([response])
        if len(response) != 1:
            raise ValueError
        setA(plario_tab, answers[int(response)-1])
    except (ValueError, IndexError):
        response = GenerateAnswer(cgpt_tab=cgpt_tab, text="Sorry, what's the final answer? Provide just a index (without anything else)")
        response = re.sub(r"\D", "", response)
        time.sleep(3)
        setA(plario_tab, answers[int(response)-1])
    
    