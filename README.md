# simplecms
An ugly and simple local net work client information manager.

## 文件说明
server.py为服务器  
ui_c.py为客户端图形界面  
ui_s.py为服务器图形界面  
data为缓存文件，注意保证文件夹里留有本文件，此文件中保存数据  
hash为用户信息储存文件，默认用户名为1，密码为1
host中储存服务器ip以及地址  
其余文件为依赖文件  

## 服务端配置
先配置host中ip和端口，替换原来位置即可。  
用默认用户登录服务器客户端，可以添加用户或者更改用户。（目前只要在本地登录任何用户都有管理权限）  
可以用导出和导入功能讲xls文件导入，文件放在同文件夹下，注意输入全名，否则将出错

## 客户端配置
客户端只要有host文件即可，data，hash不用放入。  

## 一些废话
这个项目做了半个暑假，目前并未投入使用，可能有大量bug  
内网通信用了rsa，密码保存用了MD5。