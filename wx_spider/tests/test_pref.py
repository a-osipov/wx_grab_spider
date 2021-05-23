import datetime

import pytest

from wx_spider.pref import serialize_spider_data, deserialize_spider_data, PreferencesBase
from wx_spider.tests.spiders import WxSpiderAbs1, WxSpiderPr1, WxSpiderPr2, TestSpiderPassw


def test_serialize_spider_data():
    protocontrols = WxSpiderAbs1.wx_controls + WxSpiderPr1.wx_controls
    WxSpiderPr1.control_by_name('login').value = 'John'
    WxSpiderPr1.control_by_name('date1').value = datetime.date(2021, 3, 23)
    assert serialize_spider_data(WxSpiderPr1, protocontrols) == {'login': 'John',
                                                                 'date1': '2021-03-23'}


def test_deserialize_spider_data():
    data = {'login': 'John',
            'date1': '2021-03-23'}
    assert deserialize_spider_data(WxSpiderPr1, data) == {'date1': datetime.date(2021, 3, 23),
                                                          'login': 'John'}


@pytest.fixture
def pref():
    from wx_spider import pref
    class _PreferencesBase(PreferencesBase):
        data = {'WxSpiderAbs1': {'login': 'Anna'},
                'WxSpiderPr1': {'date1': '2021-03-23'},
                'WxSpiderNotAbs': {'login': 'Anna'},
                'WxSpiderPr2': {'name2': 'Rembo', 'login': 'Pedro'},
                'frame': {'spider_name': 'DemoSpider3'}
                }

        def get(self, key):
            return self.data.get(key)

        def update_preferences(self, preferences):
            self.data.update(preferences)

        def get_password(self, spider_name, control_name):
            passwords = {'TestSpiderPassw': {'password': '12345'}}
            return passwords[spider_name].get(control_name)

    pref.set_preferences(_PreferencesBase)
    return pref


class TestPreferencesBase:

    def test_get_spider_preference(self, pref):
        preference1 = pref.get_spider_preference(WxSpiderPr1)
        assert preference1 == {'login': 'Anna',
                               'date1': datetime.date(2021, 3, 23)}
        preference2 = pref.get_spider_preference(WxSpiderPr2)
        assert preference2 == {'login': 'Pedro', 'name2': 'Rembo'}

    def test_set_spider_preference(self, pref):
        WxSpiderPr1.control_by_name('login').value = 'Maksim'
        WxSpiderPr1.control_by_name('date1').value = datetime.date(2021, 3, 27)
        pref.set_spider_preference(WxSpiderPr1)
        assert pref.PREFERENCES.data['WxSpiderPr1'] == {'date1': '2021-03-27'}
        assert pref.PREFERENCES.data['WxSpiderAbs1'] == {'login': 'Maksim'}
        WxSpiderPr2.control_by_name('login').value = 'Maksim'
        WxSpiderPr2.control_by_name('name2').value = 'Biden'
        pref.set_spider_preference(WxSpiderPr2)
        assert pref.PREFERENCES.data['WxSpiderPr2'] == {'login': 'Maksim', 'name2': 'Biden'}

    def test_get_frame_preference(self, pref):
        assert pref.get_frame_preference() == {'spider_name': 'DemoSpider3'}

    def test_set_frame_preference(self, pref):
        pref.set_frame_preference({'spider_name': 'DemoSpider2'})
        assert pref.PREFERENCES.data['frame'] == {'spider_name': 'DemoSpider2'}

    def test_get_passwords(self, pref):
        assert pref.get_passwords(TestSpiderPassw) == {'password': '12345'}
        assert pref.get_passwords(WxSpiderPr2) == {}
