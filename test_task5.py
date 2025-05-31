from dash.testing.application_runners import import_app
from dash.testing.browser import Browser
import pytest
import chromedriver_autoinstaller

# 在測試開始前安裝 ChromeDriver
chromedriver_autoinstaller.install()

def test_header_present(dash_duo):
    # 導入應用
    app = import_app('task4')
    dash_duo.start_server(app)
    
    # 驗證標題是否存在
    assert dash_duo.find_element('h1').text == 'Pink Morsel Sales Analysis'

def test_visualization_present(dash_duo):
    # 導入應用
    app = import_app('task4')
    dash_duo.start_server(app)
    
    # 驗證圖表是否存在
    assert dash_duo.find_element('#graph-with-slider') is not None

def test_region_picker_present(dash_duo):
    # 導入應用
    app = import_app('task4')
    dash_duo.start_server(app)
    
    # 驗證區域選擇器是否存在
    assert dash_duo.find_element('#region-dropdown') is not None 