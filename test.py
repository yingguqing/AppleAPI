#!/usr/bin/python3
# coding=utf-8

from pathlib import Path
import json
from AppleAPI import AppStore


if __name__ == '__main__':
    key_path = Path('~/Desktop/AppleAPI/api_keys.json').expanduser()
    json_info = json.loads(key_path.read_text())
    # 必填
    issuer_id = json_info["issuer_id"]
    # 必填
    key_id = json_info["key_id"]
    # 必填
    key = json_info["key"]

    app = AppStore(issuer_id, key_id, key)
    bundle_id = json_info["bundle_id"]
    name = json_info["bundle_name"]
    email = json_info["email"]
    developer_name = json_info["developer_name"]
    country = json_info["country"]
    password = json_info["password"]
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
