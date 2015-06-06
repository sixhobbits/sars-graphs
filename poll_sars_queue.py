# poll sars queue
# ---------------
# Grabs the number of people in the queue at the moment 
# Should be run as cron job or equivalent
# Currently SARS seems to update the queue count every five minutes
# Writes data to text file

import urllib2
import re
import time
import datetime

URL = "http://tools.sars.gov.za/BQMS/?branch=Cape%20Town"
# Compulsory referency to http://stackoverflow.com/questions/1732348/regex-match-open-tags-except-xhtml-self-contained-tags
# But BeautifulSoup dependency didn't seem worth it
NUM_PEOPLE_MATCHER = re.compile("queue: <b>([0-9]*)</b>")


def get_html(url):
    try:
        page = urllib2.urlopen(url).read()
        return page
    except Exception as e:
        print e


def run():
    page = get_html(URL)
    if "We will be able to tell you the queue length and how long you" in page:
	return  # Over weekends, SARS displays a message saying to check back later
    num_people_match = NUM_PEOPLE_MATCHER.search(page)
    num_people = int(num_people_match.group(1))
    with open("/data/sars_queue.txt", "a") as f:
        f.write("{}, {}\n".format(datetime.datetime.utcnow(), num_people))


if __name__ == '__main__':
    run()


