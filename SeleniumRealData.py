from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import xlrd


id_applicationID_entity="1017715898708027"
id_offerID_entity="223123982664921"
id_workflowID_entity="193478442374438"
id_actorName_entity="728707217742526"
AppID="435446804119031"

application_list=[]
offer_list=[]
workflow_list=[]
actor_list=[]

# Give the location of the file
loc = ("C:/Users/user/Desktop/Courses/Master2/Stage/MyFirstPaper/BPI Challenge 2017 (filtered2).xlsx")

# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)


def goToEntitiesURL(url):
    newUrl=""
    i=0
    while i<len(url)-13:
        newUrl=newUrl+url[i]
        i=i+1
    newUrl=newUrl+"entities"
    return newUrl

def getApplicationList():
    i=1
    while i<sheet.nrows:
         application_id=sheet.cell_value(i,0)
         if application_id not in application_list:
             application_list.append(application_id)
         i=i+1

def getOfferList():
    i=1
    while i<sheet.nrows:
        event_origin=sheet.cell_value(i,14)
        if event_origin=='Offer':
            offerID=sheet.cell_value(i,11)
            if offerID=='':
                offer_id=sheet.cell_value(i,15)
            else:
                offer_id=offerID
            if offer_id not in offer_list:
                offer_list.append(offer_id)
        i=i+1

def getWorkflowList():
    i=1
    while i<sheet.nrows:
        event_origin=sheet.cell_value(i,14)
        if event_origin=='Workflow':
            workflow_id=sheet.cell_value(i,15)
            if workflow_id not in workflow_list:
                workflow_list.append(workflow_id)
        i=i+1

def getActorList():
    i=1
    while i<sheet.nrows:
        actor_name=sheet.cell_value(i,12)
        if actor_name not in actor_list:
            actor_list.append(actor_name)
        i=i+1


driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://wit.ai/")
#open tab
driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

#connect with facebook account
link = driver.find_element_by_link_text('Continue With Facebook')
link.click()
driver.switch_to.window(driver.window_handles[1])

email_area = driver.find_element_by_id("email")
email_area.clear()
email_area.send_keys("meriana.kb@gmail.com")

pass_area = driver.find_element_by_id("pass")
pass_area.clear()
pass_area.send_keys("MyChatBot")

login_button=driver.find_element_by_id("u_0_0")
login_button.click()

#wait to close the connection window
time.sleep(20)

#return to the intial window
driver.switch_to.window(driver.window_handles[0])

driver.implicitly_wait(5)

#close new alert
close_alert= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p tn64ylxs bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]').click()
time.sleep(3)
#click on the app cell
#driver.get(driver.current_url+"/"+AppID)

#go the entities url
#entities_url=goToEntitiesURL(driver.current_url)



start_time = time.time()
'''''
driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_applicationID_entity)
getApplicationList()
for appid in application_list:
     #add keyword button
    while 1==1:
        try:
            add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
            break
        except:
            driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_applicationID_entity)
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(appid)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()
    
    time.sleep(2.5)
  
driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_offerID_entity)
getOfferList()
for offid in offer_list:
     #add keyword button
    while 1==1:
        try:
            add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
            break
        except:
            driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_offerID_entity)
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(offid)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()

    time.sleep(2.5)
    
driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_workflowID_entity)
getWorkflowList()
for workid in workflow_list:
     #add keyword button
    while 1==1:
        try:
            add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
            break
        except:
            driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_workflowID_entity)
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(workid)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()

    time.sleep(2.5)
    '''
driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_actorName_entity)
getActorList()
for actor in actor_list:
     #add keyword button
    while 1==1:
        try:
            add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
            break
        except:
            driver.get("https://wit.ai/apps/"+AppID+"/entities/"+id_actorName_entity)
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(actor)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()

    time.sleep(2.5)

print("--- %s seconds ---" % (time.time() - start_time))

