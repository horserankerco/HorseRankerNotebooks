# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.selector import Selector
import re
import datetime


def clean_races(races):
    races_obj = Selector(text=races)
    raw_races = races_obj.xpath('.//div/div')
    races = []
    for index, raw_race in enumerate(raw_races):
        race_info_raw = raw_race.xpath('./text()').get()
        race_info = race_info_raw.split(" ")
        races.append({
            "track_abbr": race_info[0].strip(),
            "race_number": race_info[1].strip()
        })
    return races


def clean_date(date):
    date_obj = Selector(text=date)
    raw_month = date_obj.xpath('.//div[@class="date-month"]/text()').get()
    day = date_obj.xpath('.//div[@class="date-day"]/text()').get()
    year = datetime.date.today().year
    date_time = "{}/{}/{}".format(year, raw_month, day)
    date_object = datetime.datetime.strptime(date_time, "%Y/%b/%d")
    track_date = date_object.strftime('%Y-%m-%d')
    return track_date


def clean_results(results):
    results_obj = Selector(text=results)
    races_rows = results_obj.xpath('.//tbody/tr/td/span[@class="fullSize"]')
    results_rows = results_obj.xpath('.//tbody/tr[@class="results"]')

    races = []
    for race_row in races_rows:
        raw_race = race_row.xpath('./text()').get()
        race = raw_race.split(" #")
        track_name = race[0].strip()
        race_number = race[1].strip()

        races.append({
            'track_name': track_name,
            'race_number': race_number,
        })

    results = []
    for index, result_row in enumerate(results_rows):
        raw_result_rows = result_row.xpath('./td/div/table/tbody/tr')

        for raw_result_row in raw_result_rows:
            raw_horse = raw_result_row.xpath('./td/div[@class="horse"]')
            horse_number = raw_horse.xpath('normalize-space(.//div[@class="horse-number saddleCloth"]/text())').get()
            horse_name = raw_horse.xpath('normalize-space(.//div[@class="horse-name"]/text())').get()
            raw_win = raw_result_row.xpath('normalize-space(./td[2]/text())').get()
            win = re.sub(r"\$", '', raw_win)
            raw_place = raw_result_row.xpath('normalize-space(./td[3]/text())').get()
            place = re.sub(r"\$", '', raw_place)
            raw_show = raw_result_row.xpath('normalize-space(./td[4]/text())').get()
            show = re.sub(r"\$", '', raw_show)

            results.append({
                'track_name': races[index]['track_name'],
                'race_number': races[index]['race_number'],
                'horse_number': horse_number,
                'horse_name': horse_name,
                'win': float(win),
                'place': float(place),
                'show': float(show)
            })
    return results


def clean_players(players):
    players_obj = Selector(text=players)
    raw_players = players_obj.xpath('.//tr[@class="entry " or @class="entry odd"]')
    players = []
    for player in raw_players:
        raw_name_entry = player.xpath("normalize-space(./td[2]/text())").get()
        name_entry = raw_name_entry.split("- Entry")
        raw_earnings = player.xpath("./td[3]/text()").get()
        name = name_entry[0].strip()
        rank = player.xpath("./td[1]/text()").get()
        entry = name_entry[1].strip()
        earnings = re.sub(r"\$", '', raw_earnings)

        players.append({
            'name': name,
            'rank': int(rank),
            'entry': int(entry),
            'earnings': float(earnings)
            #           'selections': selections
        })
    return players


def clean_selections(selections):
    selections_obj = Selector(text=selections)
    raw_selections = selections_obj.xpath('.//tr[@class="leaderboard-details" or @class="leaderboard-details odd"]')

    selections = []

    for selection in raw_selections:
        raw_player_name_entry = selection.xpath('./preceding-sibling::*[1]/td[2]/text()').get()
        player_name_entry = raw_player_name_entry.split("- Entry")
        player_name = player_name_entry[0].strip()
        player_entry = player_name_entry[1].strip()

        raw_player_selections = selection.xpath('./td/div/table[@class="leaderboard-race-list"]/tbody/tr[not(@class)]')
        for player_selection in raw_player_selections:
            selection_number = player_selection.xpath('./td[1]/text()').get()
            raw_track_and_race = player_selection.xpath('./td[1]/span[1]/text()').get()
            track_and_race = raw_track_and_race.split(" #")
            track_name = track_and_race[0]
            race_number = track_and_race[1]

            horse_scratch = player_selection.xpath('./td[2]/div[@class="horse scratch"]').get()
            second_horse = player_selection.xpath('./td[2]/div[2]').get()

            if horse_scratch:
                horse_number = player_selection.xpath('./td[2]/div[2]/div[1]/text()').get()
                horse_name = player_selection.xpath('./td[2]/div[2]/div[2]/text()').get()
            elif not horse_scratch and second_horse:
                first_horse_number = player_selection.xpath('./td[2]/div/div[1]/text()').get()
                first_horse_name = player_selection.xpath('./td[2]/div/div[2]/text()').get()
                second_horse_number = player_selection.xpath('./td[2]/div[2]/div[1]/text()').get()
                second_horse_name = player_selection.xpath('./td[2]/div[2]/div[2]/text()').get()
                second_horse_name = \
                    re.sub(" - Alt", "", str(second_horse_name)) if second_horse_name else second_horse_name
                second_horse_name = \
                    re.sub(" - PTF", "", str(second_horse_name)) if second_horse_name else second_horse_name

                horse_number = "{}/{}".format(first_horse_number, second_horse_number)
                horse_name = "{}/{}".format(first_horse_name, second_horse_name)
            else:
                horse_number = player_selection.xpath('./td[2]/div/div[1]/text()').get()
                horse_name = player_selection.xpath('./td[2]/div/div[2]/text()').get()

            horse_name = re.sub(" - Alt", "", str(horse_name)) if horse_name else horse_name
            horse_name = re.sub(" - PTF", "", str(horse_name)) if horse_name else horse_name

            raw_win = player_selection.xpath('./td[3]/text()').get()
            win = re.sub(r"\$", '', raw_win)
            raw_place = player_selection.xpath('./td[4]/text()').get()
            place = re.sub(r"\$", '', raw_place)
            raw_show = player_selection.xpath('./td[5]/text()').get()
            show = re.sub(r"\$", '', raw_show)

            selections.append({
                'player': player_name,
                'player_entry': int(player_entry),
                'selection_number': int(selection_number.strip()),
                'track_name': track_name,
                'race_number': race_number,
                'horse_number': horse_number,
                'horse_name': horse_name,
                'win': float(win),
                'place': float(place),
                'show': float(show)
            })

    return selections


def clean_website(website):
    website_obj = Selector(text=website)
    raw_website = website_obj.xpath('.//text()').get()
    raw_website_url = raw_website.split(" - ")
    raw_website_name = raw_website_url[1].split(".")
    website_name = raw_website_name[0].strip()
    return website_name.lower()


def clean_contest_code(contest_code):
    contest_code_obj = Selector(text=contest_code)
    contest_code = contest_code_obj.xpath('.//@rel').get()
    return contest_code


class TourneysItem(scrapy.Item):
    races = scrapy.Field(
        input_processor=MapCompose(clean_races)
    )

    name = scrapy.Field(
        output_processor=TakeFirst()
    )

    date = scrapy.Field(
        input_processor=MapCompose(clean_date),
        output_processor=TakeFirst()
    )

    website = scrapy.Field(
        input_processor=MapCompose(clean_website),
        output_processor=TakeFirst()
    )

    contest_code = scrapy.Field(
        input_processor=MapCompose(clean_contest_code),
        output_processor=TakeFirst()
    )

    players = scrapy.Field(
        input_processor=MapCompose(clean_players)
    )

    selections = scrapy.Field(
        input_processor=MapCompose(clean_selections)
    )

    results = scrapy.Field(
        input_processor=MapCompose(clean_results)
    )
