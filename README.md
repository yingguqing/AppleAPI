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
    bundle_id = 'com.test.test.a.b'
    name = 'Test'
    email = 'test@test.com'
    developer_name = 'Name'
    country = 'US'
    password = '123'
    appstore_version = '1.0'
    screenshots = {
        'zh-Hans' : {
            "APP_IPHONE_67"             : "C:/Users/Administrator/Desktop/python/iPhone14PM-6.7",
            # "APP_IPHONE_65"           : "iPhone11PM-6.5",
            # "APP_IPHONE_55"           : "iPhone8P-5.5",
            # "APP_IPAD_PRO_3GEN_129"   : "iPadPro-12.9",
            # "APP_IPAD_PRO_129"        : "iPadPro-12.9",
        }
    }   
    devices = {
        'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx设备id' : '设备名称(可选)，比如：iphone6s'
    }
    # https://developer.apple.com/documentation/appstoreconnectapi/capabilitytype
    capabilitys = ['ASSOCIATED_DOMAINS'] # APPLE_ID_AUTH
    # 创建Bundle Id
    app.create_bundle_id(bundle_id=bundle_id, bundle_name=name, capabilitys=capabilitys)
    # 添加测试设备
    app.add_devices(devices=devices)
    # 创建证书
    app.create_certificate(is_dev=False, email=email, developer_name=developer_name, password=password, country=country)
    # 创建描述文件
    app.create_profile(is_dev=False,bundle_id=bundle_id, name=name)
    # 上传5图
    app.upload_screenshot(bundle_id=bundle_id, appstore_version=appstore_version, screenshots=screenshots)

```



