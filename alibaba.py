from alibabacloud_nlp_automl20191111.client import Client as nlp_automl20191111Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_nlp_automl20191111 import models as nlp_automl_20191111_models


class AliClient:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> nlp_automl20191111Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = 'nlp-automl.cn-hangzhou.aliyuncs.com'
        return nlp_automl20191111Client(config)

    @staticmethod
    def process(content: str) -> dict:
        client = AliClient.create_client('LTAI5tRXr8op1Nz7Wc2VNSNL', 'X6uSbJGBnDyqdJvrPUCFX32YXbm7Ee')
        get_predict_result_request = nlp_automl_20191111_models.GetPredictResultRequest(model_id=8391, content=content, model_version='V1')
        result = client.get_predict_result(get_predict_result_request)
        return result.to_map()
