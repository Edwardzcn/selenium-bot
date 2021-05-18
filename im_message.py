#!/bin/bash

# 自动表单
# 基于python + selenium
from copy import Error
from os import close
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import random
import re
import logging
import yaml
from pathlib import Path


def set_chrome_options(cfg):
    if cfg['chrome']['with_ui'] == 'true':
        return None
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        "user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
    return chrome_options


def filter_emoji(desstr, restr=''):
    # 过滤带emoji的比如
    # Sugar friend👿.D
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


def get_random_message(user_name):
    message_title = "【IM两岸青年影展】"
    random_num = random.randint(0, 1e5)
    message_body = "\n\nhi," + \
        str(user_name) + "！\n\n2021第二届IM两岸青年影展征片时间截止延长至6月15日啦！\n\n主竞赛单元共计29个奖项，最高奖30万人民币，现面向全球青年创作者征集参赛作品。\n\n报名链接：https://imff.mike-x.com/nvVv2，如有问题可联系工作人员：17750285085，影展将于8月27~29日于福建平潭举行，期待您的参与! Usr:" + str(random_num)
    return message_title+message_body


def logger_config(cfg):
    '''
    logger是日志对象，handler是流处理器，console是控制台输出（没有console也可以，将不会在控制台输出，会在日志文件中输出）
    '''
    # 获取logger对象,取名
    log_path=cfg['log']['path']
    log_name=cfg['log']['name']
    log_level=cfg['log']['level']
    logger = logging.getLogger(log_name)
    # 获取文件日志句柄并设置日志级别，第二层过滤
    if log_path == None:
        log_path = Path.cwd()/('msg_from_'+ str(cfg['page']['st_num']) + '_to_' + str(cfg['page']['ed_num']) +'.log')
    else:
        log_path = Path.cwd()/log_path
    # console相当于控制台输出
    # handler文件输出。获取流句柄并设置日志级别，第二层过滤
    filehdl = logging.FileHandler(log_path, encoding='UTF-8')
    console = logging.StreamHandler()
    # 生成并设置文件日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehdl.setFormatter(formatter)

    # logger对象添加句柄
    logger.addHandler(console)
    logger.addHandler(filehdl)

    # logger 输出的详细程度
    logger.setLevel(log_level)
    return logger


def login_certify(driver, cfg, logger):
    # try log_in certify
    logger.info("|" + "".center(40, "=") + "|")
    logger.info("|" + "Now navigate to 'login_url".center(40) + "|")
    driver.get(cfg['login']['url'])
    id = cfg['login']['id']
    pwd = cfg['login']['pwd']
    logger.info("|" + "".center(40, "-") + "|")
    logger.info("|" + "From the configuration file".ljust(40) + "|")
    logger.info("|" + "Username:{usr}".format(usr=id).ljust(40) + "|")
    logger.info("|" + "Password:{pwd}".format(pwd=pwd).ljust(40) + "|")
    sleep(2)
    elem = driver.find_element_by_xpath(
        "/html/body/div[2]/section/main/div[2]/div/div/div/form/div[2]/div/div/span/span/span/input")
    elem.send_keys("18695770923")
    elem = driver.find_element_by_xpath(
        "/html/body/div[2]/section/main/div[2]/div/div/div/form/div[3]/div/div/span/span/input")
    elem.send_keys("a123456a")
    button = driver.find_element_by_xpath(
        '//*[@id="__next"]/section/main/div[2]/div/div/div/form/div[4]/div/div/span/button')
    button.click()
    logger.info("|" + "Finish.".center(40) + "|")
    logger.info("|" + "".center(40, "=") + "|")
    sleep(5)
    return driver


def main():

    # 加载配置
    with open('config.yml', 'r') as stream:
        cfg = yaml.load(stream=stream, Loader=yaml.FullLoader)
    # 启动日志
    logger = logger_config(cfg)
    logger.debug("%v", cfg)

    # 启动 Chrome Driver
    try:
        opts = set_chrome_options(cfg)
        driver = webdriver.Chrome(chrome_options=opts)
    except Error as e:
        logger.error("Fail to start the Chrome driver.")
        logger.error(e)
        exit(1)
    finally:
        logger.info("Success to  start the Chrome driver.\n\n")

    # 进行 login 验证
    try:
        driver = login_certify(driver=driver, cfg=cfg, logger=logger)
    except Error as e:
        logger.error("Fail to log in.")
        logger.error(e)
        exit(1)
    finally:
        logger.info("Success to Log in.\n\n")

    # 主要逻辑
    # catch exception ElementNotInteractableException
    people_cnt = 0
    # 跳转至创作人页面
    start_num = int(cfg['page']['st_num'])
    end_num = int(cfg['page']['ed_num'])
    logger.debug("Start page num:{} End page num:{}".format(
        start_num, end_num))
    for pg_num in range(start_num, end_num):
        page_url = cfg['main']['url'] + str(pg_num)
        logger.info("|" + "".center(40, "=") + "|")
        logger.info("|" + "Now navigate to 'main_url".center(40) + "|")
        logger.info("|" + "".center(40, "-") + "|")
        # year type = 1 标识三年以下
        logger.debug(page_url)
        logger.info(
            "|" + "Switch to page: {pg_num}".format(pg_num=pg_num).ljust(40) + "|")
        logger.info("|" + "Number of people received the message:{pp_num}".format(
            pp_num=people_cnt).ljust(40) + "|")
        try:
            driver.get(page_url)
            # 等待页面加载完成
            sleep(5)
            buttons = driver.find_elements_by_class_name("bg-white")
            for _, button in enumerate(buttons):
                button.click()
                people_cnt += 1
                # 等待小窗口加载完成
                sleep(2)
                user_name = driver.find_element_by_xpath(
                    "/html/body/div[9]/div/div[1]/div[2]/h4").text
                message = get_random_message(filter_emoji(user_name))
                elem = driver.find_element_by_xpath(
                    "/html/body/div[9]/div/div[2]/textarea")
                # 填充信息，这里有可能有特殊字体问题，先忽略
                elem.send_keys(message)
                sleep(1)
                # # 关闭按钮
                # driver.find_element_by_xpath(
                #     "/html/body/div[9]/div/div[1]/span").click()
                # 发送按钮
                driver.find_element_by_xpath(
                    "/html/body/div[9]/div/div[3]/div/span[2]").click()
                sleep(2)
                # 发送成功页面暂不下载
                driver.find_element_by_class_name("ex-show-tooltip").click()
                # 确定
                sleep(0.5)
                driver.find_element_by_xpath(
                    "/html/body/div[10]/div/div[3]/div/span[2]").click()

        except Exception as e:
            # 遇到问题，休息30mins，page_num ++ 再继续
            logger.error("Error in page{}:".format(pg_num))
            logger.error(e)
            logger.error("Rest for 1h")
            sleep(4000)
            pg_num += 1
            logger.error("Omit the error. Continue")
            continue


main()
