from src.solver import LoginManager, AttemptManager
from dotenv import load_dotenv
import os, logging


load_dotenv()
logging.basicConfig(filename="debug.log", format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

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
        logging.error(err)
        print("Error buzz_main : ", err)
        return False

if __name__ == "__main__":
    ATTEMPT_ID = os.getenv('ATTEMPT_ID')
    EMAIL = os.getenv('EMAIL')
    PASSWORD = os.getenv('PASSWORD')
    COURSE_URL = os.getenv('COURSE_URL')
        
    work = start_and_solve(EMAIL, PASSWORD, COURSE_URL, ATTEMPT_ID)

    if work:
        print("You nailed it :)")
    else:
        print("Something went wrong :(")
