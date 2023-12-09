import datetime
import numpy as np
from abnormal_attack.models import AbnormalTraffic
from abnormal_attack.serializers import AbnormalTrafficSerializer

DEFAULT_SITUATION_VALUE = 1000

# 默认态势倍率
DEFAULT_SITUATION_TIMES = 100


# 统计攻击类型的数量
def calculate_attack_num(serialized_data):
    attack_score = {
        0: 7,
        1: 9,
        2: 5,
        3: 9,
        4: 9,
        5: 9,
        6: 6,
        7: 4,
        8: 3,
        9: 3
    }  # 为每种攻击类型赋予一个权重
    attack_num = 0
    for data in serialized_data:
        attack_type = data['type']
        attack_num += attack_score[attack_type] * DEFAULT_SITUATION_TIMES
    return attack_num + DEFAULT_SITUATION_VALUE


def calculate_situation_value(history_step):
    """
    Get attack event from database within 5(history_step) minutes and calculate situation value.
    """
    current_system_time = datetime.datetime.now()
    situation_value_list = []
    for i in range(1, history_step + 1):
        front_time = current_system_time - datetime.timedelta(minutes=i - 1)
        back_time = current_system_time - datetime.timedelta(minutes=i)
        res = AbnormalTraffic.objects.all().order_by('-time').filter(time__range=[back_time, front_time])
        ser = AbnormalTrafficSerializer(res, many=True)
        if not ser.data:
            situation_value_list.append(DEFAULT_SITUATION_VALUE)
        else:
            situation_value_list.append(calculate_attack_num(ser.data))
    return situation_value_list


def MinMaxScaler(data: np.array, min_value, max_value):
    numerator = data - min_value
    denominator = max_value - min_value
    return numerator / (denominator + 1e-7)


def MinMaxInverseScaler(data: np.array, min_value, max_value):
    return data * (max_value - min_value) + min_value
