import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.com/Synology-DS418play-Station-4-bay-Diskless/dp/B075ZNKCK4/ref=cm_cr_arp_d_product_sims?ie=UTF8'

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def check_price():

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    soup2 = BeautifulSoup(soup.prettify(), "html.parser")

    title = soup2.find(id= "productTitle").get_text()
    price = soup2.find(id= "priceblock_ourprice").get_text()
    converted_price = float(price[1:4])

    if(converted_price < 450):
        send_mail()

    print(converted_price)
    print(title.strip())

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('jperkinator@gmail.com', 'xvxyiwxftvbmtjgx')

    subject = 'Price fell down!'
    body = 'Check the Amazon link https://www.amazon.com/Synology-DS418play-Station-4-bay-Diskless/dp/B075ZNKCK4/ref=cm_cr_arp_d_product_sims?ie=UTF8'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'jperkinator@gmail.com',
        'jeremy.perkins99@gmail.com',
        msg
    )
    print('Email has been sent.')



while(True):
    check_price()
    time.sleep(60*60)
