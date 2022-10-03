from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class ControlBrowser:
    def __init__(self, driver_path="chromedriver.exe"):
        """Crea una clase para controlar el navegador.
        - driver_path: Ruta de la ubicación del driver de chrome
        """
        self.driver_path = driver_path   
        self.driver:webdriver.Chrome = None    #es None porque lo creo despues

    def send_data(self, xpath:str, value:str|int):          
        """
        Escribe sobre un input según el xpath indicado.
        - xpath: xpath del input donde se escribirá
        - value: valor que se enviará al input
        return None
        """
        element = self.driver.find_element("xpath",xpath)
        element.send_keys(value)

    
    def get_urls(self, xpath:str):
        urls_list = self.driver.find_elements("xpath", xpath)
        return [ url.get_attribute('href') for url in urls_list]

    def get_data(self):
        #Esta funcion encuentra cada elemento segun su xpath y devuelve en una lista los valores. 
        direccion = self.driver.find_element("xpath", "//*[contains(text(),'Dirección')]//parent::p")
        email = self.driver.find_element("xpath","//*[contains(text(),'mail')]//parent::p")
        tel = self.driver.find_element("xpath","//div[@id='main-content']//*[contains(text(),'Tel')]//parent::p")
        fax= self.driver.find_element("xpath","//div[@id='main-content']//*[contains(text(),'Fax')]//parent::p")
        web = self.driver.find_element("xpath","//div[@id='main-content']//*[contains(text(),'www')]//parent::p")

        return [
            direccion.text, 
            email.text, 
            tel.text, 
            fax.text, 
            web.text
        ]


    def open_browser(self, url:str):
        self.driver = webdriver.Chrome(self.driver_path)   
        self.driver.maximize_window() #maximiza la ventana
        self.driver.get(url)  #direccion abierta


if __name__ == "__main__":
    #inicializar clase:
    browser = ControlBrowser()
    #abrir navegador
    browser.open_browser("http://rivieramaya.org.mx/hoteles/")
    
    #guardar las urls de todo el sitio web
    list_urls = []
    #aceptar cookies para que no moleste y me deje dar click al otro boton
    try:
        browser.driver.find_element("xpath","//*[@id='cn-accept-cookie']").click()
    except:
        pass
    #cambio de pagina
    for _ in range(100):
        sleep(1)
        #guardo las urls de los hoteles (primeras 15 por pagina)
        list_urls +=  browser.get_urls("//article/h2/a")
        try:
            #encontrar el boton siguiente y esperar a que el boton de siguiente este presente en la pag
            button_sig = WebDriverWait(browser.driver, 20).until(EC.element_to_be_clickable(("xpath","//a[@rel='next']")))
            sleep(0.5)
            #dar click
            button_sig.click()
            
        except Exception as e:
            print(e)
            break
    
    #separo las urls una por una
    for url in list_urls:
        #abrir cada url
        browser.driver.get(url)
        #encontrar elemento y retornar su valor y lo guardo en 'data'
        data = browser.get_data()
        print(data)

    #cerrar el navegador
    browser.driver.close()  






