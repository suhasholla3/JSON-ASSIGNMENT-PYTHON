#lets begin with importing standard libraries
import json #well,its a json file ,thus to handle it
import gzip
from collections import Counter #counter function as a utility
import re #to handle regular Expressions

today = 'testtoday.json.gz' #assigning the path of today json file contents to a variable
today_content = []
with gzip.open(today , 'rb') as today_file:
  for tline in today_file:  # Read one line.
        tline = tline.rstrip()
        if tline:  # Any JSON data on it?
            tobj = json.loads(tline)
            today_content.append(tobj)
print(len(today_content)) #returns the length of the today json file

yest = 'testyest.json.gz' #reading today json contents to the variable
yest_content = []
with gzip.open(yest , 'rb') as yest_file:
  for line in yest_file:  # Read one line.
        line = line.rstrip()
        if line:  # Any JSON data on it?
            obj = json.loads(line)
            yest_content.append(obj)
print(len(yest_content))  #returns the length of the yesterday json file

# question 1
#using intersection between two files to check for overlapping of the urlh.
today_list = [item['urlh'] for item in today_content]
today_set = set(today_list)
yest_list = [item['urlh'] for item in yest_content]
yest_set = set(yest_list)
overlap_set = today_set.intersection(yest_set)
overlap_list = [value for value in today_list if value in yest_list] 
print('**************************')
print('Number of urlh in today crawlings ',len(today_list))
print('Unique urlh of today crawlings',len(today_set))
print('Number of urlh in yesterday crawlings',len(yest_list))
print('Unique urlh of yesterday crawlings',len(yest_set))
print('urlh of two days by allowing overlapping inside a single file is ',len(overlap_list)) 
print('Question 1\nThe number of distinct overlapping urlh between two files are ',len(overlap_set))  # Prints the No of URLH which are overlapping between two days crawl.



#Question 2  For all the URLH which are overlapping, calculate the price difference (wrt available_price) if there is any between yesterday's and today's crawls. There might be duplicate URLHs in which case you can choose the first valid (with http_status 200) record.

def overlap(today_content, yest_content):   # here overlap function does the price difference estimation alongside with a condition http_status as 200 (first valid)
    new_list = []
    set_1 = set()
    list_1 =[]
    count_http = set()
    s = 0
    for x in today_content:
        for y in yest_content:
            if (x['urlh'] == y['urlh']) :
              if x['available_price'] == y['available_price']:
                 pass
              else :  
                if x['http_status'] == '200' and x['http_status'] not in count_http :
                  count_http.add(x['http_status'])
                  set_1.add(x['urlh'])
                  list_1.append(x['urlh'])
                  s = float(x['available_price']) - float(y['available_price'])
                  print("Question 2")
                  if s < 0:
                    print( 'The available Price today is decreased to rs', float(x['available_price']) ,'from yesterday rs',float(y['available_price']),'with a decrease of rs',s,'for urlh', x['urlh'])
                  else :
                    print( 'The available Price today is increased to  Rs',float(x['available_price']) ,'from yesterday rs',float(y['available_price']),'with an increase of rs',s,'for urlh', x['urlh'])
                  new_list.append(x)
            else :
                pass
    #print( len(set_1) , len(list_1),count_http)
    print("The total number of overlapping urlh's  :",len(new_list))
    return new_list  #Returns the complete items of the urlh associated along with its length 
    
overlap(today_content,yest_content)

#Question 3
#NO of unique categories in two files 

#number of unique categories in today and yesterday crawls.
cat = [d['category'] for d in today_content]  
categories_today = set(cat)  #sets advantage is it takes only unique element
caty = [d['category'] for d in yest_content]
categories_yest = set(caty)
print('Number of unique categories in yesterday file is ' , len(categories_yest),'and the categories are',categories_yest)
print('Number of unique categories in today file is ' , len(categories_today),categories_today)

#checking the length and verifying if both files have the same categories.
print(len(categories_today) == len(categories_yest) and categories_today == categories_yest)
#The unique categories present in both the files 
categories_unique = categories_today.intersection(categories_yest)
print("Question 3.\n No. of unique categories in both files:(overlapping) is ", len(categories_unique))

#Question 4
# List of categories which is not overlapping.
categories_total = cat + caty
print(" List of categories which is not overlapping: ", list(set(categories_total).difference(categories_unique)))
nonoverlap = list(categories_today.difference(categories_yest))
print('QUestion 4.\n The number of non overlapping categories in both the files are ', len(nonoverlap))

#Generate the stats with count for all taxonomies (taxonomy is concatenation of category and subcategory separated by " > ").

cat_t,subcat_t,cat_y,subcat_y =([] for i in range(4)) # Creating lists of categories and subcategories
for item in today_content:  
    cat_t.append(item['category'])
    subcat_t.append(item['subcategory'])

for item in yest_content:
    cat_y.append(item['category'])
    subcat_y.append(item['subcategory'])

subcat_set = set(subcat_t).intersection(subcat_y) #creating a set which contains common subcategories in both the files
subcat_total = subcat_t + subcat_y #creating a set which contains subcategories of both the files
crawl_total = today_content + yest_content #total list of today_contents and yesterday's contents
subcat_dict = Counter(subcat_total) #create a dictionary of sub categories along with the frequency of how many times it has occured.
print("Question 5. The Taxonomies of category and subcategories are: ")
for item in crawl_total:
    if item['category'] in categories_unique and item['subcategory'] in subcat_set:  #checking if the categories are present in unique categories set
        print(item['category'] + " > " + item['subcategory'] + ": " + str(subcat_dict[item['subcategory']])) #printing category and subcategory along with the dictionary of subcategory and its counts.
        subcat_set.remove(item['subcategory']) 


#6. Generate a new file where mrp is normalized. If there is a 0 or a non-float value or the key doesn't exist, make it "NA".
today_mrp_list = [] 
yest_mrp_list =[]
for item in today_content:
        try:
            if (item["mrp"] == "0") or (re.match("^\d+?\.\d+?$", item["mrp"]) is None) or (item["mrp"] == None):
              item["mrp"] = "NA"
        except TypeError:
              item["mrp"] = "NA" #normalising
        today_mrp_list.append(item) #appending the result to the today's mrp list.
for item in yest_content:
        try:
            if (item["mrp"] == "0") or (re.match("^\d+?\.\d+?$", item["mrp"]) is None) or (item["mrp"] == None):
              item["mrp"] = "NA"
        except TypeError:
              item["mrp"] = "NA" #normalising
        yest_mrp_list.append(item)  #appending the result to the yesterday's mrp list.

#writing the output to a new json file by creating two new files.
open("mrp_today.json", 'a').close()
open("mrp_yesterday.json", 'a').close()

with open("mrp_today.json", "w") as f:
    json.dump(today_mrp_list, f) #writing today's mrp list contents to a file 

with open("mrp_yesterday.json", "w") as f:
    json.dump(yest_mrp_list, f)  #writing yesterday's mrp list contents to a file 

print("Question 6\n For normalised MRP Check the files in which will be saved in your system with mrp_today and mr_yesterday as filename")
#output will be present in the new files once created. 

print('*********************************************THANK YOU :) ****************************************')

