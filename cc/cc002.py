"""
* text：返回 alert/confirm/prompt 中的文字信息。
* accept()：接受现有警告框。
* dismiss()：解散现有警告框。
* send_keys(keysToSend)： 发送文本至警告框。
"""
from selenium import webdriver
from time import sleep
from poium import Page, PageElement, PageElements,NewPageElement
class BaiduIndexPage(Page):
    search_input = NewPageElement(name='wd')
    search_button = NewPageElement(id_='su')
    settings_button=NewPageElement(id_='s-usersetting-top')
    settings_search_button=NewPageElement(link_text='搜索设置')



driver = webdriver.Chrome()

page = BaiduIndexPage(driver)
page.get("https://www.baidu.com")
sleep(2)
page.settings_button.click()

sleep(2)

page.settings_search_button.click()

sleep(10)



driver.quit()