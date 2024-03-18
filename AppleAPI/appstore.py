#!/usr/bin/python3
# coding=utf-8
# 苹果后台操作，基于AppStore Content API

import os
from .apple_api_agent import TokenManager, APIAgent, die
from .models import *
from pathlib import Path
from typing import List

class AppStore(object):
    
    def __init__(self, issuer_id:str, key_id:str, key:str) -> None:
        # 解析配置文件内容
        if not issuer_id:
            die('isserId不能为空')
        elif len(issuer_id) != 36:
            die('isserId长度不正确')

        if not key_id:
            die('keyId不能为空')

        if not key:
            die('key不能为空')

        self._foldPath = None
        # 创建请求的Agent
        token_manager = TokenManager(issuer_id=issuer_id, key_id=key_id, key=key)
        self.agent = APIAgent(token_manager)

    @property
    def foldPath(self) -> Path:
        """文件保存路径"""
        #  在脚本目录下创建一个开发者名称的文件夹，文件保存在这个文件夹下
        if self._foldPath is None:
            self._foldPath = Path().resolve().joinpath('file')
            # 创建文件夹
            if not self._foldPath.exists():
                self._foldPath.mkdir()
        return self._foldPath

    def p12Path(self, is_dev:bool, password:str, isOverwrite:bool = True) -> Path:
        """p12文件保存路径"""
        title = 'dev' if is_dev else 'dis'
        if password:
            p12name = f'{title}_密码{password}.p12'
        else:
            p12name = '{title}_无密码.p12'
        path = self.foldPath.joinpath(p12name)
        if isOverwrite and path.exists():
            os.remove(path)
        return path
    
    def profilePath(self, is_dev:bool, bundle_id:str, name:str, isOverwrite:bool = True) -> Path:
        """描述文件保存路径"""
        title = 'dev' if is_dev else 'dis'
        name = name if "*" in bundle_id else bundle_id
        path =  self.foldPath.joinpath(f'{name}_{title}.mobileprovision')
        if isOverwrite and path.exists():
            os.remove(path)
        return path
    
    def appstore_bundle_id(self, bundle_id:str) -> BundleId:
        """
        获取对应的BundleId
        @param identifier: BundleId的identifier, 例如：com.hello.world
        @return:
        """
        list = self.agent.list_bundle_id(filters={"identifier":bundle_id})
        return list[0] if list else None

    def create_certificate(self, is_dev:bool, email:str, developer_name:str, password:str, country:str):
        """
        创建证书
        @param is_dev: true:创建开发证书，false:发布证书
        @param email: 邮箱地址
        @param developer_name:开发都名称
        @param password: p12文件密码
        @param country: 国家代码。比如：IN，US
        """
        if not email:
            die('email不能为空')
        if not developer_name:
            die('name不能为空')
        if not password:
            die('password不能为空')
        title = 'dev' if is_dev else 'dis'
        print(f'开始创建{title}证书')
        save_path = self.p12Path(is_dev, password=password)
        self.agent.create_certificates_export_p12(is_dev=is_dev, email=email, developer_name=developer_name, password=password, country=country, save_path=save_path)
        print(f'{title}证书保存成功:{save_path}')

    def create_bundle_id(self, bundle_id:str, bundle_name:str, capabilitys: List[str]=None):
        """
        创建Bundle Id
        @param bundle_id: 唯一标识
        @param bundle_name: 名称
        @param capabilitys: 权限。比如：ASSOCIATED_DOMAINS，APPLE_ID_AUTH
        """
        if not bundle_id:
            die('bundle_id不能为空')
        if not bundle_name:
            die('bundle_name不能为空')
        item = self.appstore_bundle_id(bundle_id)
        if item:
            print('Bundle Id已存在，不能创建')
            return
        print('开始创建Bundle Id')
        # 创建Bundle Id
        result_dict = self.agent.register_bundle_id(bundle_id=bundle_id, name=bundle_name)
        tmp_dict = result_dict.get('data', {})
        app_bundle_id = BundleId(tmp_dict)
        if app_bundle_id.attributes.identifier == bundle_id:
            # 开启相应权限功能
            self.capability(app_bundle_id, capabilitys)
            print('创建Bundle Id完成')
        else:
            print('创建Bundle Id失败')

    def capability(self, bundle_id: BundleId, capabilitys: List[str]):
        """开启相应权限功能"""
        if not capabilitys or not bundle_id:
            return
        for type in capabilitys:
            settings = []
            # 苹果登录
            if type == "APPLE_ID_AUTH":
                settings = [
                    {
                        "key": "TIBURON_APP_CONSENT",
                        "options": [
                            {
                                "key": "PRIMARY_APP_CONSENT"
                            }
                        ]
                    }
                ]
            self.agent.enable_a_capabilities(inner_bundle_id=bundle_id.id, capability_type=type, settings=settings)

    def get_cer_list(self, is_dev=True) -> List[Certificate]:
        """
        获取cer列表
        @param is_dev: 是否为iOS的dev证书，反之则为iOS的release类型，默认True
        @return:
        """
        all_cer_list = self.agent.list_certificates()

        if is_dev:
            supported_types = [CertificateType.DEVELOPMENT, CertificateType.IOS_DEVELOPMENT]
        else:
            supported_types = [CertificateType.DISTRIBUTION, CertificateType.IOS_DISTRIBUTION]
        cer_list = []
        for tmp_cer in all_cer_list:
            platform = tmp_cer.attributes.platform
            is_ios = (not platform) or (platform == BundleIdPlatform.IOS)
            if is_ios and (tmp_cer.attributes.certificate_type in supported_types):
                # 支持iOS设备，且为支持类型
                cer_list.append(tmp_cer)
        return cer_list
    
    def create_profile(self, is_dev:bool, bundle_id:str, name:str):
        """
        创建描述文件
        @param is_dev: true:开发，false:发布
        @param bundle_id: bundle id
        @param name: 描述文件名称
        """
        if not bundle_id:
            die('bundleId不能为空')
        if not name:
            die('name不能为空')
        title = 'dev' if is_dev else 'dis'
        print(f'开始创建{title}描述文件')
        name = f'{name}_{title}'
        profile_list = self.agent.list_profiles(filters={"name": name})
        for profile in profile_list:
            self.agent.delete_a_profile(profile.id)
        type = ProfileType.IOS_APP_DEVELOPMENT.value if is_dev else ProfileType.IOS_APP_STORE.value
        attrs = ProfileCreateReqAttrs(name, type)
        appstore_bundle_id = self.appstore_bundle_id(bundle_id)
        cer_list = self.get_cer_list(is_dev)
        devices = self.agent.list_devices(filters={"platform": "IOS", "status": DeviceStatus.ENABLED.name}) if is_dev else []
        # 创建新的Profile
        profile = self.agent.create_a_profile(attrs=attrs, bundle_id=appstore_bundle_id, devices=devices, certificates=cer_list)
        filePath = self.profilePath(is_dev, bundle_id=bundle_id, name=name)
        profile.attributes.save_content(filePath)
        print(f'{title}描述文件创建并下载完成:{filePath}')

    def add_devices(self, devices:dict[str:str]):
        """
        添加设备
        @param devices: 测试设备。格式：{'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx设备id' : '设备名称(可选)，比如：iphone6s'}
        """
        if not devices:
            die('devices不能为空')
        # 获取device设备列表，排除掉已添加的设备
        print('开始添加设备')
        device_list = self.agent.list_devices()
        existDevices = []
        modifyDevices = []
        successDevices = []
        faildDevices = []
        # 添加设备
        for udid, name in devices.items():
            # 取出后台测试中，和准备添加的设备id相同的的有设备
            in_devices = list(filter(lambda item: item.udid.lower() == udid.lower(), device_list))
            if len(in_devices) > 0:
                device = in_devices[0]
                # 如果当前设备的状态是禁用，修改设备状态
                if device.status == DeviceStatus.DISABLED:
                    self.agent.modify_a_device(device_id=udid)
                    modifyDevices.append(f'{name}:{udid}')
                else:
                    existDevices.append(f'{name}:{udid}')
                continue

            info, device = self.agent.register_a_device(DeviceCreateReqAttrs(name, udid))
            if device is not None and device.udid == udid:
                successDevices.append(f'{name}:{udid}')
            else:
                faildDevices.append(f'{name}:{udid} -> {info}:{device}')

        existStr = '\n'.join(existDevices)
        modifyStr = '\n'.join(modifyDevices)
        successStr = '\n'.join(successDevices)
        faildStr = '\n'.join(faildDevices)
        if existStr:
            print(f'以下设备已存在，无需添加：\n{existStr}')
        if modifyStr:
            print(f'以下设备状态已修改：\n{modifyStr}')
        if successStr:
            print(f'以下设备添加成功：\n{successStr}')
        if faildStr:
            print(f'以下设备添加失败：\n{faildStr}')

    def upload_screenshot(self, bundle_id:str, appstore_version: str, screenshots:dict[str:dict[str:str]]):
        """
        上传App截图,自动上传对应尺寸目录下所有图片文件
        @param bundle_id: bundle id
        @param appstore_version: 提审版本号
        @param screenshots: 5图相关。格式：
        {
            'zh-Hans' : {
                "APP_IPHONE_67"           : "C:/Users/Administrator/Desktop/python/iPhone14PM-6.7",
                "APP_IPHONE_65"           : "C:/Users/Administrator/Desktop/python/iPhone11PM-6.5",
                "APP_IPHONE_55"           : "C:/Users/Administrator/Desktop/python/iPhone8P-5.5",
                "APP_IPAD_PRO_3GEN_129"   : "C:/Users/Administrator/Desktop/python/iPadPro-12.9",
                "APP_IPAD_PRO_129"        : "C:/Users/Administrator/Desktop/python/iPadPro-12.9",
            }
        }
        """
        if not bundle_id:
            die('bundle_id不能为空')
        if not screenshots:
            die('screenshot不能为空')
        if not appstore_version:
            die('version不能为空')
        print("开始上传App截图")
        # 检查5图配置的目录是否存在
        currentPath = Path().resolve()
        for (local, screenshotDic) in screenshots.items():
            typeDic = {}
            for (type, dir) in screenshotDic.items():       
                if not Path(dir).exists():
                    dir = currentPath.joinpath(dir)
                    if not Path(dir).exists():
                        die(f'{local}语言下 {type} 5图目录 {dir} 不存在')
                typeDic[type] = dir
            screenshots[local] = typeDic
        # 所有5图尺寸集
        appleIds = self.agent.list_apps(filters={"bundleId": bundle_id})
        if appleIds:
            appleId = appleIds[0].id
        else:
            die(f"通过Bundle id：{bundle_id}未找到apple id")
        print(f"apple id:{appleId}")
        resourceIds = self.agent.list_appstore_version(appleId, filters={"versionString":appstore_version, "platform":"IOS"})
        if resourceIds:
            resourceId = resourceIds[0].id
        else:
            die("未找到资源id")
        print(f"资源id:{resourceId}")
        locale_list = self.agent.list_localization(resourceId)
        for (local,screenshotDic) in screenshots.items():
            in_locals = list(filter(lambda item: item.locale.lower() == local.lower(), locale_list))
            if not in_locals:
                select_local = self.agent.create_localization(resourceId, local)
                print(f"创建App本地化语言：{local}")
            else:
                select_local = in_locals[0]

            for (type, dir) in screenshotDic.items():
                try:
                    screenshotType = ScreenshotDisplayType[type.upper()]
                except:
                    die(f"截图类型{type}不存在")
                # 先查找图集，如果没有就创建图集
                print(f'正在获取截图集')
                sets = self.agent.list_app_screenshot_set(select_local.id, filters={"screenshotDisplayType":screenshotType.name})
                if sets:
                    print(f'获取截图集成功')
                    set_id = sets[0].id
                    # 获取截图集中所有的截图
                    print(f'正在获取截图集中的所有截图,并删除')
                    screenshots = self.agent.list_app_screenshot(set_id)
                    if screenshots:
                        # 删除所有已存在截图
                        for item in screenshots:
                            self.agent.delete_app_screenshot(item.id)
                else:
                    print(f'未找到 {screenshotType} 截图集，准备创建')
                    set_id = self.agent.create_app_screenshot_set(select_local.id, screenshotType)
 
                retry = 0
                # 获取dir下的所有图片文件路径
                for file in Path(dir).iterdir():
                    if file.is_file() and file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                        screenshot = self.agent.create_app_screenshot(set_id, file)
                        while True:
                            if retry > 3:
                                print(f'{file} 上传失败')
                                break
                            self.agent.upload_app_screenshot(screenshot, file)
                            state = self.agent.verify_app_screenshot(screenshot.id, file)
                            if state == AppScreenshotState.UPLOAD_COMPLETE:
                                print(f'{file} 上传成功')
                                break
                            else:
                                retry += 1
                                print(f'{file} 上传失败，正在进行第{retry}次重试')

