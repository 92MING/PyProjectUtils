# -*- coding: utf-8 -*-
'''封裝並簡化了Selenium的常用操作'''

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By as SeleniumBy
from selenium.webdriver import Chrome as SeleniumChrome
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ChromeOptions as SeleniumChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from typing import Tuple, Union, Literal, Callable
from .TypeUtils import simpleTypeCheck
from ..base_class import CrossModuleEnum
from time import sleep
import json, pickle

class ByMethod(CrossModuleEnum):
    '''封裝了Selenium的By類, 可以清楚知道可選的By類型'''
    XPATH = SeleniumBy.XPATH
    ID = SeleniumBy.ID
    NAME = SeleniumBy.NAME
    TAG_NAME = SeleniumBy.TAG_NAME
    CLASS_NAME = SeleniumBy.CLASS_NAME
    CSS_SELECTOR = SeleniumBy.CSS_SELECTOR
    LINK_TEXT = SeleniumBy.LINK_TEXT
    PARTIAL_LINK_TEXT = SeleniumBy.PARTIAL_LINK_TEXT

class ChromeOptionItem:
    def __init__(self, name:str, default:any=False, format:type=bool, type:Literal['normal','pref']= 'normal',
                 serializeMethod:callable=None):
        '''
        Chrome選項的單個參數封裝
        :param name: 參數名稱, 例如--start-maximized, 用作填寫ChromeOptions.add_argument()、ChromeOptions.add_experimental_option()等方法
        :param default: 默認值, 如果設置為None, 則不會默認添加到add_argument/add_experimental_option中
        :param format: 參數類型, 用作檢查
        :param type: 參數類型, 用於標記是普通參數還是pref參數。pref類的option會在ChromeOptions.add_experimental_option('prefs', {})中添加
        :param serializeMethod: 序列化方法, 如果為None，則直接返回值
        '''
        self._name = name
        self._default = default
        self._format = format
        self._type = type
        self._default = default
        self._serializeMethod = serializeMethod
    @property
    def name(self):
        '''返回參數名稱'''
        return self._name
    @property
    def type(self):
        '''返回參數類型(normal/pref)'''
        return self._type
    @property
    def default(self):
        '''返回serialized後的默認值. 如果為None, 則返回None'''
        if self._default is None:
            return None
        return self.serialize(self._default)
    @property
    def format(self):
        '''返回參數的合法類型'''
        return self._format
    def checkType(self, value):
        '''檢查參數類型是否合法'''
        return simpleTypeCheck(value, self._format)
    def serialize(self, value):
        '''序列化參數值, 如果serializeMethod為None, 則直接返回值'''
        if self._serializeMethod is None:
            return value
        return self._serializeMethod(value)
class ChromeCommonOption(CrossModuleEnum):
    '''封裝了常用的Chrome選項（True/False類型）'''
    START_MAXIMIZED = ChromeOptionItem('--start-maximized')
    '''啟動時最大化'''
    DISABLE_EXTENSIONS = ChromeOptionItem('--disable-extensions')
    '''禁用擴展'''
    DISABLE_INFOBARS = ChromeOptionItem('--disable-infobars')
    '''禁用信息欄'''
    INCOGNITO = ChromeOptionItem('--incognito')
    '''隱身模式'''
    HEADLESS = ChromeOptionItem('--headless')
    '''無頭模式, 不啟動GUI'''
    DISABLE_WEB_SECURITY = ChromeOptionItem('--disable-web-security')
    '''禁用網絡安全'''
    DISABLE_GPU = ChromeOptionItem('--disable-gpu')
    '''禁用GPU'''
    ALLOW_RUNNING_INSECURE_CONTENT = ChromeOptionItem('--allow-running-insecure-content')
    '''允許運行不安全的內容'''
    ALLOW_FILE_ACCESS_FROM_FILES = ChromeOptionItem('--allow-file-access-from-files')
    '''允許從文件訪問文件'''
    ALLOW_EXTERNAL_PAGES = ChromeOptionItem('--allow-external-pages')
    '''允許外部頁面'''
    ALWAYS_OPEN_PDF_EXTERNALLY = ChromeOptionItem('plugins.always_open_pdf_externally', default=True, type='pref')
    '''總是在外部打開PDF'''
    PROMPT_FOR_DOWNLOAD = ChromeOptionItem('download.prompt_for_download', type='pref')
    '''點擊下載時，是否彈框詢問下載位置'''
    USER_AGENT = ChromeOptionItem('--user-agent', default=None, format=str)
    '''設置User-Agent'''
    WINDOW_SIZE = ChromeOptionItem('--window-size', default=None, format=Tuple[int, int], serializeMethod=lambda x: f'{x[0]},{x[1]}')
    '''設置窗口大小'''
    WINDOW_POSITION = ChromeOptionItem('--window-position', default=None, format=Tuple[int, int], serializeMethod=lambda x: f'{x[0]},{x[1]}')
    '''設置窗口位置'''
    WINDOW_NAME = ChromeOptionItem('--window-name', default=None, format=str)
    '''設置窗口名稱'''
    DEFAULT_DOWNLOAD_PATH = ChromeOptionItem('download.default_directory', format=str, type='pref')
    '''設置下載路徑'''
class ChromeOptions:
    '''Chrome選項封裝'''
    def __init__(self):
        self._commonArgs = {}
        self._otherArgs = {}
        self._prefArgs = {}
    @property
    def commonArgs(self)->dict:
        return self._commonArgs.copy()
    @property
    def otherArgs(self)->dict:
        return self._otherArgs.copy()
    @property
    def prefArgs(self)->dict:
        return self._prefArgs.copy()
    def setCommonArg(self, arg: ChromeCommonOption, value):
        '''設置一個參數。'''
        op: ChromeOptionItem = arg.value
        if not op.checkType(value):
            raise TypeError(f'參數{op.name}的類型應為{op.format}，但傳入了{type(value)}')
        self._commonArgs[op.name] = op.serialize(value)
    def setOtherArg(self, name, value):
        '''設置一個在ChromeCommonOption以外的參數。'''
        self._otherArgs[name] = value
    def removeOtherArg(self, name):
        '''移除一個在ChromeCommonOption以外的參數。'''
        self._otherArgs.pop(name) if name in self._otherArgs else None
    def setPrefArg(self, name, value):
        '''設置一個pref類型(且不在ChromeCommonOption內)的參數。'''
        self._prefArgs[name] = value
    def removePrefArg(self, name):
        '''移除一個pref類型的參數。'''
        self._prefArgs.pop(name) if name in self._prefArgs else None

class ChromeService(Service):
    pass

class Chrome(SeleniumChrome):

    def __init__(self, option: ChromeOptions, service:Service, waitMethod:Callable[[float],any]=sleep,**kwargs):
        '''
        初始化Chrome
        :param option: ChromeOptions （注意為這個庫的ChromeOptions而不是Selenium的ChromeOptions）
        :param service: Selenium Service
        :param waitMethod: 等待方法，默認為sleep
        :param kwargs: 其他參數，參見Selenium的Chrome
        '''
        seleniumOptions = SeleniumChromeOptions()
        prefs = {}

        currentCommonArgs = option.commonArgs
        currentOtherArgs = option.otherArgs
        currentPrefArgs = option.prefArgs
        for arg in ChromeCommonOption:
            op:ChromeOptionItem = arg.value
            if op.name in currentCommonArgs:
                if op.type == 'normal':
                    if isinstance(currentCommonArgs[op.name], bool) and currentCommonArgs[op.name] is True:
                        print('add arg', op.name)
                        seleniumOptions.add_argument(op.name)
                    elif not isinstance(currentCommonArgs[op.name], bool):
                        print('add arg', f'{op.name}={currentCommonArgs[op.name]}')
                        seleniumOptions.add_argument(f'{op.name}={currentCommonArgs[op.name]}')
                elif op.type == 'pref':
                    print('add pref', f'{op.name}={currentCommonArgs[op.name]}')
                    prefs[op.name] = currentCommonArgs[op.name]
            else:
                if op.default is not None:
                    if op.type == 'normal':
                        if isinstance(op.default, bool) and op.default is True:
                            print('add arg', op.name)
                            seleniumOptions.add_argument(op.name)
                        elif not isinstance(op.default, bool):
                            print('add arg', f'{op.name}={op.default}')
                            seleniumOptions.add_argument(f'{op.name}={op.default}')
                    elif op.type == 'pref':
                        print('add pref', f'{op.name}={op.default}')
                        prefs[op.name] = op.default
        for name, value in currentOtherArgs.items():
            if value is not None:
                if isinstance(value, bool) and value is True:
                    seleniumOptions.add_argument(name)
                else:
                    seleniumOptions.add_argument(f'{name}={value}')
        for name, value in currentPrefArgs.items():
            prefs[name] = value
        seleniumOptions.add_experimental_option('prefs', prefs)

        super().__init__(options=seleniumOptions, service=service, **kwargs)
        self._waitMethod = waitMethod

    def waitUntilElementAppear(self, key, by=ByMethod.XPATH, timeout=8, OnTimeOut:callable=None)->WebElement:
        '''等待元素出現, 並返回該元素. 若超時則同樣拋出異常'''
        try:
            return WebDriverWait(self, timeout).until(EC.presence_of_element_located((by.value, key)))
        except TimeoutException:
            if OnTimeOut is not None:
                OnTimeOut()
    def waitUntilElementNotAppear(self, key, by=ByMethod.XPATH, timeout=8, OnTimeOut:callable=None):
        '''等待元素消失'''
        try:
            WebDriverWait(self, timeout).until_not(EC.presence_of_element_located((by.value, key)))
        except TimeoutException:
            if OnTimeOut is not None:
                OnTimeOut()
    def hasElement(self, key: str, by=ByMethod.XPATH, timeOut:float = 0.125):
        '''判斷元素是否存在'''
        try:
            WebDriverWait(self, timeOut).until(EC.presence_of_element_located((by.value, key)))
            return True
        except TimeoutException:
            return False

    def setWaitMethod(self, method:Callable[[float],any]):
        '''設置等待方法'''
        self._waitMethod = method

    def changeDownloadPath(self, path:str):
        '''更改下載路徑。執行後需要稍等，否則可能未生效。'''
        self.command_executor._commands["send_command"] = (
            "POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': path}}
        self.execute("send_command", params)
        self._waitMethod(0.25)

    def loadCookie(self: WebDriver, cookiePath: str, mode: Literal['json', 'pickle'] = 'json'):
        '''從文件中讀取Cookie. 確保在load cookie前已經訪問過該網站, 否則會報錯'''
        if mode == 'json':
            with open(cookiePath, 'r') as f:
                cookies = json.load(f)
        elif mode == 'pickle':
            with open(cookiePath, 'rb') as f:
                cookies = pickle.load(f)
        else:
            raise ValueError('mode must be json or pickle')
        for cookie in cookies:
            self.add_cookie(cookie)
    def dumpCookie(driver: WebDriver, outputPath: str, mode: Literal['json', 'pickle'] = 'json'):
        '''將Cookie序列化到文件'''
        if mode == 'json':
            with open(outputPath, 'w') as f:
                json.dump(driver.get_cookies(), f)
        elif mode == 'pickle':
            with open(outputPath, 'wb') as f:
                pickle.dump(driver.get_cookies(), f)
        else:
            raise ValueError('mode must be json or pickle')

__all__ = ['ByMethod', 'ChromeCommonOption', 'ChromeOptions', 'ChromeService', 'Chrome']