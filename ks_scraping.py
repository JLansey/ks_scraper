__author__ = 'jlansey'

# import urllib
# from mailer import *
import time, csv

def main():

    name = "projects_subset.csv"

    list(csv.reader(open(name),quoting =1))


    while flag_color != 'Y':
        # print("flag color not yellow")
        print(flag_text)
        link = "https://portal2.community-boating.org/pls/apex/CBI_PROD.FLAG_JS"
        try:
            flag_text = urllib.urlopen(link).read()
            # flag_text = f.read()
            flag_color = flag_text[18:19]
            time.sleep(60*10)
        except:
            print("we had an error reading in the javascript file")
            time.sleep(60*10)

    str = mailer('lansey@gmail.com','FlagStatus is: ' + flag_color,"")
    print(str)
    print("yay flag color is YELLOW!")

if __name__ == "__main__":
    main()