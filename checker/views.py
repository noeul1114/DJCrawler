from django.shortcuts import render
from django.http.response import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user, login, logout

from selenium import webdriver
import time

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
        driver = webdriver.Chrome('/Users/Saywer/Downloads/chromedriver')
        driver.implicitly_wait(2)

        DEBUG = False
        HTTPS = False

        if DEBUG :
            SiteUrl = "http://127.0.0.1:800/"
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
            time.sleep(5)

            iframe = driver.find_elements_by_tag_name('iframe')[0]

            driver.find_element_by_name('title').send_keys(A.title)
            driver.switch_to_frame(iframe)
            driver.find_element_by_class_name('btn-codeview').click()

            contentbox = driver.find_element_by_class_name('note-codable')
            # contentbox = driver.find_element_by_xpath('//div[contains(@class, "note-editable")]')
            contentbox.send_keys(A.article)
            contentbox.send_keys("<p>&nbsp;</p><p>&nbsp;</p><p style=\"text-align: center;\"> \
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
        return HttpResponseRedirect(reverse('check_main'))
    else:
        return Http404