# Selenium Bot

仓库含两个 Python 脚本，利用`selenium`与`pywinauto`实现自动化表单测试、发送网页信息。

- `im_form_bot.py`: 原用来进行征片网站附件上传测试，使用者可以根据网页结构替换其中 XPath 来实现自动化表单测试。
  - 支持日志打印，配置好日志目录后，可以使用`logger.info()`等接口输出日志信息。
  - 支持 windows10 弹窗的模拟操作，用`pywinauto`库实现
- `im_message.py`: 原用来自动化发送信息
  - 可根据配置文件`config.yml`，定制测试URL，日志信息等。

## LICENSE

MIT
