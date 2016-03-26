# -*- coding: utf-8 -*-

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Content, Category, PostImage, Tag, ContactUs
from .util import Util
import json, sys, itertools


"""
Page view handlers
"""


def index(request):
    """
    index page view handler
    redirect to postlist view
    """

    return post_list(request, 1)


def post_list(request, page):
    """
    return a paginated list of post object base on the input page number
    :param page: page number in paginator, 1-based
    :return: httpResponse
    """
    POST_PER_PAGE = 24  # number of post to be shown in a single page
    PAGES_PER_VIEW = 5  # number of page numbers to be shown in a single page

    posts = Post.objects.filter(status=1).order_by('-approve_datetime')   # retrieve approved posts
    paginator = Paginator(posts, POST_PER_PAGE)    # create a paginator
    num_pages = paginator.num_pages             # total number of pages
    page_range = paginator.page_range           # range of page numbers, eg. [1, 2, 3, 4]

    # set current page number
    cur_page = int(page)
    # set prev page
    prev_page = cur_page - 1
    if prev_page < 1:
        prev_page = None
    # set next page
    next_page = cur_page + 1
    if next_page > num_pages:
        next_page = None

    # create page range
    if num_pages <= PAGES_PER_VIEW:     # no need to move the page range frame
        range_start_idx = 0
        range_end_idx = num_pages
    else:                               # move the page range frame to focus on the current page
        if cur_page - PAGES_PER_VIEW/2 <= 0:
            range_start_idx = 0
        else:
            range_start_idx = cur_page - PAGES_PER_VIEW/2 - 1

        if page_range[range_start_idx] + PAGES_PER_VIEW - 1 >= num_pages:
            range_start_idx = num_pages - PAGES_PER_VIEW
            range_end_idx = num_pages
        else:
            range_end_idx = page_range[range_start_idx] + PAGES_PER_VIEW - 1

    print "start %d)" % range_start_idx
    print "end %d" % range_end_idx
    print "max %d" % num_pages
    # set up return context
    context = {
        'posts': paginator.page(cur_page),
        'cur_page': cur_page,
        'prev_page': prev_page,
        'next_page': next_page,
        'page_range': itertools.islice(page_range, range_start_idx, range_end_idx)
    }

    return render(request, 'posts/index.html', context)


def submit(request):
    """
    submit page view handler
    """
    categories = Category.objects.all()
    return render(request, 'posts/submit.html', {'categories': categories})


def submit_post(request):
    try:
        # init attribute list for post
        fields = dict()

        # retrieve data from request
        fields['category'] = Category.objects.get(id=request.POST['category'])
        fields['title'] = request.POST['title']

        if 'disp_thumbnail' in request.FILES.iterkeys():
            fields['disp_thumbnail'] = request.FILES['disp_thumbnail']

        if 'is_original' in request.POST.iterkeys():    # is original
            fields['is_original'] = True
        else:
            fields['is_original'] = False
            fields['source_name'] = request.POST['source_name']
            fields['source_url'] = request.POST['source_url']

        # create content for different post
        category = fields['category']
        if category.id == 1 or category.id == 4:
            # article & stuff
            body = request.POST['body']
        elif category.id == 2:
            # image
            img_list = []   # init a list to hold image objects
            body = ""       # body string for the content
            for filename, img_file in request.FILES.iteritems():    # create image objects
                if filename.startswith('img-'):     # file name for image posts
                    post_image = PostImage(
                        img=img_file
                    )
                    post_image.save()               # save first before extracting the img url
                    img_list.append(post_image)     # add image to list
                    body += post_image.img.url + Util.URL_DELIMITER
        elif category.id == 3:  # video
            body = request.POST['video-url']   # save video url

        content = Content(body=body)
        content.save()
        fields['content'] = content

        # create post object
        post = Post(**fields)
        post.save()

        # save PostImages and link them to Post
        if category.id == 2:
            for img in img_list:
                img.post = post
                img.save()

        return render(request, 'posts/success.html',
                      {
                          "title": "上传成功",
                          "message": "请等待审核"
                      })
    except:
        print "Unexpected error:", sys.exc_info()
        return HttpResponseRedirect('/fail/')


def get_recommends(post, amount):
    """
    Get a list of recommend post objects base on the input post id

    :param post: target post object
    :param amount:  number of recommends to return
    :return: a list of post object
    """

    # just return the previous posts before post
    start_id = post.id-amount
    end_id = post.id-1
    candidates = Post.objects.filter(id__range=(start_id, end_id))

    return candidates


def detail(request, post_id):
    """
    Detail view handler
    """
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    # get context for template
    context = post.get_detail_context()
    # get recommendation list
    context['recommends'] = get_recommends(post, 4)

    return render(request, "posts/detail.html", context)


def success(request):
    """
    Success page handler
    """
    return render(request, 'posts/success.html')


def fail(request):
    """
    Fail page handler
    """
    return render(request, 'posts/fail.html')


def about(request):
    """
    About page handler
    """
    return render(request, 'posts/about.html')


def contact(request):
    """
    Contact page handler
    """
    if request.method == 'GET':
        return render(request, 'posts/contact.html')
    else:
        try:
            fields = dict()
            fields['body'] = request.POST['contact-body']
            if "contact-email" in request.POST.iterkeys():
                fields['email'] = request.POST['contact-email']

            con = ContactUs(**fields)
            con.save()

            return render(request, 'posts/success.html',
                          {
                              "title": "上传成功",
                              "message": "非常感谢您的宝贵意见"
                          })

        except:
            print "Unexpected error:", sys.exc_info()
            return HttpResponseRedirect('/fail/')

"""
Review view handlers
"""


def review(request):
    """
    Review index page handler
    """
    if not request.user.is_authenticated():
        return render(request, 'posts/review/auth.html')
    else:   # use has been authenticated for reviewing
        # retrieve all posts
        posts = Post.objects.all()

        return render(request, 'posts/review/index.html', {
            'approved': posts.filter(status=1).order_by('-submit_datetime'),
            'pending': posts.filter(status=0).order_by('-submit_datetime'),
            'rejected': posts.filter(status=2).order_by('-submit_datetime'),
        })


def review_login(request):
    """
    Login review user
    """
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('review')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'posts/review/auth.html', {"err_msg": "Cannot login as superuser."})
    else:
        # redirect to review index page if user access this view directly from browser URL
        return HttpResponseRedirect('/review/')


def review_logout(request):
    """
    Logout review admin
    """
    logout(request)
    return redirect('/')


def review_detail(request, post_id):
    """
    Review detail page
    """
    # authenticate user
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return render(request, 'posts/review/auth.html', {"err_msg": "Login first."})

    # search post object
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")

    # search tag list
    tags = Tag.objects.all()

    # get context from post
    context = post.get_detail_context()     # get context for template

    context['tags'] = tags  # add tags to context

    return render(request, "posts/review/review_detail.html", context)


def review_save(request, post_id):
    """
    Save the review result
    """

    # authenticate user
    if not request.user.is_authenticated() or not request.user.is_superuser:
        return render(request, 'posts/review/auth.html', {"err_msg": "Login first."})

    try:
        if request.method == 'POST':
            status = request.POST['status']
            tags = []
            for k in request.POST.iterkeys():
                if k.startswith('tag-'):  # find checked tag id
                    tag_id = int(k.replace('tag-', ''))
                    tags.append(Tag.objects.get(pk=tag_id))

            # update post
            post = Post.objects.get(id=post_id)
            if status != post.status:   # update post status
                if status == '0':
                    post.pending()
                elif status == '1':
                    post.approve()
                elif status == '2':
                    post.reject()
                else:
                    return HttpResponseRedirect('/review_fail/')
            post.set_tags(tags)     # set new tag list to post
            post.save()

            return HttpResponseRedirect('/review_success/')
        else:
            return HttpResponseRedirect('/review_fail/')

    except:
        print "Unexpected error:", sys.exc_info()
        return HttpResponseRedirect('/review_fail/')


def review_success(request):
    """
    Review saved successfully
    """
    return render(request, 'posts/review/review_success.html')


def review_fail(request):
    """
    Review saved failed
    """
    return render(request, 'posts/review/review_fail.html')


"""
Ajax view handlers
"""


def upload_img(request):
    """
    Handle the images uploaded during the editing of articles,
    save the uploaded image and return a url of the save image
    """
    if request.method == 'POST':
        img = request.FILES['article-img']  # get image from request

        # save image
        post_img = PostImage(img=img)
        post_img.save()

        # return saved url
        return HttpResponse(json.dumps({'success': 1, 'url': post_img.img.url}), content_type="application/json")
    else:
        pass
        # response error, only get is allowed


def newtag(request):
    """
    Create a new tag via AJAX call
    """
    if request.method == 'POST':
        try:
            tag_name = request.POST['new_tag']

            t = Tag(name=tag_name)
            t.save()

            res = {
                'success': 1
            }
        except:
            res = {
                'success': -1,
                "err_msg": str(sys.exc_info())
            }
    else:
        res = {
                'success': -1,
                "err_msg": "this api only allow POST request"
            }

    return HttpResponse(json.dumps(res), content_type="application/json")