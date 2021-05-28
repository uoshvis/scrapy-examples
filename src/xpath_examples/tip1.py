from scrapy import Selector


def example_contains():
    # https://www.zyte.com/blog/xpath-tips-from-the-web-scraping-trenches/

    # Avoid using contains(.//text(), 'search text') in your XPath conditions.
    # Use contains(., 'search text') instead.
    sel = Selector(text='<a href="#">Click here to go to the <strong>Next Page</strong></a>')
    xp = lambda x: sel.xpath(x).extract()
    # take a peek at the node-set
    text = xp('//a//text()')
    assert text == ['Click here to go to the ', 'Next Page']
    # convert it to a string
    text_string = xp('string(//a//text())')
    assert text_string == ['Click here to go to the ']
    # selects the first a node
    first_node = xp('//a[1]')
    assert first_node == ['<a href="#">Click here to go to the <strong>Next Page</strong></a>']
    # converts it to string
    first_node_string = xp('string(//a[1])')
    assert first_node_string == ['Click here to go to the Next Page']
    # GOOD
    assert xp("//a[contains(., 'Next Page')]") == first_node
    # BAD
    assert xp("//a[contains(.//text(), 'Next Page')]") == []
    assert xp("//a[contains(.//text(), 'Next Page')]") != first_node
    # GOOD
    assert xp("substring-after(//a, 'Next ')") == ['Page']
    # BAD
    assert xp("substring-after(//a//text(), 'Next ')") == ['']
    assert xp("substring-after(//a//text(), 'Next ')") != ['Page']


if __name__ == '__main__':
    example_contains()


