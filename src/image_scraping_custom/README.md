#Custom Image scraping


```
ITEM_PIPELINES = {
   'myproject.pipelines.MyImagesPipeline': 1,
}

IMAGES_STORE = 'images' 
```

OR
```
IMAGES_STORE = 'images'

```
**!!! Pillow must be installed**

`pip install Pillow`

**Custom filename**
```markdown
class MyImagesPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        return request.url.split('/')[-1]
```