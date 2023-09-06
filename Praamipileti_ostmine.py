from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from playsound import playsound
import datetime


IK = input("Sisesta on isikukood: ")
auto = input("Sisesta oma auto reg. nr: ") 
email = input("Sisesta oma email: ") 
tel = input("Sisesta oma tel. nr ilma suunakoodita: ")
suund = input('Vali kas HR(Heltermaa-Rohuküla) või RH(Rohuküla-Heltermaa): ')
mitmes_praam = input("Sisesta mitmendale praamile tahad piletit osta: ")


suuna_URL = "https://www.praamid.ee/portal/ticket/departure?direction=" + suund

#muudab pileti xpathi vastavalt mitmendale praamile piletit ostetakse
nupu_xpathi_tunnus = str(int(mitmes_praam) * 2)
vali_nupu_xpath = "(//button[contains(text(),'Vali')])[" + nupu_xpathi_tunnus + "]" #Nupu xpath

#muudab pileti xpathi vastavalt sellele mitmenda praami peal tahetakse piletit osta
pileti_algne_xpath = "/html[1]/body[1]/app-root[1]/app-ticket-purchase[1]/app-ticket-layout[1]/div[1]/div[2]/div[6]/div[1]/section[1]/app-event-selector[1]/div[1]/div[1]/article[1]/div[3]/div[1]/div[2]/div[1]/div[2]/span[1]"
pileti_xpath_list = list(pileti_algne_xpath)
pileti_xpath_list[145] = mitmes_praam
pileti_XPath = "".join(pileti_xpath_list)

piletite_arv = 0
refreshide_arv = 0

browser = webdriver.Firefox()                                   #Avab veebilehitseja
browser.maximize_window()
browser.get(suuna_URL)                                          #Avab etteantud lehekülje 
element = WebDriverWait(browser, 10).until(                     # Ootab kuni leht laeb vajaliku elemendi
EC.presence_of_element_located((By.XPATH, pileti_XPath)))       
piletite_arv = browser.find_element(By.XPATH, pileti_XPath)     # Leiab piletite arvu
if browser.find_elements(By.XPATH, '/html[1]/body[1]/app-root[1]/app-ticket-purchase[1]/app-ticket-layout[1]/app-footer[1]/app-cookie-notice[1]/div[1]/div[1]/button[1]'):
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, ("/html[1]/body[1]/app-root[1]/app-ticket-purchase[1]/app-ticket-layout[1]/app-footer[1]/app-cookie-notice[1]/div[1]/div[1]/button[1]")))).click()


#Loeme mitmele praamile on võimalik pileteid osta
praamide_arv = len(browser.find_elements(By.TAG_NAME, "h3"))
print(praamide_arv)

#vaatab kohe kas piletite arv on 0
if piletite_arv.text != "0":
    
    #vajutab pileti valimisnupu peale
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, (vali_nupu_xpath)))).click()

    # Valib soodustusega pileti    
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='btn btn--icon btn--primary'])[4]"))).click() 

    #Sisestab isikukoodi
    ootaIK = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@type='resident-0-id'])[1]")))
    isikukoodi_väli = browser.find_element(By.XPATH, ("(//input[@type='resident-0-id'])[1]"))
    isikukoodi_väli.send_keys(IK)

    #Sisestab auto registreerimisnurmbri
    oota_auto = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='vehicleNr'])[1]")))
    auto_reg = browser.find_element(By.XPATH, ("(//input[@id='vehicleNr'])[1]"))
    auto_reg.send_keys(auto)

    #Sisestab emaili
    oota_email =WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
    email_väli = browser.find_element(By.XPATH, ("(//input[@id='email'])[1]"))
    email_väli.send_keys(email)

    #Sisestab telefoni nri
    oota_tel =WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='mobile'])[1]")))
    tel_väli = browser.find_element(By.XPATH, ("(//input[@id='mobile'])[1]"))
    tel_väli.send_keys(tel)

    time.sleep(3)

    #Vajutab jätkamisnuppu
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='btn btn--primary cursor-pointer gap-x-2 grid grid-cols-7']"))).click()
    playsound('C:/Users/Jaagup/Desktop/praamipiletid/alarm.wav')

    #Valib pangalingi
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "(//img[@alt='swedbank'])[1]"))).click()

    #nõustub tingimstega
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/app-root[1]/ng-component[1]/app-ticket-layout[1]/div[1]/div[2]/div[2]/div[1]/div[1]/app-payment-submit[1]/div[1]/div[1]/div[1]/label[1]"))).click()

    #Maksma
    WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/app-root[1]/ng-component[1]/app-ticket-layout[1]/div[1]/div[2]/div[2]/div[1]/div[1]/app-payment-submit[1]/div[1]/div[1]/app-button[1]/a[1]/p[1]"))).click()
    
    print("Palju õnne said pileti!")
    exit()
    
    #Kordab sama asja kuni Piletite arv ei ole enam 0
while piletite_arv.text == "0":

    browser.refresh()
    refreshide_arv += 1
    element = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, pileti_XPath)))
    piletite_arv = browser.find_element(By.XPATH, pileti_XPath)
 

    #Loeb üle mitu praami järjekorras on. Kui on muutunud siis vahetab nupu ja pileti arvu xpathi ära.
    praamide_arv_uus = len(browser.find_elements(By.TAG_NAME, "h3"))
    if praamide_arv != praamide_arv_uus:
        #uuendab praamide arvu ära
        praamide_arv = praamide_arv_uus

        #piletite arvu xpath
        pileti_xpath_list = list(pileti_xpath)
        pileti_xpath_list[145] = str(int(pileti_xpath_list[145]) - 1)
        pileti_XPath = "".join(pileti_xpath_list)


        #Nupu xpath
        nupu_xpathi_tunnus = str(int(nupu_xpathi_tunnus)-2)
        vali_nupu_xpath = "(//button[contains(text(),'Vali')])[" + nupu_xpathi_tunnus + "]" 
        
    
    #Kui piletite arv on nullist erinev hakkab siit programm tööle
    if piletite_arv.text != "0":
        print("sad")
        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, (vali_nupu_xpath)))).click()

        # Valib soodustusega pileti   
        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='btn btn--icon btn--primary'])[4]"))).click()
        
        #Sisestab isikukoodi
        ootaIK = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@type='resident-0-id'])[1]")))
        isikukoodi_väli = browser.find_element(By.XPATH, ("(//input[@type='resident-0-id'])[1]"))
        isikukoodi_väli.send_keys(IK)

        #Sisestab auto registreerimisnurmbri
        oota_auto = WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='vehicleNr'])[1]")))
        auto_reg = browser.find_element(By.XPATH, ("(//input[@id='vehicleNr'])[1]"))
        auto_reg.send_keys(auto)

        #Sisestab emaili
        oota_email =WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        email_väli = browser.find_element(By.XPATH, ("(//input[@id='email'])[1]"))
        email_väli.send_keys(email)

        #Sisestab telefoni nri
        oota_tel =WebDriverWait(browser, 2).until(EC.visibility_of_element_located((By.XPATH, "(//input[@id='mobile'])[1]")))
        tel_väli = browser.find_element(By.XPATH, ("(//input[@id='mobile'])[1]"))
        tel_väli.send_keys(tel)

        time.sleep(3)

        #vajutab jätkamisnuppu
        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[class='btn btn--primary cursor-pointer gap-x-2 grid grid-cols-7']"))).click()


        #Valib pangalingi
        WebDriverWait(browser, 2).until(EC.element_to_be_clickable((By.XPATH, "(//img[@alt='swedbank'])[1]"))).click()

        #nõustub tingimstega
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/app-root[1]/ng-component[1]/app-ticket-layout[1]/div[1]/div[2]/div[2]/div[1]/div[1]/app-payment-submit[1]/div[1]/div[1]/div[1]/label[1]"))).click()

        #Maksma
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/app-root[1]/ng-component[1]/app-ticket-layout[1]/div[1]/div[2]/div[2]/div[1]/div[1]/app-payment-submit[1]/div[1]/div[1]/app-button[1]/a[1]/p[1]"))).click()

        playsound('C:/Users/Jaagup/Desktop/praamipiletid/alarm.wav')

        print(refreshide_arv)
        print("Palju õnne said pileti!")
        exit()



"""
IK = "50112100257"
auto = "395CCF" 
email = "Jaagupkopli1@gmail.com" 
tel = "50112100257"
suund = "HR"
mitmes_praam = "3"


"""
