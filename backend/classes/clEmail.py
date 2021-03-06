from email.message import EmailMessage
import ssl
import smtplib
# tutorial for how you do it : https://www.youtube.com/watch?v=g_j6ILT-X0k
email = "smart.fridge.bot@gmail.com"  # put your chosen e-mail here
passwd = "ixpthvqvkktgitgi"  # put your password here
emailme = "lucas03dewil@gmail.com"

sub = "Expired dates!"
em = EmailMessage()
em['From'] = email
# lucas03dewil@gmail.com"
em['Subject'] = sub


class emailPy:
    def __init__(self,  dates, emailToSend="lucas03dewil@gmail.com") -> None:
        self.expired = dates
        self.body = ""
        self.emailme = emailToSend
        em['To'] = self.emailme
        self.send_mail()

    def send_mail(self):
        self.body = "Hi there! These are the products that expired today: "
        self.teller = 1
        for product in self.expired:
            self.body += f"\n{self.teller}-{product['Naam']},{product['HoudbaarheidsDatum']}"
            self.teller += 1
        em.set_content(self.body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email, passwd)
            smtp.sendmail(email, self.emailme, em.as_string())
        del em['To']
