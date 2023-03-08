from pathlib import Path

import scrapy


class BrooklynBowlConcertsSpider(scrapy.Spider):
    name = "brooklyn_bowl"

    def start_requests(self):
        urls = [
            "https://www.brooklynbowl.com/brooklyn/shows/all",
            # "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for show in response.css("div.eventItem"):
            yield {
                "show": show.css("h3.title a *::text").get(),
                "date": show.css("div.date.outside::attr(aria-label)").get(),
                "doors": show.css("span.doors::text").re(r"((\d+:\d+\s[A|P]M))"),
                "times": show.css("div.time::text").re(r"((\d+:\d+\s[A|P]M))"),
                "prices": show.css(".prices::text").get(),
                "tagline": show.css(".tagline::text").get(),
            }

            # band = band
            # date = date

            # response.css(".doors::text").re(r"((\d+:\d+\s[A|P]M))")
            # response.css(".time::text").re(r"((\d+:\d+\s[A|P]M))").getall() is None
            # response.css(".prices::text").extract()
            # response.css(".tagline::text").extract()

            # yield {
            #     "band": band,
            #     "date": date,
            # "doors": doors,
            # "times": times,
            # "prices": prices,
            # "tagline": tagline,
            # }
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")
