import requests

class GETPlarioAnswerAPI:

    def __init__(self, module_id:int, teacher_course_id:int, attempt_id:int, auth_token:str) -> None:
        self.module_id = module_id
        self.teacher_course_id = teacher_course_id
        self.attempt_id = attempt_id
        self.auth_token = auth_token

    def get_answer(self):

        try:
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "en-US,en;q=0.9,bn;q=0.8",
                "authorization": f"Bearer {self.auth_token}",
                "content-type": "application/json",
                "sec-ch-ua": "\"Chromium\";v=\"117\", \"Not)A;Brand\";v=\"24\", \"Microsoft Edge\";v=\"117\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }

            get_question = requests.get(
                url = f'https://my.plario.ru/api/adaptiveLearning?moduleId={self.module_id}&teacherCourseId={self.teacher_course_id}&culture=ru',
                headers=headers,
                json=None
            )
            result = get_question.json()
            activity_id = result['exercise']['activityId']
            answers = result['exercise']['possibleAnswers']

            api_answer_map = {}
            choosen_answer_id = answers[0]['answerId']
            for answer in answers:
                api_answer_map[answer['answerId']] = answer['text']

             
            post_answer = requests.post(
                url = 'https://my.plario.ru/api/adaptiveLearning/checkAnswer?culture=ru',
                headers=headers,
                json={
                    "activityId" : activity_id,
                    "attemptId" : self.attempt_id,
                    "answerId" : choosen_answer_id,
                    "moduleId" : self.module_id,
                    "teacherCourseId" : self.teacher_course_id
                }
            )

            result = post_answer.json()
            right_answer_id = result['rightAnswerId']

            if right_answer_id == choosen_answer_id :
                return True
            
            return {
                'answer_id' : right_answer_id,
                'answer_text' : api_answer_map[right_answer_id]
            }

        except Exception as err:
            print("Error : (API Call) : ", err)
            return False

