

from __future__ import unicode_literals

from datetime import datetime
from django.db import models

from .util import Util


class Tag(models.Model):
    """
    Tag class defines a tag that labels the content of a post
    """
    name = models.CharField(max_length=100)  # name of the tag


class Content(models.Model):
    """
    Content class contains the content body of a post
    """
    body = models.TextField()   # body of the content

    def __str__(self):
        return "content - %s" % self.post.title


class Category(models.Model):
    """
    Category class defines the category of a post
    """
    name = models.CharField(max_length=100)  # name of the category
    thumbnail = models.ImageField(upload_to='local/category_thumbnails', blank=True)   # thumbnail image of the category

    def __str__(self):
        return self.name.encode("utf-8")


class Post(models.Model):
    """
    Post class defines a post with text, image, or video content
    """
    POST_STATUS_CHOICES = (     # choices for the Post.status field
        (0, 'pending'),
        (1, 'approved'),
        (2, 'rejected')
    )

    ''' General attributes '''
    title = models.CharField(max_length=254)                # title of the post

    is_original = models.BooleanField(default=True)             # a flag indicate whether this post is original

    source_name = models.CharField(max_length=512, blank=True)  # source name of the post, eg. Youku
    source_url = models.CharField(max_length=512, blank=True)   # URL of the source site

    author = models.CharField(max_length=512, blank=True)   # author of the post

    submit_datetime = models.DateTimeField(auto_now=True)   # datetime of submission
    approve_datetime = models.DateTimeField(blank=True, null=True)  # datetime of approval
    status = models.DecimalField(
            max_digits=2,
            decimal_places=0,
            choices=POST_STATUS_CHOICES,
            default=0)                      # status of the post, default to 0 ('submitted')
    likes = models.IntegerField(default=0)  # number of likes on this post
    category = models.ForeignKey(Category)  # category of the post
    email = models.EmailField(blank=True)   # email of the person who submitted the post
    tags = models.ManyToManyField(Tag)      # tags attached to this article
    disp_thumbnail = models.ImageField(
            upload_to='local/display_thumbnails',
            blank=True)                     # display thumbnail image for the post

    # content of the post
    # if the post is Article or Stuff, the content is the html string of the body
    # if the post is Video, the content is the url of the video
    # if the post is Image, the content is the url of the images separated by "<br>"
    content = models.OneToOneField(
            Content,
            on_delete=models.CASCADE)

    def pending(self):
        """
        make this post pending
        """
        self.status = 0

    def approve(self):
        """
        approve this post
        """
        self.status = 1
        self.approve_datetime = datetime.now()

    def reject(self):
        """
        reject this post
        """
        self.status = 2

    def set_tags(self, new_tags):
        """
        Set the many-to-many field tags

        :param new_tags: list of Tag object need to be added to self.tags
        """
        # sync new_tags and self.tags
        for t in self.tags.all():
            if t in new_tags:
                new_tags.remove(t)  # this tag is already added, remove from new tag list
            else:
                self.tags.remove(t) # this tag is not in new_tags, remove from the current post

        for t in new_tags:          # add the remaining tags in new_tags to this post
            self.tags.add(t)

    def get_detail_context(self):
        """
        create the context for detail(or review detail) view(s) to render the template

        :return: context object contains the required fields for view
        """
        context = {
            'post': self
        }

        if self.category.id == 2:  # handle image post detail
            # post_images = post.postimage_set.all()
            img_urls = self.content.body.split(Util.URL_DELIMITER)
            img_urls = filter(None, img_urls)   # remove empty url
            context['img_urls'] = img_urls

        return context

    def __str__(self):
        """
        String representation of the post
        """
        return self.title


class PostImage(models.Model):
    """
    PostImage class defines the image attachment related to a post
    """
    img = models.ImageField(upload_to='uploads/%Y/%m/%d/')
    post = models.ForeignKey(Post, blank=True, null=True, on_delete=models.CASCADE)  # foreign key points to Post

    def __str__(self):
        return self.img.url


class ContactUs(models.Model):
    """
    Contact us stores the information of user advise
    """
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
