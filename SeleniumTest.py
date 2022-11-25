from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from ReadFromExcel import BusinessRole, ActorRole

id_acceptedRelation_entity="1551408325019014"
id_roleName_entity="224137248606408"
id_actorEmail_entity="588434325445186"

def goToEntitiesURL(url):
    newUrl=""
    i=0
    while i<len(url)-13:
        newUrl=newUrl+url[i]
        i=i+1
    newUrl=newUrl+"management/entities"
    return newUrl



driver = webdriver.Chrome('./chromedriver')
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

#click on the app cell
app_click=driver.find_element_by_xpath('//div[@class="_2e42 _2yi9 _2yia"]').click()

#go the entities url
entities_url=goToEntitiesURL(driver.current_url)

driver.get(entities_url+"/"+id_roleName_entity)

for item in BusinessRole:
    #add keyword button
    while 1==1:
        try:
            add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
            break
        except:
            driver.get(entities_url+"/"+id_roleName_entity)
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(item)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()

    time.sleep(2.5)
'''
#add actor emails
driver.get(entities_url+"/"+id_actorEmail_entity)
for item in ActorRole:
    #add keyword button

    add_keyWord= driver.find_elements_by_xpath('//div[@class="g1fckbup dfy4e4am lfmgir71 sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b ndrgvajj s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea ne82rp9a fg52cco8"]')[1].click()
    keyword_area = driver.find_element_by_xpath("//input[@placeholder='Enter a new keyword']")
    keyword_area.clear()
    keyword_area.send_keys(item)

    save_keyWord= driver.find_element_by_xpath('//div[@class="g1fckbup dfy4e4am gcxdxe9k sdgvddc7 b8b10xji okyvhjd0 rpcniqb6 jytk9n0j ojz0a1ch avm085bc mtc4pi7f jza0iyw7 njc9t6cs qhe9tvzt spzutpn9 puibpoiz svsqgeze if5qj5rh har4n1i8 diwav8v6 nlmdo9b9 h706y6tg qbdq5e12 j90q0chr rbzcxh88 h8e39ki1 rgsc13q7 a53abz89 llt6l64p pt6x234n bmtosu2b hk3wrqk2 s7wjoji2 jztyeye0 d5rc5kzv jdcxz0ji frrweqq6 qnavoh4n b1hd98k5 c332bl9r f1dwqt7s rqkdmjxc tb4cuiq2 nmystfjm kojzg8i3 m33fj6rl wy1fu5n8 chuaj5k6 hkz453cq dkjikr3h ay1kswi3 lcvupfea siqinikb ppbiusal"]').click()

    time.sleep(2.5)
'''''
