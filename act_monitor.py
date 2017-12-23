from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import datetime
import calendar
import matplotlib.pyplot as plt


browser = webdriver.PhantomJS(executable_path='G:\phantomjs');
browser.get('http://portal.actcorp.in/group/blr/myaccount')
wait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='My Package']"))).click()
sleep(10)

html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
browser.quit();

text_file = open("Output.html", "w")
text_file.write(html)
text_file.close()

soup = BeautifulSoup(open("Output.html"), "html.parser")



print("\n")
#UserName
UserName = soup.find_all("td",class_="packagecol3")[0];
UserName = UserName.get_text()
print("User ID : "+UserName)

#Plan-Name
s_Plan = soup.find_all("td",class_="packagecol3")[2];
s_Plan = s_Plan.get_text()
print("Plan : "+s_Plan)

print("\n")

#Usage
p_used = soup.find_all("td",class_="packagecol3")[3];
p_used = p_used.get_text()
str_p_used = p_used[0:6]
str_p_max_fup = p_used[17:22]


now = datetime.datetime.now()
nodm = int(calendar.monthrange(now.year, now.month)[1])
res =  str(float(str_p_max_fup)/ float(nodm))
dom = str(int(datetime.date.today().strftime("%d")) * float(res));

print("Limit/Day of "+s_Plan+" : "+str(res[0:4])+" GB for Fair Usage")
avgday = str(float(str_p_used)/float((datetime.date.today().strftime("%d"))))
print("Your Average Limit/Day : "+str(avgday[0:4])+ " as per (",datetime.date.today().strftime("%d"),"/",datetime.date.today().strftime("%B"),")")
print("\n")
print("Max FUP of "+s_Plan+" : "+str_p_max_fup)
print("Your Usage : "+str_p_used)

val = str(float(str_p_max_fup) - float(str_p_used))

print("\n")
print("Remaining FUP : "+val[0:5])
used = float (str_p_used) / float(str_p_max_fup) *100
remi = float (val) / float(str_p_max_fup) * 100

labels = [('Remaining: '+str(val[0:5])+ ' GB') ,('Used: '+str(str_p_used)+ ' GB')]
sizes = [remi, used]
colors = ['lightgreen', 'lightcoral']

plt.title(str(s_Plan)+" : "+str(str_p_max_fup)+" GB");

pie = plt.pie(sizes, autopct='%1.1f%%',colors=colors,startangle=90)

plt.legend(pie[0],labels,title="FUP Status")
fig = plt.gcf()
fig.canvas.set_window_title('ACT Usage Monitor by Madhav')
plt.axis('equal')
plt.tight_layout()
plt.show()


