from rest_framework.views import APIView


class MessageResponseMixin(APIView):
    """Mixin that wraps successful responses with a message and data.

    Views can set `message = 'custom message'` or override `get_message()`.
    The mixin will not modify error responses (status_code >= 400).
    """

    message = None

    def get_message(self):
        return self.message

    def finalize_response(self, request, response, *args, **kwargs):
        resp = super().finalize_response(request, response, *args, **kwargs)

        # If there's no data or it's an error response, don't change it
        try:
            data = resp.data
        except Exception:
            return resp

        if resp.status_code >= 400:
            return resp

        # If already wrapped, do nothing
        if isinstance(data, dict) and {'status_code', 'message', 'data'}.issubset(set(data.keys())):
            return resp

        if isinstance(data, dict) and 'message' in data and 'data' in data and 'status_code' not in data:
            # view already provided {'message','data'} shape
            return resp

        # Determine a message
        msg = self.get_message()
        if not msg:
            # Try to derive from queryset model if available
            queryset = getattr(self, 'queryset', None)
            model_name = None
            if queryset is not None:
                try:
                    model_name = queryset.model._meta.verbose_name.title()
                except Exception:
                    try:
                        model_name = queryset.model.__name__
                    except Exception:
                        model_name = None

            verb = 'retrieved' if request.method == 'GET' else 'success'
            if model_name:
                msg = f"{model_name} {verb}"
            else:
                msg = 'success'

        resp.data = {'message': msg, 'data': data}
        return resp
