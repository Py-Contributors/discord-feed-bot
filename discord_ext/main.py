import os
import sys
sys.path.append('.')
from time import sleep

from discord_ext.api import RssFeed
from discord_ext.utils import send_message_to_discord
from discord_ext.utils import ROOT_DIR
from discord_ext.utils import read_txt_file, dump_article_title

expand_usr = os.path.expanduser("~")
os.makedirs(os.path.join(ROOT_DIR, "logs"), exist_ok=True)


class DiscordBot:
    def __init__(self, discord_webhook_url, feed_url, sleep_time=10):  # sleep_time is in seconds
        self.discord_webhook_url = discord_webhook_url
        self.feed_url = feed_url
        self.sleep_time = sleep_time
        self.rss_feed = RssFeed(self.feed_url)
        self.dump_article_file = os.path.join(expand_usr, "dump.txt")

    def send_message_to_discord(self):
        metadata = self.rss_feed.get_metadata()
        feed_title = metadata['title']  
        print("Starting {} Bot".format(feed_title))
        print("Running Bot... Press Ctrl+C to stop")
        print("Checking for new articles every {} seconds".format(self.sleep_time))
        while True:
            items = self.rss_feed.get_items()  # fetch all items from rss feed
            dump_articles = read_txt_file(self.dump_article_file)

            for item in items:  # loop through all items 
                item_title = self.rss_feed.get_item_by_tag(item, 'title')
                item_description = self.rss_feed.get_item_by_tag(item, 'description')
                item_link = self.rss_feed.get_item_by_tag(item, 'link')
                item_pubDate = self.rss_feed.get_item_by_tag(item, 'pubDate')
                
                if item_title not in dump_articles:
                    send_message_to_discord(self.discord_webhook_url, feed_title, item_title, item_description, item_link, item_pubDate)
                    dump_article_title(self.dump_article_file, item_title)  # dump article title to txt file to avoid duplicate message
                    print("Sending message to discord")
                    
                    
            sleep(self.sleep_time)  # sleep for 10 minutes