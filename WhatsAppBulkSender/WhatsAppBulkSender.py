import os
import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoAlertPresentException


#   -> static_itr is used in the send_message() function to maintain the number of iteration
static_itr = 1



#######################################################################################################################################################################
#####################################################################             CLASS           #####################################################################
#######################################################################################################################################################################



class WhatsAppBulkSender:
    #   -> CONSTRUCTOR
    def __init__(self):
        #   -> Making object of Options class
        '''
            -> It allows the webdriver to detach from the session of chrome
               and no longer control it once all the commands are finished.
        '''

        chrome_options = Options()

        #   -> Enabling experimental options
        '''
            -> It allows the webdriver to detach from the session of chrome
               and no longer control it once all the commands are finished.
        
        '''
        chrome_options.add_experimental_option("detach", True)

        #   Launching chrome using chrome web driver in options mode
        self.driver = webdriver.Chrome(options = chrome_options)

        #   Opening whatsapp web
        self.driver.get('https://web.whatsapp.com')


#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

    #   -> Function for checking checkbox of "Keep me signed in"
    '''
        -> This function checks whether checkbox is ticked or not so that
           user remains always logged in.
    '''
    def keep_me_signed_in_tick(self):
         try:
            #   -> Waiting for sometime
             '''
            -> The 'time' module in python provides sleep() function
               which suspends (waits) execution of the current thread for a given number of seconds.
             '''
             # time.sleep(3)

             #  -> Searching for class
             '''
                -> Here we check for the presence of "_2-pPz" which tells us
                   whether the checkbox is ticked or not. By default, on whatsapp
                   web the checkbox is ticked. If it is unticked then, we use
                   click() function to check it.
             '''
             check = self.driver.find_element_by_class_name('_2-pPz')
             check.click()
             print ('clicked the check box')
         except NoSuchElementException:
            #   -> Handling exception
            '''
                -> If we do not find element then "NoSuchElementException"
                   is thrown and following print statement prints on the
                   console.
            '''
            print('checkbox not clicked')
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

    #   -> Checking for user login
    '''
        -> This function checks whether the user has logged in (whether scanned QR code)
           into the whatsapp web using presence of "_1qoA" class.
    '''
    def not_login_check(self):
        #   -> Try-except block
        '''
            -> Following try-except block checks the presence of "_1qoA" class in HTML page
               of whatsapp web. Which basically means that it checks for the login page existance
        '''
        try:
            #   -> Searching for class 
            '''
                -> Here we will search for class "_1qoA" which tells whether
                   user has logged in or not. 
                -> Wait for a maximum of 10 seconds
                   for an element matching the given criteria to be found.
            '''
            login = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, '_1dqoA')))

        except TimeoutException:
            #   -> Handling exception
            '''
                -> If we do not find element then "NoSuchElementException"
                   is thrown and following print statement prints on the
                   console.
            '''
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

    #   -> This function checks whether the user logged-in or not.
    '''
        -> In this function we check the presence of '_34ybp' class. This class represent
           that the user has scanned the QR code and is on home screen of whats app page 
        -> then uses TimeoutException in except block.
    '''
    def login_check(self):
        try:
            #   -> The WebDriverWait function waits 500s for log in(find class) 
            temp = WebDriverWait(self.driver, 500).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, '_34ybp')))
            print('Logged-in Successfully') 
            return True
        except TimeoutException:
            return False
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________
    
    #   -> If the user logged in, the value is true else False
    '''
        -> Following function takes the isLoggedIn value.
           If isLoggedIn is True then we print on console "User logged in" else
           the elif block asks the user if he wants to try
           logging into whatsapp once again.
    '''

    def if_not_logged_in_within_given_time(self, isLoggedIn):
        if isLoggedIn == True:
            print('User logged in')
        elif isLoggedIn == False:
            #   -> user confirmation for more time
            '''
                -> Following input() function asks for user's confirmation.
                   It asks for input and if input is 'y' or 'Y' then login_check()
                   is called. We ask this in a while loop and if user enters any other
                   character other than 'y' or 'Y' then the browser's operation is terminated.
                   And the instance of chrome is closed.
            '''
            print('Do you want more time to log-in: ')
            x = input()
            while x == 'y' or x == 'Y':
                isloggedin = self.login_check()
                if isLoggedIn == True:
                    print('User logged in')
                elif isLoggedIn == False:
                    print('Do you want more time to log-in: ')
                    x = input()
            else:
                #   -> Instance of chrome is closed.
                self.driver.quit()   
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

    #   -> Updating numbers in international format
    '''
        -> We open the INPUTcontacts and add +91 to any number which is not in this format
        -> Then we save all the numbers in another file named UpdatedContacts.txt
    '''

    def update_numbers_in_file(self):

        #   -> Reading file INPUTcontacts.txt

        inputContact = open("INPUTcontacts.txt", "r")

        #   -> Create a new file UpdatedContacts in write mode 
        numberFile = open('UpdatedContacts.txt', 'w')
        #   -> Check whether numbers starting from '+91'
        '''
            -> If numbers starting form '+91' then write it in UpdatedContacts

            -> Otherwise add string '+91' and then write it to UpdatedContacts
        '''
        for eachNumber in inputContact:
            if eachNumber[0]=='+':
                   numberFile.write(eachNumber)
            else:
                   myNumber='+91'+eachNumber
                   numberFile.write(myNumber)

        #   -> Close UpdatedContacts and INPUTcontact file
        numberFile.close()
        inputContact.close()
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

    #   -> In this function we call send_message function for each number
    '''
        -> In this function we send messages from Message.txt to all the numbers in UpdatedContacts.txt file by
           calling send_message() function for each number
    '''        
    def numbers(self):
        #   -> Opening file Message.txt in read mode
        messageFile = open("Message.txt", "r")

        #   -> Variable msg has contents of whole file
        msg = messageFile.read()

        #   -> Open UpdatedContacts file in read mode
        '''
            -> send every number to send_message() function
            -> after sending message we print if message was sent and then close the file
        '''
        numberFile = open('UpdatedContacts.txt','r')
        for eachNumber in numberFile:
            messageSent = self.send_message(eachNumber, msg)
            if messageSent is True:
                print('Message sent to number : %s' % eachNumber)        
        numberFile.close()
        self.driver.close()
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________
            
    #   -> This function sends message to one number
    '''
        -> First it replaces the number in URL -  api.WhatsApp.com/send?phone=number
        -> Then it clicks on few buttons to go to whatsapp chats page 
        -> Then we check if the given number is valid or not, returns false if invalid
        -> We copy paste the message in message box and send the message
    '''
    def send_message(self, x, msg):

        #   -> This is global variable being used in this method
        global static_itr
        
        #   -> Template link for opening link
        s = 'https://api.WhatsApp.com/send?phone=number'
        str = s.replace("number", x)
        print('Sending Message to %s' % x)
        
        #   -> Opening whatsapp web (https://api.WhatsApp.com/send?phone=xxxxxxxxxx)
        self.driver.get(str)
        
        #   -> This block clicks accept in alert generated by whatsapp after sending first message
        '''
            -> If condition checks if the current call of send_message() function is not first call.
               static_itr is used to check the above condition and is incremented after every 
               successful sent message
            -> An alert is generated by whatsapp website after sending first message
            -> We accept the alert (leave page) so as to open other links 
        '''
        try:
            if static_itr > 1:
                alert = Alert(self.driver)
                alert.accept()
        except NoAlertPresentException: 
            print("No alert found !!!")
        
        # time.sleep(20) -> to find alert error

        #   -> Click on "continue to chat" button
        '''
            -> This button comes on the above page

            -> The "#action-button" is the css selector by which
               "continue to chat" button is accessed and we click it
               using click() function
        '''

        self.driver.find_element_by_css_selector("#action-button").click()

        #   -> Click on "use Whatsapp Web" link by searching for link text
        '''
            -> "use Whatsapp Web" link comes after clicking above button
               and we wait provide 10s for page buffering. After this, the
               link "use Whatsapp Web" is found by link text and then it is clicked.
        '''
        btn = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "use WhatsApp Web")))
        btn.click()

        #   -> Checks for div in which it is written "Phone number shared via url is invalid"
        '''
            -> If the number entered is invalid then we find "Phone number shared via url is invalid"
               using class name.
        '''
        invalidNumberCheck = None
        #time.sleep(3)
        try:
            invalidNumberCheck = WebDriverWait(self.driver, 1).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')))
        except TimeoutException:
            # print("invalid number is not found")
            pass

        #   -> If the number is invalid we return False
        '''
            -> If number entered is invalid then we find above string and because that
               string occurs in a box that contains "Ok" button, we click that button to
               close that box.
        '''
        
        if invalidNumberCheck is not None:
            return False
                        
            '''
            ----------------------------------------This code is not needed as next url is loaded--------------------------------------------
                                                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            #   -> Clicks on "Ok" button
            okButton = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "VtaVl")))
            okButton.click()
            print("Ok button clicked because phone number was invalid")
            
            '''

        else:
            #   -> Click on msg box and then copy message, then click send
            '''
                -> This is a css selector for message box "._1JAUF._2x4bz". Then we click on the message box.
                   The "msg" variable has the contents of the message file and we paste the contents
                   of the message in the message box. Then we wait for 1s and press enter using
                   send_keys(Keys.RETURN) method to send the message.
            '''
            try:
                # time.sleep(5)
                messageBox = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))

                messageBox.click()
                
                #   -> this statement copies the contents of the file, copied into variable "msg", on clipboard
                pyperclip.copy(msg)

                messageBox.send_keys(Keys.CONTROL, 'v')

                # time.sleep(1)
                messageBox.send_keys(Keys.RETURN)

                #   -> static_itr is incremented to keep track of number of iteration
                static_itr = static_itr + 1
                
                return True

            except TimeoutException:
                print("couldn't send due to time out exception")
                return False
#_____________________________________________________________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________________________________________________________

































#######################################################################################################################################################################
######################################################################             MAIN           #####################################################################
#######################################################################################################################################################################
            
        
#   -> It is our main function from where the execution starts
if __name__ == '__main__':
    #   -> Here we create our object of WhatsAppBulkSender class
    bulkSender = WhatsAppBulkSender()

    #   -> Calling keep_me_signed_in_check() and login_check()
    bulkSender.keep_me_signed_in_tick()
    bulkSender.not_login_check()
 
    #   -> IsLoggedIn is a flag 
    #   -> Calling login_check() through bulkSender 
    isLoggedIn = bulkSender.login_check()   

    #   -> This function just checks if isLoggedIn value is TRUE. If user needs more time to login. 
    bulkSender.if_not_logged_in_within_given_time(isLoggedIn)
    
    #   -> This function converts the numbers into international format and write it in new file
    bulkSender.update_numbers_in_file()

    #   -> This function reads each contact no. and sends that contact no. to send_message() method
    '''
        -> When send_message() is called, first it checks if the contact no. provided is valid
           or not then send_message() method sends message to each contact no.
    '''
    bulkSender.numbers()

    






