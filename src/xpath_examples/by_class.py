from scrapy import Selector


def example_class():
    # https://www.zyte.com/blog/xpath-tips-from-the-web-scraping-trenches/
    # When selecting by class, be as specific as necessary
    # *[contains(concat(' ', normalize-space(@class), ' '), ' someclass ')]

    sel = Selector(text='<p class="content-author">Someone</p><p class="content text-wrap">Some content</p>')
    xp = lambda x: sel.xpath(x).getall()

    # BAD
    # doesn't work because there are multiple classes in the attribute
    bad = xp("//*[@class='content']")
    assert bad == []

    # BAD MORE
    # gets more than we want
    bad_more = xp("//*[contains(@class,'content')]")
    assert bad_more == ['<p class="content-author">Someone</p>', '<p class="content text-wrap">Some content</p>']

    # GOOD
    good = xp("//*[contains(concat(' ', normalize-space(@class), ' '), ' content ')]")
    assert good == ['<p class="content text-wrap">Some content</p>']

    #  you can just use a CSS selector instead, and even combine the two of them if needed:

    # ALSO GOOD
    also_good = sel.css(".content").getall()
    assert also_good == ['<p class="content text-wrap">Some content</p>']

    # get class name
    # nested selectors
    # https://docs.scrapy.org/en/latest/topics/selectors.html#nesting-selectors
    also_good1 = sel.css('.content').xpath('@class').getall()
    assert also_good1 == ['content text-wrap']

    # to get text content
    # https://stackoverflow.com/questions/19343231/extracting-just-page-text-using-htmlagilitypack/19350897#19350897
    # // *[not (self::script or self::style)] / text()[normalize - space(.)]


if __name__ == '__main__':
    example_class()


