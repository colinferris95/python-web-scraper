import urllib.request
from bs4 import BeautifulSoup
import json
import time

#4100

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def openPage(page_number,category):	   
    url = "https://www.ewg.org/skindeep/browse.php?"
    #download the URL and extract the content to the variable html 
    t0 = time.time()
    request = urllib.request.Request(url+category+page_number,headers=hdr)
    html = urllib.request.urlopen(request).read()
    response_delay = time.time() - t0
    time.sleep(20*response_delay )

    #pass the HTML to Beautifulsoup.
    soup = BeautifulSoup(html, 'lxml')
    #get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("table",attrs={'id':'table-browse'})
    #Now we go into main_table and get every a element in it which has a class "title" 
    #name_cell = soup.find("td",attrs={'class': 'product_name_list'})
    
    links_whole = main_table.find_all("td", attrs={'class':'product_name_list'})
	
    return links_whole

	
    #from each link extract the text of link and the link itself
    #List to store a dict of the data we extracted 
main_extracted_records = []	
ingrdients_extracted_records = []
def scrapeSite(startingNum,category):
    full_links = openPage(startingNum,category)
	
    
    for links in full_links:

        link = links.find("a")
        title = link.text
        url = link['href']

        if not url.startswith('http'):
            url = "https://ewg.org"+url
    
	
        request = urllib.request.Request(url,headers=hdr)	
        html = urllib.request.urlopen(request).read()	
        time.sleep(7)
        soup = BeautifulSoup(html,'html.parser')



        print(url)
        print(url.split('/'))
        url_array = url.split('/')
        product_id = url_array[5]
		

		
        img_area = soup.find('div', attrs={'class':'right2012product_left'})
        prod_img = img_area.find('img')
        print(prod_img['src'])
		
        infos_area = soup.find('div', attrs={'id':'Ingredients'})
        #infos = infos_area.find_all('tr')
        infos_first = infos_area.find_all('td', attrs={'class': 'firstcol'})
        infos_concerns = infos_area.find_all('td', attrs={'width': '320'})
        info_data = infos_area.find_all('div', attrs={'id': 'score_style_small'})
        info_score = infos_area.find_all('img')
		
		
        extracted_info_score = ""
        for (score,ingredient,concern,data) in zip(info_score,infos_first,infos_concerns,info_data):
            score_img = score['src']

            if 'https://static.ewg.org/skindeep/img/draw_score/score_image1__1_.png' == score_img:
                score_img = 1

            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image2__1_.png' == score_img:
                score_img = 2

            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image3__1_.png' == score_img:
                score_img = 3

            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image4__1_.png' == score_img:
                score_img = 4


            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image5__1_.png' == score_img:
                score_img = 5


            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image6__1_.png' == score_img:
                score_img = 6

            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image7__1_.png' == score_img:
                score_img = 7
				
            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image8__1_.png' == score_img:
                score_img = 8	
			
            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image9__1_.png' == score_img:
                score_img = 9	
			
            elif 'https://static.ewg.org/skindeep/img/draw_score/score_image10__1_.png' == score_img:
                score_img = 10					






            extracted_info_score = score_img
		    
            print(score_img)
		
        
            ingredient_text = ingredient.find('a').text
            extracted_info_ing = ingredient_text
            #extracted_info.append({'ingredient':ingredient})
            print(ingredient_text)	
	
	
        
            concern_text = concern.text
            extracted_info_concern = concern_text
        
            print(concern_text)
	
        
            data_text = data.find('span').text
            extracted_info_data = data_text
        
            print(data_text)
			
            ingredient_record = {
                'title':title,
                'product_id':product_id,				
                'ingredients':extracted_info_ing,
		'concerns':extracted_info_concern,
		'data':extracted_info_data,
		'score':extracted_info_score
		
		}
            ingrdients_extracted_records.append(ingredient_record)
     


        main_record = {
            'title':title,
            'product_id':product_id,
            'url':url,
	    'img':prod_img['src']
            }
			
		
        main_extracted_records.append(main_record)
	
	
    #print(extracted_records)

def runScrape(items):
    #aftersun
    scrapeSite(str(items),"category=after_sun_product&&showmore=products&atatime=")
	#anti-aging
    scrapeSite(str(items),"category=anti-aging&&showmore=products&atatime=")	
    #around-eye	
    scrapeSite(str(items),"category=around-eye+cream&&showmore=products&atatime=")	
    #body-firm	
    scrapeSite(str(items),"category=body+firming+lotion&&showmore=products&atatime=")
    #body-oil
    scrapeSite(str(items),"category=body+oil&&showmore=products&atatime=")	
	#facial-moisturizer
    scrapeSite(str(items),"category=facial+moisturizer;;treatment&&showmore=products&atatime=")
    #foot-moisturizer
    scrapeSite(str(items),"category=foot+moisturizer&&showmore=products&atatime=")	
    #hand+cream
    scrapeSite(str(items),"category=hand+cream&&showmore=products&atatime=")
    #moisturizer	
    scrapeSite(str(items),"category=moisturizer&&showmore=products&atatime=")	
	
	

runScrape(5000)		
with open('main_facial_moisturizer.json', 'w') as outfile:
    json.dump(main_extracted_records,outfile)
	
with open('ingredients_facial_moisturizer.json', 'w') as outfile:
    json.dump(ingrdients_extracted_records,outfile)
