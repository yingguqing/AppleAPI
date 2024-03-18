# AppleAPI
基于appstore connect api封装功能。
代码是基于[OKAppleAPI](https://github.com/shede333/OKAppleAPI)原码。只是在原代码基础上，新增了部分接口，封装了些自用功能。



用法:

```python
#!/usr/bin/python3
# coding=utf-8

from AppleAPI import AppStore

if __name__ == '__main__':
  	# 必填
    issuer_id = 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx' 
    # 必填
    key_id = 'XXXXXXXXXX' 						
    # 必填
    key = """
    -----BEGIN PRIVATE KEY-----
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    XXXXXXXX
    -----END PRIVATE KEY----- 
    """

    app = AppStore(issuer_id, key_id, key)
    # 必填
    app.bundle_id = 'com.test.test.a.b'
    # 必填
    app.bundle_name = 'Test'
    # 必填
    app.email = 'test@test.com'
    # 必填
    app.developer_name = 'Name'
    # 可选
    app.country_name = 'US'
    # 可选
    app.password = '123'
    # 可选（上传5图必填）
    app.appstore_version = '1.0'
    # 可选（上传5图必填）
    app.screenshots = {
        'zh-Hans' : {
            "APP_IPHONE_67"             : "C:/Users/Administrator/Desktop/python/iPhone14PM-6.7",
            # "APP_IPHONE_65"           : "iPhone11PM-6.5",
            # "APP_IPHONE_55"           : "iPhone8P-5.5",
            # "APP_IPAD_PRO_3GEN_129"   : "iPadPro-12.9",
            # "APP_IPAD_PRO_129"        : "iPadPro-12.9",
        }
    }	
    # 可选（添加测试设备时必填）
    app.devices = {
        'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx设备id' : '设备名称(可选)，比如：iphone6s'
    }																									
    # 创建Bundle Id
    app.create_bundle_id()
    # 添加测试设备
    app.add_devices()
    # 创建Dis证书
    app.create_certificate(False)
    # 创建Dev证书
    app.create_certificate(True)
    # 创建Dis描述文件
    app.create_profile(False)
    # 创建Dev描述文件
    app.create_profile(True)
    # 上传5图
    app.upload_screenshot()
```



