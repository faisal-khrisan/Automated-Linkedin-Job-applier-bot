import time
import google.generativeai as geni
from selenium import  webdriver
from selenium.common import ElementNotVisibleException
from selenium.webdriver.common.by import  By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import  expected_conditions as ec
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

geni.configure(api_key=api_key)

model = geni.GenerativeModel('models/gemini-1.5-pro-latest')


def  generate_content (prompt):
    respone = model.generate_content(prompt)
    return  respone.text

options = webdriver.EdgeOptions()
options.add_experimental_option("detach", True)
news_driver = webdriver.Edge()

news_driver.get("https://news.ycombinator.com/news")

# Scraping the information from tech news hacker news

titles = news_driver.find_elements(By.CSS_SELECTOR, "span.titleline > a")
scores = news_driver.find_elements(By.CLASS_NAME, "score")

links = [link.get_attribute("href") for link in titles]

titles = [title.text for title in titles]

scores = [int(score.text.split()[0]) for score in scores]

highest_value = max (scores)
index_of_highest_element = scores.index( highest_value)

prompt = f"give me Brief summary in 2 short lines for this {titles[index_of_highest_element]}"
hashtage_prompt = f"Generate 3 relevant Hashtages for this title {titles[index_of_highest_element]} for tweeter like #TechNews do not give more just three is enough and no need to write 1,2,3 also I want them all to be in the same line  "

summary_of_headnews = generate_content(prompt)
hashtage_generation = generate_content(hashtage_prompt)

post = f""" Breaking News : {titles[index_of_highest_element]} 
 {summary_of_headnews}
Read more: {links[index_of_highest_element]}
#TechNews {hashtage_generation}"""



driver = webdriver.Edge(options=options)


driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")

wait = WebDriverWait(driver,10)

# button = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
# button.click()
user_email = wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
user_email.send_keys(email)
user_password = wait.until(ec.presence_of_element_located((By.XPATH,"/html/body/div/main/div[2]/div[1]/form/div[2]/input")))
user_password.send_keys(password)
submit = wait.until(ec.presence_of_element_located((By.XPATH,'//*[@id="organic-div"]/form/div[4]/button')))
submit.click()

go_write_post = wait.until(ec.presence_of_element_located((By.XPATH,"/html/body/div[6]/div[3]/div/div/div[2]/div/div/main/div[1]/div[2]/div[2]/button")))
go_write_post.click()

write_post = wait.until(ec.presence_of_element_located((By.XPATH,"//div[@class='ql-editor ql-blank']")))
write_post.send_keys(post)

share_post = wait.until(ec.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div[2]/button")))
share_post.click()



