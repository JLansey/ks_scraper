__author__ = 'jlansey'

import urllib
import time
import re
import csv
import unicodedata
# import os.path
import os


from bs4 import BeautifulSoup


def main():

    # name = "data/projects_subset.csv"
    name = "data/projects.csv"
    d_dir = "html/"

    # name = "data/projects.csv"

    # project_list =list(csv.reader(open(name),quoting = 1))
    # headers = project_list[0]
    #
    #
    # # first download all the files.
    # #  index for looping over pages
    # for ii in range(1,len(project_list)):
    #     try:
    #         this_id = project_list[ii][headers.index('id')]
    #         this_file_path = os.path.join(d_dir,this_id + ".html")
    #         if os.path.isfile(this_file_path):
    #             print("skipping file: " + this_id)
    #         else: # download this file yo
    #                 this_url = project_list[ii][headers.index('web_url')]+"/description"
    #                 try:
    #                     html = urllib.urlopen(this_url).read()
    #
    #                     ks_file = open(this_file_path,'w')
    #                     ks_file.write(html)
    #                     ks_file.close()
    #                     time.sleep(.25)
    #                     print('loaded project ' + str(ii) + "/" + str(len(project_list)))
    #                 except:
    #                     print("we had an error reading in the url, what do")
    #                     time.sleep(1)
    #     except:
    #         print("skipping this puppy")
    #         time.sleep(1)


    all_html = os.listdir(d_dir)

    output_file = open('data/output.csv','w')


    output_header = write_csv_line('this_id','backernum','reward_price','reward_shipping','max_back','launch','deadline')+"\n"
    output_file.write(output_header) # python will convert \n to os.linesep

    # prepare some regex stuff
    # find_currency = re.compile('data-currency=\"(.*?)\"')
    # find_currency = re.compile('([$])')
    extract_number = re.compile("\d+")


    # index for looping over pages
    for ii in range(len(all_html)):
        try:
            this_name = all_html[ii]


            # read that HTML file
            this_path = os.path.join(d_dir,this_name)
            this_file = open(this_path)
            html = this_file.read()
            this_file.close()

            # get that ID out
            this_id = this_name[0:-5]
            launch = '' #project_list[ii][headers.index('launched_at')]
            deadline = '' #project_list[ii][headers.index('deadline')]


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
                reward_price = unicodedata.normalize('NFKD', reward_price).encode('ascii','replace')


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

                # print(to_print)

                output_file.write(to_print)
        except:
            print("skipping this puppy don't know why" + str(ii))
            # output_file.write("bummer but this line had a problem\n")


    output_file.close()



# Additional variables:
# max_reward, the maximum number that can be sold of each reward level. default -1.

def write_csv_line(*args):
    return '"' + reduce(lambda x,y: x + '","' + y ,args) + '"'



# Not using this anywhere
def grep(s,pattern):
    return '\n'.join(re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M))



if __name__ == "__main__":
    main()















