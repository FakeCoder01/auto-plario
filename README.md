## Plario Automate All Task

#### It uses Microsoft Edge as the webdriver, if you want to use other that this, configure it accordingly.

### Steps:
1. Install dependencies
```
pip install -r requirements.txt
```

2. Open plario and go to the `network tab`. Find `attempId` in under the payload of /api/checkAnswer/ 


3. Change the credentials in the file `plario.py`. put Email, Attempt ID and  Password in respected field.


4. Run the script
```
python plario.py
```

```
I do not suggest or support using this. I wrote this code entirely for learning purposes only. 
Only you will be responsible if you use this cript.
```