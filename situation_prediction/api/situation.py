import numpy as np
from keras.models import load_model
from rest_framework.views import APIView

from response import CustomResponse, ERROR_CODES, ERROR_MESSAGES
from situation_prediction.models import Situation
from situation_prediction.serializers import SituationSerializer
from situation_prediction.utils import calculate_situation_value, MinMaxScaler, MinMaxInverseScaler


def load_predict_model(real_data, max_situ_value=5000, min_situ_value=1000):
    """
    Load predict model and predict situation value.
    """
    processed_data = []
    for data in real_data:
        processed_data.append([data])
    model = load_model('situation_prediction/model/tcn_gcn_model.keras')
    scaled_data = MinMaxScaler(np.array(processed_data), min_situ_value, max_situ_value)

    predict = model(np.array([scaled_data])).numpy()
    predict_value = MinMaxInverseScaler(predict, min_situ_value, max_situ_value)[0][0]

    return predict_value


class SituationPredictionView(APIView):
    # throttle_scope = 'get_situation_prediction'  # 限制访问频率 一分钟一次

    def get(self, request):
        """
        Get situation prediction value.
        """
        predict_step = 5
        try:
            situation_value = calculate_situation_value(predict_step)
            predict_result = load_predict_model(situation_value)
        except Exception as e:
            return CustomResponse(code=ERROR_CODES['PREDICTION_ERROR'], msg=str(e),
                                  data={
                                      "situation_value": None,
                                      "predict_result": None
                                  })
        # 将结果存入数据库
        try:
            # 将situation_value和predict_result结果合并存入数据库
            situation_value.reverse()
            situation = Situation(first_situation_value=situation_value[0],
                                  second_situation_value=situation_value[1],
                                  third_situation_value=situation_value[2],
                                  fourth_situation_value=situation_value[3],
                                  fifth_situation_value=situation_value[4],
                                  prediction_value=predict_result)
            situation.save()
        except Exception as e:
            return CustomResponse(code=ERROR_CODES['DATABASE_ERROR'], msg=str(e),
                                  data={})
        return CustomResponse(data={
            "situation_value": situation_value,
            "predict_result": predict_result
        })


class SituationPredictionHistoryView(APIView):

    def get(self, request):
        """
        Get situation prediction history data.
        """
        try:
            situation_history = Situation.objects.all().order_by('-create_time')[:5]
            # 序列化数据
            ser = SituationSerializer(situation_history, many=True)
        except:
            return CustomResponse({"code": ERROR_CODES['DATABASE_ERROR'], "msg": ERROR_MESSAGES['DATABASE_ERROR'],
                                   "data": None})

        return CustomResponse(data={
            "situation_history": ser.data
        })
