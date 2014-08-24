# Scrapy settings for yellowPages project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'yellowPages'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['yellowPages.spiders']
NEWSPIDER_MODULE = 'yellowPages.spiders'
DEFAULT_ITEM_CLASS = 'yellowPages.items.YellowpagesItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DEPTH_LIMIT = 2
DOWNLOAD_DELAY = 2
