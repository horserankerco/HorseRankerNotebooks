# -*- coding: utf-8 -*-
import scrapy
# from itemloaders import ItemLoader
from scrapy.loader import ItemLoader
from ..items import TourneysItem
import os

class LeaderboardSpider(scrapy.Spider):
    name = 'leaderboard'

    def __init__(self, file_name=None, *args, **kwargs):
        super(LeaderboardSpider, self).__init__(*args, **kwargs)
        self.start_url = file_name
        
    def start_requests(self):

        yield scrapy.Request(url=self.start_url)

    def parse(self, response):
        loader = ItemLoader(item=TourneysItem(), response=response)
        loader.add_xpath('name', '//div[@class="type-tournament"]/h1/text()')
        loader.add_xpath('date', '//div[@class="date"]')
        loader.add_xpath('website', '//title')
        loader.add_xpath('contest_code', '//table[@id="leaderboard"]')
        loader.add_xpath('races', '//div[@id="leaderboard-events"]')
        loader.add_xpath('players', '//table[@id="leaderboard"]')
        loader.add_xpath('selections', '//table[@id ="leaderboard"]/tbody')
        loader.add_xpath('results', '(//table[@class="leaderboard-race-list"])[1]/tbody')

        file_to_delete = self.start_url.replace('file://', '')
        os.remove(file_to_delete)

        return loader.load_item()



