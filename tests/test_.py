try:
    from app.serializers import *
    from app.utils import *
except (ModuleNotFoundError, ImportError):
    from Pearson.app.serializers import *
    from Pearson.app.utils import *
from django import urls
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
import time
import pytest


@pytest.mark.parametrize('param', [('index')])
def test_index_page(client, param):
    url = urls.reverse(param)
    resp = client.get(url)
    assert resp.status_code == 200


class TestPOSTCalculate(APITestCase):
    def test_post_200(self):
        url = reverse('calculate')
        user = User.objects.create(username='TestUser')
        data = {
            "user_id": 1,
            "data": {
                "x_data_type": "height",
                "y_data_type": "weight",
                "x": [
                    {
                        "date": "2015-10-10",
                        "value": 1000
                    },
                    {
                        "date": "2015-10-11",
                        "value": 20.02
                    },
                    {
                        "date": "2015-10-12",
                        "value": 33.02
                    },
                    {
                        "date": "2015-10-13",
                        "value": 21.06
                    },
                    {
                        "date": "2015-10-14",
                        "value": 21.06
                    },
                    {
                        "date": "2015-10-15",
                        "value": 21.06
                    }, {
                        "date": "2015-10-17",
                        "value": 21.06
                    }, {
                        "date": "2015-10-16",
                        "value": 21.06
                    }
                ],
                "y": [
                    {
                        "date": "2015-10-10",
                        "value": 100.06
                    },
                    {
                        "date": "2015-10-11",
                        "value": 50.3
                    },
                    {
                        "date": "2015-10-12",
                        "value": 10.06
                    },
                    {
                        "date": "2015-10-13",
                        "value": 5.06
                    },
                    {
                        "date": "2015-10-14",
                        "value": 100.06
                    },
                    {
                        "date": "2015-10-16",
                        "value": 50.3
                    },
                    {
                        "date": "2015-10-15",
                        "value": 10.06
                    },
                    {
                        "date": "2015-10-17",
                        "value": 5.06
                    }
                ]
            }
        }
        expected = {"detail": "Success"}
        self.client.force_authenticate(user)
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.json(), expected)
        self.assertEqual(response.status_code, 200)

    def test_post_400(self):
        user = User.objects.create(username='TestUser')
        url = reverse('calculate')
        data = {"data": "some invalid data"}
        self.client.force_authenticate(user)
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_without_auth_401(self):
        url = reverse('calculate')
        data = {"data": "some invalid data"}
        response = self.client.post(url, json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)


class TestGETCorrelation(APITestCase):
    def test_get_200(self):

        # ---- Prepare environment -----

        url = reverse('calculate')
        user = User.objects.create(username='TestUser')
        data = {
            "user_id": 1,
            "data": {
                "x_data_type": "height",
                "y_data_type": "weight",
                "x": [
                    {
                        "date": "2015-10-10",
                        "value": 1000
                    },
                    {
                        "date": "2015-10-11",
                        "value": 20.02
                    },
                    {
                        "date": "2015-10-12",
                        "value": 33.02
                    },
                    {
                        "date": "2015-10-13",
                        "value": 21.06
                    },
                    {
                        "date": "2015-10-14",
                        "value": 21.06
                    },
                    {
                        "date": "2015-10-15",
                        "value": 21.06
                    }, {
                        "date": "2015-10-17",
                        "value": 21.06
                    }, {
                        "date": "2015-10-16",
                        "value": 21.06
                    }
                ],
                "y": [
                    {
                        "date": "2015-10-10",
                        "value": 100.06
                    },
                    {
                        "date": "2015-10-11",
                        "value": 50.3
                    },
                    {
                        "date": "2015-10-12",
                        "value": 10.06
                    },
                    {
                        "date": "2015-10-13",
                        "value": 5.06
                    },
                    {
                        "date": "2015-10-14",
                        "value": 100.06
                    },
                    {
                        "date": "2015-10-16",
                        "value": 50.3
                    },
                    {
                        "date": "2015-10-15",
                        "value": 10.06
                    },
                    {
                        "date": "2015-10-17",
                        "value": 5.06
                    }
                ]
            }
        }
        self.client.force_authenticate(user)
        self.client.post(url, json.dumps(data), content_type="application/json")
        time.sleep(1)
        # ----- test ------

        url = reverse('correlation')
        response = self.client.get(url, {"x_data_type": "height", "y_data_type": "weight", "user_id": 1})
        print(response.json(), response.status_code)
        self.assertEqual(response.status_code, 200)
        expected = {
            "user_id": 1,
            "x_data_type": "height",
            "y_data_type": "weight",
            "correlation": {
                "value": 0.578,
                "p_value": 0.036
            }
        }
        self.assertEqual(response.json(), expected)


def test_serializer():
    _dict = {"user_id": 5, 'data': {"x_data_type": "str",
                                    "y_data_type": "str",
                                    "x": [{"date": "YYYY-MM-DD", "value": 10}],
                                    "y": [{"date": "YYYY-MM-DD", "value": 10}]}
             }
    string = '''{
        "user_id": 5,
        "data": {
            "x_data_type": "str",
            "y_data_type": "str",
            "x": [
                {
                    "date": "YYYY-MM-DD",
                    "value": 10
                }
            ],
            "y": [
                {
                    "date": "YYYY-MM-DD",
                    "value": 10
                }
            ]
        }
    }'''
    serialized = ReceivedDataSerializer(string).data
    assert _dict == serialized
