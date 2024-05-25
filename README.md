# CF-Auto-Test
---
`CF-AUTO-Test`
是一个基于 [CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest) 的自动化测试使用不同端口的 CDN IP

_瞎写的_

---
## 使用
1. 创造`list.txt`在执行目录
2. 按照`ip:port`格式每行一个放入文件(防呆设计:会自动去除https://、http://，域名、ip若没有:port会自动加上:443)
3. 给CloudflareST赋予执行权限
   ```
   chmod +x Cloudflare
   ```
   若你是Windows平台，在[此处](https://github.com/XIU2/CloudflareSpeedTest/releases)获取二进制可执行文件，重命名为 `CloudflareST.exe` 当前目录下放置可执行文件
   内置 `CloudflareST` 为amd64架构，若你不是，请自行更换二进制文件
4. 执行
   ```
   python main.py [-tll 最大延迟] [-sl 下载速度下限] [-tl 最小延迟]
   ```
5. 在 `result.cvs` 查看结果