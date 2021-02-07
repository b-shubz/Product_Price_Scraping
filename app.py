
from flask import Flask, request, render_template
from bs4 import BeautifulSoup as soup
import urllib
import requests

app = Flask(__name__)


def flipkart(product=None):
    base_url='https://www.flipkart.com'

    #product='samsung galaxy s20 128 gb'
    #product=input('Enter product : ')
    try:
        product=product.replace(' ','%20')

        url=base_url+'/search?q='+product

        with urllib.request.urlopen(url) as url:
            page = url.read()

        html_data=soup(page, "html.parser")

        #print(html_data)

        name=html_data.find("div",{"class":"_4rR01T"})
        link=base_url+html_data.find('a',{'class':'_1fQZEK'})['href']
        price=html_data.find('div',{'class':'_30jeq3 _1_WHN1'})

        print(name.text)
        print(price.text)
        return  ['Flipkart',price.text,name.text,link]
    except:
        print('Wrong input flipkart')
        return None

def amazon(product=None):
    base_url='https://www.amazon.in'

    #product='samsung galaxy s20 128 gb'
    #product=input('Enter product : ')

    try:
        product=product.replace(' ','+')

        url=base_url+'/s?k='+product

        with urllib.request.urlopen(url) as url:
            page = url.read()

        html_data=soup(page, "html.parser")

        #print(html_data)

        name=html_data.find("span",{"class":"a-size-medium a-color-base a-text-normal"})
        link=base_url+html_data.find('a',{'class':'a-link-normal a-text-normal'})['href']
        price=html_data.find('span',{'class':'a-price-whole'})

        print(name.text)
        print(price.text)
        return ['Amazon',price.text,name.text,link]
    except:
        print('Wrong Input amazon')
        return None



@app.route('/result', methods=['POST'])
def result():
    product = request.form['product']
    print(product)
    flipkart_data=flipkart(product)
    amazon_data=amazon(product)
    fk_price=None
    if flipkart_data:
        fk_price=float(flipkart_data[1][1:].replace(',',''))
    amz_price=None
    if amazon_data:
        amz_price=float(amazon_data[1].replace(',',''))
    data_set=[]
    if fk_price and amz_price:
        if fk_price < amz_price:
            data_set.append(flipkart_data)
            data_set.append(amazon_data)
        else:
            data_set.append(amazon_data)
            data_set.append(flipkart_data)
    elif fk_price:
        data_set.append(flipkart_data)
    elif amz_price:
        data_set.append(amazon_data)

    print(fk_price)
    print(amz_price)
    print(data_set)

    return render_template('result.html',data=data_set)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)