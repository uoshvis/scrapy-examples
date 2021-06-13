# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from pydispatch import dispatcher


# first case
# please, enable in settings

def item_type(item):
    # The CSV file names are used (imported) from the scrapy spider.
    return type(item).__name__


class ExportToMultiFilesPipeline:
    # filenames match item class names
    fileNamesCsv = ['AuthorItem', 'QuoteItem']

    def __init__(self):
        self.files = {}
        self.exporters = {}
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        # define output directory and filename
        self.files = dict([(name, open("./outputs/" + name + '.csv', 'wb')) for name in self.fileNamesCsv])
        for name in self.fileNamesCsv:
            self.exporters[name] = CsvItemExporter(self.files[name])
            # define export fields here
            # can be removed if all item fields are exported
            if name == 'AuthorItem':
                self.exporters[name].fields_to_export = ['time', 'author']
                self.exporters[name].start_exporting()
            if name == 'QuoteItem':
                self.exporters[name].fields_to_export = ['url', 'quote']
                self.exporters[name].start_exporting()

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        types_item = item_type(item)
        if types_item in set(self.fileNamesCsv):
            self.exporters[types_item].export_item(item)
        return item


# second case
# check if enabled in settings
class MultiPipeline:

    def __init__(self):
        self.file = None
        self.files = {}

    def close_spider(self, spider):
        for exporter in self.files.values():
            exporter.finish_exporting()

    def file_name(self, item):
        adapter = ItemAdapter(item)
        # title must be defined in item
        title = adapter['title']
        string = str(title).lower()
        # export to file logic
        if 'author' in string:
            exporter = CsvItemExporter(open('author_output.csv', 'ab'), include_headers_line=False)
            exporter.fields_to_export = ['title', 'time', 'author']
            exporter.start_exporting()
            self.files['author'] = exporter
            return self.files['author']
        # another export to file logic
        elif 'quote' in string:
            exporter = CsvItemExporter(open('quote_output.csv', 'ab'), include_headers_line=False)
            exporter.fields_to_export = ['title', 'url', 'quote']
            exporter.start_exporting()
            self.files['quote'] = exporter
            return self.files['quote']

    def process_item(self, item, spider):
        exporter = self.file_name(item)
        exporter.export_item(item)
        return item
