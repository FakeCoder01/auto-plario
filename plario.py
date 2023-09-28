from src.solver import LoginManager, AttemptManager

def start_and_solve(email:str, password:str, course_url:str, attempt_id:int) -> bool:
    try:
        print("\n-------Started------\n")
        login_manager = LoginManager(email=email, password=password, course_url=course_url)
        if not login_manager.login_to_moodle() :
            return False
        plario_login = login_manager.login_to_plario()
        if plario_login == False:
            return False

        attempt_manager = AttemptManager(plario_tab=plario_login, attempt_id=attempt_id)
        if attempt_manager.start_test():
            for i in range(150):
                i += attempt_manager.submit_answer()
            return True
        else:
            return False
    
    except Exception as err:
        print("Error buzz_main : ", err)
        return False

if __name__ == "__main__":


    # PLARIO_ATTEMP_ID. Find in plario network tab. endpoint : /api/checkAnswer/  (check attemptID in payload)
    ATTEMPT_ID = 'ATTEMP_ID' # ( a 7 digit int)

    # YOUR TSU ACCOUNT EMAIL
    EMAIL = "email"

    # YOUR TSU ACCOUNT PASSWORD
    PASSWORD = "password"

    # MOODLE COURSE URL
    COURSE_URL = "https://moodle.tsu.ru/mod/lti/view.php?id=364399"
        
    work = start_and_solve(EMAIL, PASSWORD, COURSE_URL, ATTEMPT_ID)

    if work:
        print("You nailed it :)")
    else:
        print("Something went wrong :(")
