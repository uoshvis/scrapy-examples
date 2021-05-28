from scrapy import Selector


def example_node():
    # https://www.zyte.com/blog/xpath-tips-from-the-web-scraping-trenches/

    # the difference between //node[1] and (//node)[1]

    # //node[1] selects all the nodes occurring first under their respective parents.
    sel = Selector(text="""
    <ul class="list">
        <li>1</li>
        <li>2</li>
        <li>3</li>
    </ul>
    <ul class="list">
        <li>4</li>
        <li>5</li>
        <li>6</li>
    </ul>""")
    xp = lambda x: sel.xpath(x).getall()
    # get all first LI elements under whatever it is its parent
    all_first_li = xp("//li[1]")
    assert all_first_li == ['<li>1</li>', '<li>4</li>']
    # get the first LI element in the whole document
    first_li_whole = xp("(//li)[1]")
    assert first_li_whole == ['<li>1</li>']
    # get all first LI elements under an UL parent
    all_first_li_ul = xp("//ul/li[1]")
    assert all_first_li_ul == ['<li>1</li>', '<li>4</li>']
    # get the first LI element under an UL parent in the whole document
    first_li_ul_whole = xp("(//ul/li)[1]")
    assert first_li_ul_whole == ['<li>1</li>']

    # to get a collection of the local anchors that occur first under their respective parents:
    # //a[starts-with(@href, '#')][1]

    # to get the first local anchor in the document:
    # (//a[starts-with(@href, '#')])[1]


if __name__ == '__main__':
    example_node()


