#!/usr/bin/env python

# 自动表单
# 基于python + selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import simplejson as json
import time
from pywinauto import application
import logging


def logger_config(log_path, logging_name):
    '''
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    '''
    '''
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    # 输出DEBUG及以上级别的信息，针对所有输出的第一层过滤
    logger.setLevel(level=logging.DEBUG)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    handler.setLevel(logging.INFO)
    # 生成并设置文件日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # console相当于控制台输出，handler文件输出。获取流句柄并设置日志级别，第二层过滤
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 为logger对象添加句柄
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def upload_aux(driver, xpath, filepath):
    upload_input = driver.find_element_by_xpath(xpath)
    upload_input.click()
    time.sleep(1)
    app = application.Application()
    app.connect(class_name='#32770')  # 根据class_name找到弹出窗口
    app["Dialog"]["Edit1"].type_keys(filepath)     # 在输入框中输入值
    app["Dialog"]["Button1"].click()


def main():
    # 日志记录

    logger = logger_config(log_path='im_log.txt',
                           logging_name='IM WEBSITE TEST LOG')
    test_size = 500
    test_number = 1
    cnt_success = 0
    cnt_fail = 0

    # 测试用变量
    test_url = "https://imff.mike-x.com/sKM8G"
    test_name_prefix = "Edward_test"
    test_email_str = "edwardzcn98@gmail.com"
    test_date = ""
    test_month = "2021-04"
    test_date = "2021-04-10"
    # 测试图片路径 用于填充学籍照片、导演照片、作品海报、作品截图、拍摄花絮
    path_to_img = "C:\\Users\\64980\\Pictures\\bg1.jpg"
    # 测试视频 用于填充预告片
    path_to_preview = "C:\\Daily\\PersonalStudy\\Python\\test.mp4"
    # 测试视频 用于填充正片
    path_to_mainview = "C:\\Daily\\PersonalStudy\\Python\\test3.mp4"
    # 测试视频  用于填充限时表达短片
    path_to_limitview = "C:\\Daily\\PersonalStudy\\Python\\test.mp4"

    driver = webdriver.Chrome()
    driver.get(test_url)
    print(driver.title)
    # 确定打开页面为 IM两岸青年影展报名通道
    assert "IM" in driver.title

    # TODO 在有cookie缓存情况下不需要填email，应该跳过
    elem_input_address = driver.find_element_by_class_name(
        "fbi_input.aria-content")
    elem_input_address.clear()
    # 填写测试用
    elem_input_address.send_keys(test_email_str)
    button = driver.find_element_by_class_name("fb_mlButton.has_next").click()
    # 填写验证码！ 手动
    verify_code = input()
    elem_input_verify = driver.find_element_by_class_name(
        "fbi_input.aria-content")
    elem_input_verify.clear()
    elem_input_verify.send_keys(verify_code)

    button = driver.find_element_by_class_name("fb_mlButton")
    button.click()

    # 保存cookies
    with open('im_cookies.txt','w') as cookief:
    #将cookies保存为json格式
        cookief.write(json.dumps(driver.get_cookies()))
    # TODO 需要用cookies 免密登录 拆分为两个脚本

    # 登录后部分

    # 设置当前测试字串
    # TODO 设定当前轮的测试数字
    for i in range(11,test_size):
        driver.get(test_url)
        # driver.delete_all_cookies()
        with open('im_cookies.txt','r') as cookief:
            #使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookieslist = json.load(cookief)
        for cookie in cookieslist:
            #并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)
        driver.refresh()
        num = i
        logger.info("Test cicle {} start.".format(num))
        test_str = test_name_prefix + "{:0>3d}".format(num)

        # 模拟点击“已详细阅读” 至下一页
        # 显示等待 同步状态
        button = WebDriverWait(driver, timeout=3).until(
            lambda d: d.find_element_by_class_name("fbc_cpBs7Content"))
        button.click()

        # Fix 元素没有加载完成导致无法click的问题
        time.sleep(2)
        WebDriverWait(driver, timeout=3).until(lambda d: d.find_element_by_xpath(
            '//*[@id="205444644"]/div[2]/div/div/textarea'))
        elems = driver.find_elements_by_class_name("fbi_input.aria-content")
        for elem in elems:
            elem.clear()
            elem.send_keys(test_str)
        # 单独填充影片完成时间
        elems[2].clear()
        elems[2].send_keys(test_date)
        # 单选框默认为剧情
        driver.find_element_by_xpath(
            '//*[@id="205444638"]/div[2]/div/ul/li[1]').click()
        # 下一页
        driver.find_element_by_class_name("fbc_cpBs7Content").click()

        # 申请人资料页
        time.sleep(2)
        elems = driver.find_elements_by_class_name("fbi_input.aria-content")
        for elem in elems:
            elem.clear()
            elem.send_keys(test_str)
        # 单独填充出生年月，毕业时间和邮箱
        elems[2].clear()
        elems[2].send_keys(test_month)
        elems[6].clear()
        elems[6].send_keys(test_month)
        elems[10].clear()
        elems[10].send_keys(test_email_str)

        upload_aux(
            driver, '//*[@id="205444657"]/div[2]/div/div/ul/li', path_to_img)
        driver.find_element_by_class_name("fbc_cpBs7Content").click()

        # 主创团队资料
        time.sleep(1)
        # 默认全空 点击下一页
        driver.find_element_by_class_name("fbc_cpBs7Content").click()

        # 作品资料上传
        time.sleep(1)
        elem = driver.find_element_by_class_name("fbi_input.aria-content")
        elem.clear()
        elem.send_keys(test_str)
        # 上传导演照片
        upload_aux(
            driver, '//*[@id="205444676"]/div[2]/div/div/ul/li', path_to_img)
        # 上传作品海报
        upload_aux(
            driver, '//*[@id="205444677"]/div[2]/div/div/ul/li', path_to_img)
        # 上传作品截图
        upload_aux(
            driver, '//*[@id="205444678"]/div[2]/div/div/ul/li', path_to_img)
        # 上传拍摄花絮
        upload_aux(
            driver, '//*[@id="205444679"]/div[2]/div/div/ul/li', path_to_img)
        # 上传预告片 < 300MB
        upload_aux(
            driver, '//*[@id="205444667"]/div[2]/div/div/ul/li', path_to_preview)
        # 上传正片 < 3GB
        upload_aux(
            driver, '//*[@id="205444668"]/div[2]/div/div/ul/li', path_to_mainview)
        # 上传显示表达短片 < 500MB
        upload_aux(
            driver, '//*[@id="205444669"]/div[2]/div/div/ul/li', path_to_limitview)
        button = driver.find_element_by_class_name("fbc_cpBs7Content")
        button.click()
        time_start = time.time()
        # 踏步等待元素过期
        while True:
            try:
                time.sleep(1)
                driver.find_element_by_class_name("fbc_cpBs7Content")
            except Exception as e:
                logger.info("Jump off the circle with e: {}".format(e))
                break
        time_end = time.time()

        try:
            # time.sleep(1)
            el = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element_by_xpath(
                '/html/body/div/div/div[2]/div[2]/div/div[2]/div[1]/span/span'))
            cnt_success += 1
            logger.info("SUCCESS in {:.5f}s!".format(time_end-time_start))
        except Exception as e:
            cnt_fail += 1
            logger.error("FAIL in error: {}!".format(e))
        finally:
            driver.get_screenshot_as_file(
                "C:\\Users\\64980\\Pictures\\IMTest\\"+test_str+".png")
            logger.info("Test cicle {} finished.".format(num))

    logger.info("Final Succcess: {}".format(cnt_success))
    logger.info("Final Fail: {}".format(cnt_fail))

    # print(cnt_fail)

    driver.close()


main()
