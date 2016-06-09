# WooYun_spider
按厂商列表爬的 只保存了漏洞详情部分

保存在d盘 wooyun文件夹下 按厂商分类 html打开

log在控制台中看

运行过程中报错情况：
  
1.漏洞名称相同 控制台会报错 而且只保存其中一个（暂时没想出好的办法）

2.有的漏洞名称在网页源代码中是js表示（暂时不懂原因） 导致 list_name 长度小于 list_link 长度 遍历时会出现out of index错误 d:\wooyun\erro.txt中保存了出错的厂商和页数 （暂时不知道如何解决 只能手动）

3.Max retries exceeded with url错误 暂时没发现有大的影响
