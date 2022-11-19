# -- coding: UTF-8 --
import re
import os
import sys
import time

import pyperclip

import win32gui
import win32con
import win32clipboard

from openpyxl import load_workbook
from openpyxl import Workbook

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def configchrome():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--incognito')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        return driver
    except Exception as e:
        print(repr(e))
        return False


def googleimage(driver, filepathlist):
    resultlist = []
    urllist = []
    resetflag = False
    refreshflag = False
    breakloopflag = False
    elfindflag = False
    cantfindflag = False
    lasturl = ""
    for i in range(len(filepathlist)):
        print("\n{}: {}".format(i+1, filepathlist[i]))
        if i == 0 or resetflag:
            try:
                print("Line:{}, 初始化中...".format(sys._getframe().f_lineno))
                driver.get("https://lens.google.com/search?p=AcLkwR1czMJwA0je-PjQsowwECIoS0DUK0scf\
                    BkBg5ahrkKQUftizfjUwhPu63efjg4pOPNEUW8pTKa6Zc84fC3dm9uPpV5XpQpJqpCIjE0CbpcEHpR\
                    FXjuG1T2VdmZYmuKGO7salXL7TfDHKLTL-Dxh_RykCDdr4Vi12aOyAmsQMWgk4sCIX4nWwBxDbThjr\
                    VgurR24w9J6wuQaSI5PaWlnLXZElp14-A39uvcJU45aep-ea5D3EvAWY2xb1h4U8GrO6XWUJDMuLY3\
                    MUdSk7gSSFP8evWybut1l72YnrqLVYTzf8uqLqIx6heFWLUICCSVhfzhXYhiDqfHGsrMTbBCLyR_Io\
                    CdqymS5Li-fdmACbjdV&ep=gisbubb&hl=en&re=df#lns=W251bGwsbnVsbCxudWxsLG51bGwsbnV\
                    sbCxudWxsLG51bGwsIkVrY0tKREJrTlRCbFpHTTNMVFU0TXpndE5EVmxOeTA1TTJGbUxURmlNakEyT\
                    ldJNFpUWTFNQklmU1RkdFRIWnlaVzQyT1hOWmQwMURZVjlYYUdaVlQxZ3RNVVUzTVZKNFp3PT0iXQ==")
            except Exception as e1:
                print(repr(e1))
                print("第一次异常")
                return resultlist

            try:
                print("Line:{}, 进行Upload操作中...".format(sys._getframe().f_lineno))
                lasturl = driver.current_url
                buttonUpload = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-haspopup="menu"]')))
                buttonUpload.click()
                time.sleep(2)
                WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'google-material-icons')))
                inputimage = driver.find_elements_by_class_name('google-material-icons')
                for inputimage_tmp in inputimage:
                    # print(inputimage_tmp.get_attribute("textContent"))
                    if inputimage_tmp.get_attribute("textContent") == "laptop_chromebook":
                        ActionChains(driver).move_to_element(inputimage_tmp).click(inputimage_tmp).perform()
                        # print("1")
                stime = time.time()
                while True:
                    handle = win32gui.FindWindow("#32770", "打开")
                    # print(handle)
                    if handle:
                        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                        win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
                        break
                    if time.time() - stime > 10:
                        print("弹窗超时")
                        break
            except Exception as e2:
                print(repr(e2))
                print("upload步骤异常")
                return resultlist

            try:
                print("\nLine:{}, 获取图片输入元素中...".format(sys._getframe().f_lineno))
                inputel = WebDriverWait(driver, 30).until(
                    EC.invisibility_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
                resetflag = False
            except Exception as e3:
                print(repr(e3))
                print("获取图片输入元素异常")
                return resultlist

        try:
            print("Line:{}, 图片输入中...".format(sys._getframe().f_lineno))
            print(inputel)
            # print(filepathlist[i])
            inputel.send_keys(filepathlist[i])
            if i != 0:
                urllist.append(lasturl)
            stime = time.time()
            while lasturl == driver.current_url:
                if time.time() - stime > 30:
                    print("加载图片超时")
                    refreshflag = True
                    break
            time.sleep(1)
            print(lasturl)
            if refreshflag:
                refreshflag = False
                resetflag = True
                resultlist.append("加载图片超时")
                lasturl = driver.current_url
                print(lasturl)
                continue
            # time.sleep(3)
        except Exception as e4:
            resetflag = True
            resultlist.append("ERROR")
            print(repr(e4))
            print("获取图片输入元素异常")
            lasturl = driver.current_url
            urllist.append(lasturl)
            print(lasturl)
            continue

        try:
            print("\nLine:{}, Switch to Text mode...".format(sys._getframe().f_lineno))
            textbutton = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Switch to Text mode"]')))
            # print(textbutton)
            textbutton.click()
            # time.sleep(1)
        except Exception as e5:
            # resetflag = True
            resultlist.append("ERROR")
            print(repr(e5))
            print("切换Text异常")
            lasturl = driver.current_url
            urllist.append(lasturl)
            print(lasturl)
            continue

        try:
            print("\nLine:{}, Select all text...".format(sys._getframe().f_lineno))
            stime = time.time()
            while True:
                cantfind = re.search(r"Can't find text", driver.page_source)
                if cantfind:
                    cantfindflag = True
                    break
                alltextbutton = WebDriverWait(driver, 30).until(
                    EC.visibility_of_any_elements_located((By.TAG_NAME, "button")))
                # print(alltextbutton)
                for alltextbutton_tmp in alltextbutton:
                    # print(alltextbutton_tmp.text)
                    if alltextbutton_tmp.text == "Select all text":
                        alltextbutton_tmp.click()
                        elfindflag = True
                        break
                if elfindflag:
                    elfindflag = False
                    break
                if time.time() - stime > 15:
                    print("未找到Select all text超时")
                    breakloopflag = True
                    break
            if cantfindflag:
                cantfindflag = False
                resultlist.append("无文字")
                print("无文字")
                lasturl = driver.current_url
                print(lasturl)
                continue
            if breakloopflag:
                breakloopflag = False
                resultlist.append("未找到Select all text")
                print("未找到Select all text")
                lasturl = driver.current_url
                print(lasturl)
                continue
        except Exception as e6:
            # resetflag = True
            resultlist.append("ERROR")
            print(repr(e6))
            print("Select all text异常")
            lasturl = driver.current_url
            urllist.append(lasturl)
            print(lasturl)
            continue

        try:
            print("\nLine:{}, Copy text...".format(sys._getframe().f_lineno))
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.CloseClipboard()
            stime = time.time()
            while True:
                copybutton = WebDriverWait(driver, 30).until(
                    EC.visibility_of_any_elements_located((By.TAG_NAME, "button")))
                # print(copybutton)
                for copybutton_tmp in copybutton:
                    # print(copybutton_tmp.text)
                    if copybutton_tmp.text == "Copy text":
                        copybutton_tmp.click()
                        elfindflag = True
                        break
                if elfindflag:
                    elfindflag = False
                    break
                if time.time() - stime > 5:
                    print("未找到Copy text")
                    breakloopflag = True
                    break
            if breakloopflag:
                breakloopflag = False
                resultlist.append("Copy text")
                print("未找到Copy text")
                lasturl = driver.current_url
                print(lasturl)
                continue
        except Exception as e7:
            # resetflag = True
            resultlist.append("ERROR")
            print(repr(e7))
            print("Copy text异常")
            lasturl = driver.current_url
            urllist.append(lasturl)
            print(lasturl)
            continue

        try:
            print("\nLine:{}, 获取粘贴板信息...".format(sys._getframe().f_lineno))
            ocrtext = pyperclip.paste()
            # win32clipboard.OpenClipboard()
            # ocrtext = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
            # win32clipboard.CloseClipboard()
            resultlist.append(ocrtext)
        except Exception as e8:
            # resetflag = True
            resultlist.append("ERROR")
            print(repr(e8))
            print("获取粘贴板数据异常")
            lasturl = driver.current_url
            urllist.append(lasturl)
            print(lasturl)
            continue
        lasturl = driver.current_url
        print(lasturl)
        time.sleep(3)
    urllist.append(lasturl)
    # win32clipboard.CloseClipboard()
    return resultlist, urllist


def main():
    filepath = input("请输入文件夹路径:\n")
    filepath = filepath.replace("\"", "").replace("\'", "")
    print(os.listdir(filepath))
    filelist = [filepath + "\\" + i for i in os.listdir(filepath) if os.path.splitext(i)[1].lower() == ".jpg" or os.path.splitext(i)[1].lower() == ".png"]
    chromedriver = configchrome()
    time_start = time.time()
    if chromedriver:
        result, url = googleimage(chromedriver, filelist)
        print(result)
        # result = [result_tmp.replace("\r\n", " ") for result_tmp in result]
        # for i in result:
        #     print(i)
        chromedriver.quit()
        # zipresult = [",".join(list(i)) + "\n" for i in zip(filelist, result)]
        # print(zipresult)
        resultreport = filepath + "\\report.xlsx"
        if os.path.exists(resultreport):
            os.remove(resultreport)
        wb = Workbook()
        sheetnames = wb.sheetnames
        ws = wb[sheetnames[0]]  # index为0为第一张表
        for cnt in range(1, len(filelist) + 1):
            try:
                print(filelist[cnt - 1])
                ws.cell(cnt, 1).value = filelist[cnt - 1]
                ws.cell(cnt, 2).value = result[cnt - 1]
                ws.cell(cnt, 3).value = url[cnt - 1]
            except Exception as e:
                print(filelist[cnt - 1] + "写入异常")
                print(repr(e))
        wb.save(resultreport)
        time_end = time.time()
        input("已生成报告, 耗时时间:{}, 平均耗时:{}, 按回车键结束".format(time_end - time_start, (time_end - time_start) / len(filelist)))
    else:
        print("启动Chrome异常")
    return


if __name__ == "__main__":
    main()

