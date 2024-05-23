# pip install zenrows
from zenrows import ZenRowsClient
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd 
import csv 




def book_scrapper(url_file_path):
    client = ZenRowsClient("0e5fd4dedc39a6f0bf239e42bdfaeae3106fe39d")
    params = {"js_render":"true","premium_proxy":"true"}
    urls=pd.read_csv(url_file_path)
    urls=urls[:50]
    df = pd.DataFrame()
    with open("fianl_res.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Author', 'Book Type', 'Original Price', 'Discount Price', 'ISBN-10', 'Published Date', 'Publisher', 'No Of Pages' ,'URL'])

    for index, row in urls.iterrows():
        url=row["URL"]
        response = client.get(url, params=params)
        soup = BeautifulSoup(response.content, 'html.parser')
        if response.status_code==200:
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag:
                # Extract the JSON content
                try:
                    json_content = script_tag.string
                    data = json.loads(json_content)
                    title = data[0]['name']
                    author = data[0]['author'][0]['name']
                    bookFormat = data[0]['workExample']['bookFormat'].split("/")[-1]
                    discount_price = data[0]['offers'][0]['price']
                    isbn = data[0]['workExample']['isbn']
                    datePublished = data[0]['workExample']['datePublished']
                    Publisher = data[0]['brand']['name']
                    span = soup.find('span', class_='strike', title='Recommended Retail Price')
                    if span:
                        original_price = span.get_text()
                        print(original_price)

                    div_element = soup.find(class_="MuiButtonBase-root MuiTab-root MuiTab-labelIcon MuiTab-textColorInherit mui-style-ax6ycu")
                    if div_element:
                        text_content = div_element.get_text()
                        pages_text = None
                        for line in text_content.split('\n'):
                            if 'Pages' in line:
                                pages_text = line
                                pages = ''.join([char for char in pages_text if char.isdigit()])
                                break
                            else:
                                pages=" "
                                break
                except:
                    pass
                else:
                    print("No element with the pages ")
            else:
                print("json is not present ")

            print(title,"\n",author,"\n","\n",bookFormat,"\n",discount_price,"\n",isbn,"\n",datePublished,"\n",Publisher,"\n",pages)
         # Append the book data to the CSV file
            with open("fianl_res_50.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([title, author, bookFormat,original_price , discount_price ,isbn, datePublished, Publisher,pages , url ])
        else:
            print("Not a valid url & zen rows key expired")

if __name__ == '__main__':
    book_scrapper(r"D:\scrapping assingment\fianl_urls.csv")
