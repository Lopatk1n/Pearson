from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from scipy import stats
try:
    from Pearson.app.models import CorrelationResult
except ModuleNotFoundError:
    from .models import CorrelationResult

# ---- for POST calculate/ ------


class CalculateRequestProcessor:
    def __init__(self, request_data: dict):
        self.request_data = request_data
        self.errors = None

    def __get_user_or_error(self):
        try:
            user_id = self.request_data["user_id"]
            user = User.objects.get(id=user_id)
            return user
        except (ObjectDoesNotExist, KeyError, TypeError) as e:
            self.errors = {'detail': f'{e}'}
            return None

    def __get_params(self):
        try:
            x_data = {item["date"]: item["value"] for item in self.request_data["data"]["x"]}
            y_data = {item["date"]: item["value"] for item in self.request_data["data"]["y"]}
            x_param = self.request_data["data"]["x_data_type"]
            y_param = self.request_data["data"]["y_data_type"]
        except (KeyError, TypeError):
            self.errors = {'detail': 'Key error'}
            return
        return x_data, y_data, x_param, y_param

    def __create_or_get_db_entry(self, user: User, x_param: str, y_param: str):
        try:
            entry = CorrelationResult.objects.get(user_id=user, first_param=x_param, second_param=y_param)
        except ObjectDoesNotExist:
            try:  # switch params
                entry = CorrelationResult.objects.get(user_id=user, first_param=y_param, second_param=x_param)
            except ObjectDoesNotExist:
                entry = CorrelationResult.objects.create(user_id=user, first_param=x_param, second_param=y_param)
        return entry

    def __dates_matching(self, x_data, y_data):
        temp = []
        for date in x_data:
            try:
                temp.append([x_data[date], y_data[date]])
            except KeyError:
                self.errors = {'detail': 'Dates should match'}
                return False
        return True

    def save(self):
        user_or_error = self.__get_user_or_error()
        if user_or_error is None:  # user_or_error is error
            return
        if type(user_or_error) == User and self.request_data["data"]:
            user = user_or_error
            try:
                x_data, y_data, x_param, y_param = self.__get_params()
            except (TypeError, ValueError):
                return
            if len(x_data) != len(y_data):
                self.errors = {'detail': 'Counts of parameters should match'}
                return
            if self.__dates_matching(x_data, y_data):
                entry = self.__create_or_get_db_entry(user, x_param, y_param)
                calculator = CorrelationCalculator(x_data, y_data)
                entry.value = calculator.value
                entry.p_value = calculator.p_value
                entry.save()
            else:
                return
        else:
            self.errors = {'detail': 'Wrong data'}
            return


class CorrelationCalculator:
    def __init__(self, x_sequence, y_sequence):
        self.x = x_sequence
        self.y = y_sequence
        self.sequence_length = len(self.x)
        self.value = self.__get_pearson_value()
        self.p_value = self.__get_p_value()

    def __sort_sequences_by_date(self):
        united_sequence = []
        for date in self.x:
            united_sequence.append([self.x[date], self.y[date]])
        return united_sequence  # [[x0,y0],[x1,y1],...[xn,yn]] where x, y are values

    def __get_pearson_value(self):
        sequence = self.__sort_sequences_by_date()
        only_x = [item[0] for item in sequence]
        only_y = [item[1] for item in sequence]
        sum_x = sum(only_x)
        sum_y = sum(only_y)
        mx = sum_x / self.sequence_length
        my = sum_y / self.sequence_length
        dx = [x - mx for x in only_x]
        dy = [y - my for y in only_y]
        dx_pow2 = [x ** 2 for x in dx]
        dy_pow2 = [y ** 2 for y in dy]
        dx_mul_dy = [dx[i] * dy[i] for i in range(0, len(dx))]
        sum_dx_pow2 = sum(dx_pow2)
        sum_dy_pow2 = sum(dy_pow2)
        sum_dx_mul_dy = sum(dx_mul_dy)
        rxy = sum_dx_mul_dy/((sum_dx_pow2 * sum_dy_pow2)**0.5)
        return rxy

    def __get_p_value(self):
        t = self.value*((self.sequence_length - 2)**0.5)/((1 - self.value)**0.5)
        p_value = stats.t.sf(abs(t), df=self.sequence_length - 2)
        return p_value

# ---- for GET correlation/ ------


class GetCorrelationRequestProcessor:  # return matching CorrelationResult
    def __init__(self, request):
        self.request = request
        self.error = None
        try:
            self.x_data_type, self.y_data_type, self.user_id = self.__get_params_from_request()
        except TypeError:
            pass
        if not self.error:
            self.correlation_result = self.__get_matching_result()

    def __get_params_from_request(self):
        try:
            x_data_type = self.request.GET.get("x_data_type", None)
            y_data_type = self.request.GET.get("y_data_type", None)
            user_id = self.request.GET.get("user_id", None)
        except TypeError:
            self.error = {"detail": "Bad params or Type error"}
            return
        if not all((x_data_type, y_data_type, user_id)):
            self.error = {"detail": "Bad params or empty data error"}
            return
        else:
            return x_data_type, y_data_type, user_id

    def __get_matching_result(self):
        try:
            user = User.objects.get(id=self.user_id)
        except (ObjectDoesNotExist, AttributeError):
            self.error = {"detail": "user does not exist"}
            return
        try:
            result = CorrelationResult.objects.get(user_id=user,
                                                   first_param=self.x_data_type,
                                                   second_param=self.y_data_type)
        except ObjectDoesNotExist:
            try:  # switch params
                result = CorrelationResult.objects.get(user_id=user,
                                                       first_param=self.y_data_type,
                                                       second_param=self.x_data_type)
            except ObjectDoesNotExist:
                self.error = {"detail": "404"}
                return
        return result
