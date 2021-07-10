# My web scraping projects
After painfully trying to clean large csv files with node (async functions and accessing/writing multiple files) easily became a nightmare. I decided to learn webscraping and data cleaning with python and here are some of the projects I've been working on. I've learned a lot from online and offline(books) resources, so there are example projects and my own personal projects mixed together in this repo. However, when it comes to data cleaning, the bulk of my work in probably in /cleaning, if you're interested.

## What's inside this repo?
The repo contains web scraping projects that can be divided into three categories:

- Projects from online courses and books (like
  the [getting_structured_data]('https://github.com/DrPoppyseed/web_scraping/tree/main/getting_structured_data') repo)
- Scrapy projects that I created (
  like [sanfranciscan]('https://github.com/DrPoppyseed/web_scraping/tree/main/sanfranciscan')
  and [cwur]('https://github.com/DrPoppyseed/web_scraping/tree/main/cwur') repos)
- Projects for cleaning data and scrapers built without scrapy
  in [cleaning]('https://github.com/DrPoppyseed/web_scraping/tree/main/cleaning')

## What are some notable projects inside this repo?
Some projects stand out to me as either having required knowledge of a new technology, or of having a plus alpha component to it. These are some of them:

- [This project](https://github.com/DrPoppyseed/web_scraping/tree/main/getting_structured_data/cloud_hosted_scrapers): hosting web scrapers and executing them on AWS E2 servers / using S3 to store the crawled data
- [This project](https://github.com/DrPoppyseed/web_scraping/tree/main/zillow): Tkinter desktop app to execute scrapy spiders on the fly
- [This project](https://github.com/DrPoppyseed/web_scraping/tree/main/steam): Flask app that scrapes the top 100 best sellings Steam games whenever the app is opened (using scrapyRT)
- [This project](https://github.com/DrPoppyseed/web_scraping/tree/main/sanfranciscan): scrapes data from the sanfranciscan website, cleans, and outputs them in word documents
- [And finally, this project](https://github.com/DrPoppyseed/web_scraping/tree/main/shanghairanking): a failed attempt at trying to scrape the shanghairanking site using scrapy-splash. Next attempt would use Selenium, smarter sleeping between accesses, and IP rotation maybe (though including sleeping pauses may be enough)

## The stuff I used
Here are the frameworks and libraries I used in this repo.

| Stuff used | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| Scrapy         | Building web scrapers fast!                     |
| Splash (+Aquarium)         | Rendering Javascript heavy websites!            |
| Tkinter           | For builing a simple desktop app                     |
| Flask           | For builing a simple web app                     |
