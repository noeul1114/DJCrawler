from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from selenium import webdriver
from selenium.webdriver.support.ui import Select

import time
import os
import random

from django.utils import timezone

from django.shortcuts import get_object_or_404

from bs4 import BeautifulSoup
from pasted.models import PastedData

# Create your views here.

def uncheckMain(request):
    user = get_user(request)
    if user.is_superuser:
        data = PastedData.objects.filter(checked=False).order_by('?')[0]
        return render(request, 'checker/board_detail.html', {'article_detail': data,
                                                             })
    else:
        return Http404



def image_checked(request, img_name):
    user = get_user(request)
    if user.is_superuser:
        driver = webdriver.Chrome('/Users/willypower/Desktop/footage/chromedriver')
        driver.implicitly_wait(2)

        DEBUG = False
        HTTPS = False

        if DEBUG :
            SiteUrl = "http://127.0.0.1:8000/"
        else:
            if HTTPS:
                SiteUrl = "https://sayproject.site/"
            else:
                SiteUrl = "http://sayproject.site/"

        driver.get(SiteUrl + 'login/')
        try:
            driver.find_element_by_name('username').send_keys('willypower')
            driver.find_element_by_name('password').send_keys('900302')

            driver.find_element_by_class_name('btn').click()
        except:
            driver.get(SiteUrl + 'logout/')

        try:
            driver.implicitly_wait(2)

            driver.get(SiteUrl + 'write/')

            driver.implicitly_wait(3)
            time.sleep(3)

            select = Select(driver.find_element_by_name("project"))
            if DEBUG :
                select.select_by_value("36")
            else:
                select.select_by_value("24")

            iframe = driver.find_elements_by_tag_name('iframe')[0]

            driver.find_element_by_name('title').send_keys("혜리")
            driver.switch_to.frame(iframe)
            # driver.find_element_by_class_name('btn-codeview').click()

            driver.find_element_by_class_name('note-icon-picture').click()
            image = driver.find_element_by_class_name('note-image-input')
            time.sleep(3)
            # contentbox = driver.find_element_by_xpath('//div[contains(@class, "note-editable")]')
            image.send_keys('C:/Users/willypower/PycharmProjects/DJCrawler/checker/static/checker/image/Hyeri/'
                            + img_name)
            time.sleep(7)

            driver.switch_to.default_content()

            driver.find_element_by_class_name('submit_button').click()

            driver.close()
            return HttpResponseRedirect(reverse('image_main'))
        except:
            return HttpResponseRedirect(reverse('image_main'))
    else:
        return Http404


def imageMain(request):
    path = 'C:/Users/willypower/PycharmProjects/DJCrawler/checker/static/checker/image/Hyeri/'
    files = os.listdir(path)
    index = random.randrange(0, len(files))

    # path = '../checker/image/'

    image = files[index]
    user = get_user(request)
    if user.is_superuser:
        return render(request, 'checker/board_image_detail.html', {'image': image,
                                                                })
    else:
        return Http404


def checkMain(request):
    user = get_user(request)
    if user.is_superuser:
        data = PastedData.objects.filter(checked=True).order_by('?')[0]
        return render(request, 'checker/board_detail.html', {'article_detail': data,
                                                             })
    else:
        return Http404


def article_checked(request, article_id):
    user = get_user(request)
    A = get_object_or_404(PastedData, pk=article_id)
    checked = A.checked
    if user.is_superuser:
        driver = webdriver.Chrome('/Users/willypower/Desktop/footage/chromedriver')
        driver.implicitly_wait(2)

        DEBUG = False
        HTTPS = False

        if DEBUG :
            SiteUrl = "http://127.0.0.1:8000/"
        else:
            if HTTPS:
                SiteUrl = "https://sayproject.site/"
            else:
                SiteUrl = "http://sayproject.site/"

        driver.get(SiteUrl + 'login/')
        try:
            driver.find_element_by_name('username').send_keys('willypower')
            driver.find_element_by_name('password').send_keys('900302')

            driver.find_element_by_class_name('btn').click()
        except:
            driver.get(SiteUrl + 'logout/')

        try:
            driver.implicitly_wait(2)

            driver.get(SiteUrl + 'write/')

            driver.implicitly_wait(3)
            time.sleep(3)

            select = Select(driver.find_element_by_name("project"))
            if DEBUG :
                select.select_by_value("36")
            else:
                select.select_by_value("23")

            iframe = driver.find_elements_by_tag_name('iframe')[0]

            driver.find_element_by_name('title').send_keys(A.title)
            driver.switch_to_frame(iframe)
            driver.find_element_by_class_name('btn-codeview').click()

            contentbox = driver.find_element_by_class_name('note-codable')
            # contentbox = driver.find_element_by_xpath('//div[contains(@class, "note-editable")]')
            contentbox.send_keys(A.article)
            contentbox.send_keys("<p>&nbsp;</p><p>&nbsp;</p><p style=\"text-align: center; display: inline-block;"
                                 " text-overflow: ellipsis;width: 18em; white-space: nowrap;overflow: hidden;\"> \
                                    출처 : <a href=\"{}\">{}</a>&nbsp;</p> ".format(A.link, A.link))

            driver.switch_to_default_content()

            driver.find_element_by_class_name('submit_button').click()
            A.checked = True
            A.save()

            driver.close()
        except:
            pass
        if checked:
            return HttpResponseRedirect(reverse('check_main'))
        else:
            return HttpResponseRedirect(reverse('uncheck_main'))
    else:
        return Http404

def article_deleted(request, article_id):
    user = get_user(request)
    A = get_object_or_404(PastedData, pk=article_id)
    if user.is_superuser:
        try:
            A.delete()
        except:
            pass
        return HttpResponseRedirect(reverse('uncheck_main'))
    else:
        return Http404