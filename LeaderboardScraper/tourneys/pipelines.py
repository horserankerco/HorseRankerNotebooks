# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from tourneys.db import database
from tourneys.db.connection_pool import get_connection


class PostgresPipeline(object):

    def open_spider(self, spider):
        # Uncomment only if you want to reset the database. This will delete all data.
        # with get_connection() as connection:
        #     database.create_tables(connection)
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        with get_connection() as connection:

            contest_id = database.add_contest(
                connection,
                item['name'],
                item['date'],
                item['website'],
                item['contest_code']
            )

            players = item['players']
            for player in players:
                database.add_player(
                    connection,
                    player['name'],
                    player['rank'],
                    player['entry'],
                    player['earnings'],
                    contest_id
                )
  
            selections = item['selections']
            for selection in selections:
                database.add_selection(
                    connection,
                    contest_id,
                    selection['player'],
                    selection['player_entry'],
                    selection['selection_number'],
                    selection['track_name'],
                    selection['race_number'],
                    selection['horse_number'],
                    selection['horse_name'],
                    selection['win'],
                    selection['place'],
                    selection['show'],
                )

            results = item['results']
            for result in results:
                database.add_result(
                    connection,
                    contest_id,
                    result['track_name'],
                    result['race_number'],
                    result['horse_number'],
                    result['horse_name'],
                    result['win'],
                    result['place'],
                    result['show'],
                )
        return item


class TourneysPipeline(object):
    def process_item(self, item, spider):
        pass


class CSVExportPipeline(object):
    def __init__(self):
        self.leaderboard_csv = None
        self.leaderboard_exporter = None

        self.player_csv = None
        self.player_exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.leaderboard_csv = open('leaderboard.csv', 'wb')
        self.leaderboard_exporter = CsvItemExporter(self.leaderboard_csv)
        self.leaderboard_exporter.start_exporting()

        self.player_csv = open('player.csv', 'wb')
        self.player_exporter = CsvItemExporter(self.player_csv)
        self.player_exporter.start_exporting()

    def process_item(self, item, spider):
        leaderboard_info = {
            'name': item['name'],
            'date': item['date'],
        }
        self.leaderboard_exporter.export_item(leaderboard_info)

        for player in item['players']:
            self.player_exporter.export_item(player)

        return item

    def spider_closed(self, spider):
        self.leaderboard_exporter.finish_exporting()
        self.player_exporter.finish_exporting()
