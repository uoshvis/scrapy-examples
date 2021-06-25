#Basic Image scraping

To scrape files or images from webpages, you need to use in-built pipelines, specifically, `FilesPipeline` or `ImagesPipeline`

Typical workflow when using `FilesPipeline`

1. You have to use a Spider to scrape an item and put the URLs of the desired file into a `file_urls` field.

2. You then return the item, which then goes into the item pipeline.

3. When the item reaches the `FilesPipeline`, the URLs in the `file_urls` are sent to the Scheduler to be downloaded by the Downloader. The only difference is that these `file_urls` are given higher priority and downloaded before processing any other requests.

4. When the files are downloaded, another field `files` will be populated with the results. It will comprise of the actual download URL, a relative path where it is stored, its checksum and the status.


`FilesPipeline` can be used to scrape different types of files (images, pdfs, texts, etc.). `ImagesPipeline` is specialized for scraping and processing images. Apart from the functionalities of `FilesPipeline`, it does the following:
- Convert all downloaded images to JPG format and RGB mode
- Generates thumbnails
- Check image width/height to make sure they meet a minimum constraint

Also, file names are different. Please use `image_urls` and `images` in place of `file_urls` and files while working with `ImagesPipeline`.

```
ITEM_PIPELINES = {
'scrapy.pipelines.images.ImagesPipeline':1
}
IMAGES_STORE = '/home/user/Documents/scrapy_project/images'
```
OR

```
IMAGES_STORE = 'images'

```
**!!! Pillow must be installed**

`pip install Pillow`


To run: 

`scrapy crawl image_crawl_spider -o output.json`