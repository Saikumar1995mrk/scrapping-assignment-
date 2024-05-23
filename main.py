from isbntools.app import *
import pandas as pd
import csv 

def generate_booktopia_urls(input_file_path):
    input_df=pd.read_csv(input_file_path)
    # input_df=input_df.head(50)
    invalid_isbn=[]
    all_valid_urls=[]
    all_valid_isbn=[]
    with open("fianl_urls.csv", mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ISBN', 'URL'])

    for index, row in input_df.iterrows():  
        isbn=str(row["ISBN13"])
        print(isbn)
        try:
            meta_dict = meta(isbn, service='goob')  # Use Google Books service
            if meta_dict:
                title = meta_dict['Title'].strip().replace(" " , "-")
                authors = meta_dict['Authors']
                if len(authors)==1:
                    authors = meta_dict['Authors'][0].strip().replace(" " , "-")
                    valid_url=f"https://www.booktopia.com.au/{title}{authors}/book/{row['ISBN13']}.html" 
                    all_valid_urls.append(valid_url)
                    all_valid_isbn.append(isbn)
                    with open("fianl_urls.csv", mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([isbn, valid_url])
       
                else:
                    authors = meta_dict['Authors'][0].strip().replace(" " , "-")
                    valid_url=f"https://www.booktopia.com.au/{title}{authors}/book/{row['ISBN13']}.html" 
                    all_valid_urls.append(valid_url)
                    all_valid_isbn.append(isbn)
                    with open("fianl_urls.csv", mode='a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([isbn, valid_url ])
       

        except:
            invalid_isbn.append(isbn)
            pass

    print(len(all_valid_urls),len(invalid_isbn))


if __name__ == '__main__':
    generate_booktopia_urls(r"D:\scrapping assingment\input_list.csv")
