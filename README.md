## 自备python和pycharm
## 如果遇到需要登录的，把cookie文件删除然后重新运行一遍
## 这是配置文件说明
## 端口说明，安装我这个浏览器之后桌面上右键打开文件所在地址，然后对chrome创建快捷方式，在目标地址后面输入空格加--remote-debugging-port=9222 --user-data-dir="文件地址，自己手动替换"
- `sess`: 场次序号，目前这个只支持只有一个场次的，后续相关的更新完会发布
- `price`: 票档序号，优先选择前面的
- `ticket_num`: 购买票数，购买票数与观影人序号的数量务必一致。
- `viewer_person`: 观影人序号（预先添加实名观影人）
- `driver_path`: 驱动地址，改为自己的驱动地址
- `damai_url`: 大麦首页地址，用于登录。这个不用更改
- `target_url`: 购票的实际地址，需要使用手机端的地址，域名: https://m.damai.cn/ 开头，电脑上可以按F12改为手机窗口然后刷新
- `chrome_path`: 谷歌浏览器的地址，需要更改一下
- `port`: 端口名称
- `switch`: 这个改为T代表点击购买，使用的时候如果想付款就改为T，最后一步不想点击就改其他字符


## selenium下载4.4.1版本
## 如果自己电脑上有谷歌浏览器的先卸载，然后打开我的谷歌浏览器安装包进行安装，去json文件里把各种路径改一下
## 注意目标网址必须是要手机版的，可以在电脑上按F12调整为手机窗口再刷新就可以使用

- `待完善的功能：1.刚打开页面的时候有几率卡出，只出现在第一次，重新运行程序就好`
- `2.自动识别验证`
