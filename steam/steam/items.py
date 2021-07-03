# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def clean_get_platforms(one_class):
    platforms = []
    platform = one_class.split(' ')[-1]
    if platform == 'win':
        platforms.append('Windows')
    if platform == 'mac':
        platforms.append('Mac osX')
    if platform == 'linux':
        platforms.append('Linux')
    if platform == 'vr_only':
        platforms.append('VR Only')
    if platform == 'vr_supported':
        platforms.append('VR Supported')
    return platforms


def clean_get_reviews_summary(raw):
    try:
        summary = remove_tags(raw)
    except TypeError as e:
        print(e)
        summary = 'No summary.'
    return summary


def clean_get_reviews_sentiment(classnames):
    print(classnames)
    sentiment = classnames.split(' ')[-1]
    return sentiment


class SteamItem(scrapy.Item):
    game_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    image_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    game_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    release_date = scrapy.Field(
        output_processor=TakeFirst()
    )
    platforms = scrapy.Field(
        input_processor=MapCompose(clean_get_platforms)
    )
    reviews_summary = scrapy.Field(
        input_processor=MapCompose(clean_get_reviews_summary),
        output_processor=TakeFirst()
    )
    reviews_sentiment = scrapy.Field(
        input_processor=MapCompose(clean_get_reviews_sentiment),
        output_processor=TakeFirst()
    )
