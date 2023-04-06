# HorseRankerNotebooks

### Includes:

- Leaderboard Scraper

    #DB Setup

    The database is designed to work with Postgres.
    You will need to create a local postgres database.
    Set up the database credentials in LeaderboardScraper/tourneys/db/connection_pool.py
    #How to use. Use the leaderboard expander chrome extension: https://github.com/JoshSummerTop/LeaderboardExpander

    This chrome extension expands the "View Details" and "View Results" panels on a leaderboard page. example leaderboard: https://www.horsetourneys.com/leaderboard/contest/1455197/turf-paradise-mixed-40-guaranteed-w-no-limit-3-entries-min-p-p.html

    Once all the panels are expanded:

    Right click and Save As the HTML page to your computer.
    Then put the HTML file into the LeaderboardScraper/AddLeaderboardFiles folder.
    Then run the LeaderboardScraper/RunScraper.ipynb script. This will parse the HTML page and add the leaderboard to your database.
    You can see various scripts for analysis and exporting to CSV in LeaderboardScraper/SeeLeaderboardData.ipynb
    You can see the exported files in LeaderboardScraper/ExportedCSVFiles folder
