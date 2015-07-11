__author__ = 'jlansey'

import urllib
import time
import re
import csv

from bs4 import BeautifulSoup


def main():

    name = "data/projects_subset.csv"
    # name = "data/projects.csv"

    project_list =list(csv.reader(open(name),quoting = 1))
    headers = project_list[0]

    output_file = open('data/output.csv','w')


    output_header = write_csv_line('this_id','backernum','reward_price','reward_shipping','max_back','launch','deadline')+"\n"
    output_file.write(output_header) # python will convert \n to os.linesep

    # prepare some regex stuff
    # find_currency = re.compile('data-currency=\"(.*?)\"')
    # find_currency = re.compile('([$])')
    extract_number = re.compile("\d+")


    # index for looping over pages
    ii=1
    this_url = project_list[ii][headers.index('web_url')]+"/description"

    # Example URL with some sold out and limited items
    # this_url = "http://www.kickstarter.com/projects/lansey/loud-bicycle-car-horns-for-cyclists/description"
    # british example:
    # this_url =  "https://www.kickstarter.com/projects/1558089494/thunderbirds-1965-new-episodes-from-1960s-recordin?ref=city"

    this_id = project_list[ii][headers.index('id')]
    launch = project_list[ii][headers.index('launched_at')]
    deadline =project_list[ii][headers.index('deadline')]


    read_failed = True
    # read in the html file
    while read_failed:
        try:
            html = urllib.urlopen(this_url).read()
            read_failed = False
        except:
            print("we had an error reading in the url, what do")
            time.sleep(60*1)

    bs = BeautifulSoup(html)

    all_rewards_text = bs.find_all("div","NS_projects__rewards_list js-project-rewards")[0]
    reward_struct = all_rewards_text.find_all("div","NS_backer_rewards__reward p2")

    for this_reward in reward_struct:

        # number of people who backed at this reward level
        backernum_str = this_reward.find_all("span","num-backers mr1")[0].contents[0].strip()
        backernum = extract_number.findall(backernum_str)[0]

        # the dates that the reward will ship
        reward_shipping = this_reward.find_all("time","invisible-if-js js-adjust-time")[0].contents[0].strip()

        # cost of this reward level
        reward_price = this_reward.find_all("h5","mb1")[0].contents[0].strip()

        # find the maximum number of backers possible
        sold_out = this_reward.find_all("span","bg-grey no-wrap pl1 pr1 sold-out")

        max_back =  "replace this"
        if len(sold_out)>0: # it is sold out wooo
            max_back = backernum
        else: # not sold out
            limited = this_reward.find_all("span","limited-number")
            if len(limited)>0: # it is limited oooh
                lim_str = limited[0].contents[0].strip()
                # the second number is the one "Limited (118 left of 140)"
                max_back = extract_number.findall(lim_str)[1]
            else: # no limit present
                max_back = "-1" # initialize to -1 for no maximum required

        to_print = write_csv_line(this_id,backernum,reward_price,reward_shipping,max_back,launch,deadline)+"\n"

        output_file.write(to_print)

    output_file.close()


# For each reward level save:
#     print(this_id,backernum,reward_price,reward_currency,reward_shipping,launch,deadline)


#
#
# #   the dates that the reward will ship
#     reward_shipping = all_times[:-2]
#
# # the dates of the campaign
#     campaign_start = all_times[-2]
#     campaign_end = all_times[-1]
#
    # reward_number = bs.find_all("span","num-backers mr1")



# #    We need the reward limit whether it was sold-out or not sold out
# #     sold out reward levels:
#     bs.find_all("span","bg-grey no-wrap pl1 pr1 sold-out")
# #     limited number rewards left.
#     bs.find_all("span","limited-number")
#



# Additional variables:
# max_reward, the maximum number that can be sold of each reward level. default -1.


def write_csv_line(*args):
    return '"' + reduce(lambda x,y: x + '","' + y ,args) + '"'



# Not using this anywhere
def grep(s,pattern):
    return '\n'.join(re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M))



if __name__ == "__main__":
    main()















