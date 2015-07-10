__author__ = 'jlansey'

import urllib
import time
import re
import csv

from bs4 import BeautifulSoup


def main():

    name = "data/projects_subset.csv"
    # name = "data/projects.csv"

    project_list =list(csv.reader(open(name),quoting = qt))
    headers = project_list[0]

    url_idx = headers.index('web_url')
    id_idx = headers.index('kickstarter_id')



    # index for looping over pages
    ii=1
    this_url = project_list[ii][url_idx]+"/description"

    # Example URL with some sold out and limited items
    # this_url = "http://www.kickstarter.com/projects/lansey/loud-bicycle-car-horns-for-cyclists/description"

    this_id = project_list[ii][id_idx]


    # read in the html file
    try:
        html = urllib.urlopen(this_url).read()

    except:
        print("we had an error reading in the url, what do")
        time.sleep(60*10)


    # bs = BeautifulSoup(urllib.urlopen(html))
    bs = BeautifulSoup(html)

    # cost of this reward level
    reward_price =bs.find_all("h5","mb1")[1:]
    #number of people who backed at this reward level
    reward_number = bs.find_all("span","num-backers mr1")

    all_times= bs.find_all("time","invisible-if-js js-adjust-time")


#   the dates that the reward will ship
    reward_shipping = all_times[:-2]

# the dates of the campaign
    campaign_start = all_times[-2]
    campaign_end = all_times[-1]

    reward_number = bs.find_all("span","num-backers mr1")

    # Find the currency (str)
    these_regex='data-currency=\"(.*?)\"'
    pattern=re.compile(these_regex)

    reward_currency = pattern.findall(html)[0]

#    We need the reward limit whether it was sold-out or not sold out
#     sold out reward levels:
    bs.find_all("span","bg-grey no-wrap pl1 pr1 sold-out")
#     limited number rewards left.
    bs.find_all("span","limited-number")

# For each reward level save:
    print(this_id,reward_price, reward_number, reward_currency,reward_shipping,campaign_start,campaign_end)

# Additional variables:
# max_reward, the maximum number that can be sold of each reward level. default -1.





# Not using this anywhere
def grep(s,pattern):
    return '\n'.join(re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M))



if __name__ == "__main__":
    main()















