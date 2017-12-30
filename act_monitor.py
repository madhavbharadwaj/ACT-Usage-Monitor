from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import datetime
import calendar
import matplotlib.pyplot as plt

#PhantomJS for invisible Browser
browser = webdriver.PhantomJS(executable_path='G:\phantomjs');
browser.get('http://portal.actcorp.in/group/blr/myaccount')
wait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='My Package']"))).click()
sleep(10)

html = browser.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
browser.quit();

#Save in Output.html
text_file = open("Output.html", "w")
text_file.write(html)
text_file.close()

#Parse Using BeautifulSoup From Output File
soup = BeautifulSoup(open("Output.html"), "html.parser")

print("")
#UserName
UserName = soup.find_all("td",class_="packagecol3")[0];
UserName = UserName.get_text()
print("Your User ID : "+UserName)

#Plan-Name
s_Plan = soup.find_all("td",class_="packagecol3")[2];
s_Plan = s_Plan.get_text()
print("Plan : "+s_Plan)

print("")

#Usage
p_used = soup.find_all("td",class_="packagecol3")[3];
p_used = p_used.get_text()
str_p_used = p_used[0:6]
str_p_max_fup = p_used[17:22]

#FlexBytes
p_used_Flex = soup.find_all("td",class_="packagecol3")[5];
p_used_Flex = p_used_Flex.get_text()
str_p_used_Flex = p_used_Flex[0:6]
str_p_max_fup_Flex = p_used_Flex[14:22]

#Fetching Current Date
now = datetime.datetime.now()

#Fetching Number of Days in a Month
nodm = int(calendar.monthrange(now.year, now.month)[1])

#Plan's LIMIT per Day
res =  str(float(str_p_max_fup)/ float(nodm))
print("Limit/Day of "+s_Plan+" : "+str(res[0:4])+" GB for Fair Usage")

#Average Limit per Day till Date
avgday = str(float(str_p_used)/float((datetime.date.today().strftime("%d"))))
print("Your Average Limit/Day : "+str(avgday[0:4])+ " GB as per (",datetime.date.today().strftime("%d"),"/",datetime.date.today().strftime("%B"),")")

print("")
#MAX FUP of your Plan
print("Max FUP of "+s_Plan+" : "+str_p_max_fup+" GB" )

#Your FUP Usage
print("Your Usage : "+str_p_used+" GB")

print("")

#Remaining FUP Count is in 'val'
val = str(float(str_p_max_fup) - float(str_p_used))
val_flex = str(float(str_p_max_fup_Flex) - float(str_p_used_Flex))
#Days Remaining
days_remain = str(int(nodm) - int(datetime.date.today().strftime("%d")))

#Calculating Limit/Day for remaining  days
peru = str(float(val) / float(days_remain))

#Calculating Remaining FUP
print("Remaining Data : "+val[0:5]+" GB")

#Used FUP and Remaning FUP for Plotting Pie Chart
used = float (str_p_used) / float(str_p_max_fup) *100
remi = float (val) / float(str_p_max_fup) * 100


#Used FUP and Remaning FUP for Plotting Pie Chart
used_flex = float (str_p_used_Flex) / float(str_p_max_fup_Flex) *100
remi_flex = float (val_flex) / float(str_p_max_fup_Flex) * 100


#Limit/Day for Remaining 'n' days
print("You can use "+str(peru)[0:5]+" GB per day (Remaining days : "+days_remain +")")

print("")

print(" ----------- Flexybytes ----------------");
print("")
print("Quota : "+str_p_max_fup_Flex+" GB")
print("Usage : "+str_p_used_Flex+" GB")
print("Remaining Data : " +str(val_flex[0:5])+" GB")
print("")
print(" ---------------------------------------")

#Pie Chart using matplotlib

#Color of Remaining and Used
colors = ['lightgreen', 'lightcoral']

names = 'Remaining', 'Used'

#Size of Remaining and Used
size = [remi, used]
labels = [('Remaining: '+str(val[0:5])+ ' GB') ,('Used: '+str(str_p_used)+ ' GB')]


colors_Flex = ['gold', 'yellowgreen']
names_Flex = 'Remaining', 'Used'
labels_flex = [('Remaining: '+str(val_flex[0:5])+ ' GB') ,('Used: '+str(str_p_used_Flex)+ ' GB')]
size_Flex = [remi_flex, used_flex]


fig = plt.figure();
#for fup
ax1 = fig.add_subplot(121)

#for flexy
ax2 = fig.add_subplot(122)

#For FUP Status

ax1.pie(size,autopct='%1.1f%%', colors=colors,startangle=90,center = (-2,0))

#For FlexyBytes

ax2.pie(size_Flex,autopct='%1.1f%%', colors=colors_Flex,startangle=90,center = (-2,0))

#Legend Title
first_legend = ax1.legend(labels, loc = 2,title="FUP Status ( "+str_p_max_fup+" GB )")
second_legend = ax2.legend(labels_flex, loc = 2,title="flexyBytes Status ("+str_p_max_fup_Flex+"GB )")

ax1.axis('equal')
ax2.axis('equal')
plt.tight_layout()

#Window Title
fig = plt.gcf()
fig.canvas.set_window_title('ACT Usage Monitor by Madhav')

#Figure for Actual FUP Status
plt.show()



