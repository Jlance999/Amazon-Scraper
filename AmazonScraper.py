import requests
from bs4 import BeautifulSoup
import smtplib
import time
from decimal import Decimal

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

import tkinter as tk

import os

mainDir = "C:\\Users\\Jeremy\\Documents\\GitHub\\Amazon Scraper\\"
    
def check_price():
    
    URL = 'https://www.amazon.com/Synology-DS418play-Station-4-bay-Diskless/dp/B075ZNKCK4/ref=cm_cr_arp_d_product_sims?ie=UTF8'

    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    # for use in debugging 
    # print(soup)

    soup2 = BeautifulSoup(soup.prettify(), "html.parser")

    #Scraping title and price of product from parser.
    title = soup2.find(id= "productTitle").get_text()
    price = soup2.find(id= "priceblock_ourprice").get_text()
    converted_price = Decimal(price.strip('$'))
    stripped_title = title.strip()
    
    # Filtering down to the closs that holds all of the image information
    imgs = soup2.find('div', class_='imgTagWrapper')
    # For debugging print('imgs= ',imgs)


    # Filtering down to the direct product image url.
    imgsurl = imgs.find('img', class_='a-dynamic-image') ['data-a-dynamic-image']
    imgsurl = imgsurl.split('"')
    imgsurl = imgsurl[1]
    print('imgsurl= ',imgsurl)



    if(converted_price < 425):
        send_mail()

    print(converted_price)
    print(title.strip())
    
    setupDir(str(stripped_title))
    storeDataTxt(str(stripped_title),str(converted_price))
    storeImagePng(str(stripped_title),imgsurl)

def storeImagePng (product,imgsurl):

    r = requests.get(imgsurl)

    imageDataDir=mainDir + '//' + product + '//'
    imageData = open(imageDataDir+'image.gif', "wb")
    imageData.write(r.content)
    print('Image saved to Directory.')

def storeDataTxt (product,price):
    #Toying with storing data to txt files. Not sure if I will use this or another method, but I want to be able to see price changes over time.
    
    from time import strftime, localtime

    priceDataDir= mainDir + '//' + product + '//' +"priceData.txt"
    priceData = open(priceDataDir, "a")
    priceData.write(strftime("%d%b%y", localtime()))
    priceData.write(',')
    priceData.write(price)
    priceData.write('\n')
    priceData.close()

def setupDir(product):
    
    if (os.path.isdir(mainDir + '//' + product) ==False):
        os.mkdir(mainDir + product)
        os.mkdir(mainDir + product + '//' +'productImages')
        titleDataDir=mainDir + '//' + product + '//' +"productData.txt"
        titleData = open(titleDataDir, "a")
        titleData.write(product)
        titleData.close()

    else:
        print("Directory already exists.")

def graph():
    style.use('dark_background')

    fig = plt.figure() #creating a subplot
    ax1=fig.add_subplot(1,1,1)

    def animate(i):

        priceDataDir= mainDir + ''
        data = open(priceDataDir,'r').read()
        lines = data.split('\n')
        xs = []
        ys = []

        for line in lines:
             if len(line) > 1:
                x, y = line.split(',') # Delimiter is comma
                xs.append((x))
                ys.append(float(y))

        ax1.clear()
        ax1.plot(xs,ys)

        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Live Graph')

        #adds major gridlines
        ax1.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)

    
    ani=animation.FuncAnimation(fig, animate, interval=1000) 
    plt.show()

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('jperkinator@gmail.com', SERVER_PW)

    subject = 'Price change!'
    body = 'Check the Amazon link https://www.amazon.com/Synology-DS418play-Station-4-bay-Diskless/dp/B075ZNKCK4/ref=cm_cr_arp_d_product_sims?ie=UTF8'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'jperkinator@gmail.com',
        'jeremy.perkins99@gmail.com',
        msg
    )
    print('Email has been sent.')

def GUI ():
    from PIL import Image, ImageTk

    root = tk.Tk()
    root.title("Amazon Scraperino")
    cHeight=500
    cWidth=800

    canvas = tk.Canvas(root, height=cHeight, width=cWidth)
    canvas.pack()

    
    # Master frame
    frame = tk.Frame(root, bg='#1f1f1f')
    frame.place(relwidth=1, relheight=1)

    # List to hold currently indexed products
    productList = [
        'Synology DS418play',
        'Sweet Cell Phone Case',
        'Arduino'
    ]

    # Dropdown for product selection
    var=tk.StringVar()          # Holds current selection
    var.set(productList[0])        # Sets Default Selection

    # Configuring actual drop down position.
    productSel= tk.OptionMenu(frame, var, *productList)     #Configuring actual drop down
    productSel.place(anchor='s', relx=.75, rely=.25)


    # Frame to hold image label
    frameInner = tk.Frame(frame, bg= "#282828")
    frameInner.place(anchor='nw', relwidth=.4, relheight=.5)

    def resize_image(event):
        new_width = event.width
        new_height = event.height
        image = copy_of_image.resize((new_width, new_height))
        photo = ImageTk.PhotoImage(image)
        labelImage.config(image = photo)
        labelImage.image = photo #avoid garbage collection

    image = Image.open("C:\\Users\\Jeremy\\Documents\\GitHub\\Amazon Scraper\\image.png")
    copy_of_image = image.copy()
    photo = ImageTk.PhotoImage(image)
    labelImage = tk.Label(frameInner, image=photo)
    labelImage.bind('<Configure>', resize_image)
    labelImage.pack()

  
    # Stores command=function_name to run a function
    button = tk.Button(frame, text="See Graph", bg='gray', command=graph)
    button.place(anchor='s', relx=.5, rely=.99)

    labelPrice = tk.Label(frame, text= "Current Price: ", bg='#1f1f1f', fg='white')
    labelPrice.place(relx=.7, rely=0)

    labelNotifPrice = tk.Label(frame, text= "Notification Price: ", bg='#1f1f1f', fg='white')
    labelNotifPrice.pack()



    # Entry pane to change notification price.
    entry = tk.Entry(frame, bg='green')
    entry.pack()

    #os.mkdir(mainDir + product)
    #print("Folder "+ product +" added to program directory to store product data.")
    root.mainloop()

GUI()


##while(True):
##    check_price()
##    time.sleep(60*60)
