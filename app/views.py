from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

try:  # For pytest
    from Pearson.app.serializers import ReceivedDataSerializer
    from Pearson.app.utils import CalculateRequestProcessor, GetCorrelationRequestProcessor
except ModuleNotFoundError:
    from .serializers import ReceivedDataSerializer
    from .utils import CalculateRequestProcessor, GetCorrelationRequestProcessor


class CalculateDataAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ReceivedDataSerializer(request.body)
        processor = CalculateRequestProcessor(serializer.data)
        processor.save()
        if processor.errors or serializer.errors:
            error = processor.errors if processor.errors else serializer.errors
            return JsonResponse(error, status=400)
        return JsonResponse({'detail': 'Success'}, status=200)


class GetCorrelationAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = GetCorrelationRequestProcessor(request)
        if result.error:
            return JsonResponse(result.error, status=404)
        else:
            result = result.correlation_result
            response = {"user_id": result.user_id.id,
                        "x_data_type": result.first_param,
                        "y_data_type": result.second_param,
                        "correlation": {
                            "value": round(result.value, 3),
                            "p_value": round(result.p_value, 3)
                        }}
            return JsonResponse(response, status=200)


def index(request):
    return HttpResponse('200, Service available')
