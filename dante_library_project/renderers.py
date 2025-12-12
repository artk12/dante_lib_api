from rest_framework.renderers import JSONRenderer
from http import HTTPStatus


class CustomJSONRenderer(JSONRenderer):
    """
    Wrap all DRF JSON responses in the shape:
    {
        "status_code": <int>,
        "message": <str>,
        "data": <original data>
    }
    """
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # If renderer_context available, try to get status code from response
        status_code = None
        if renderer_context:
            resp = renderer_context.get('response')
            if resp is not None:
                status_code = getattr(resp, 'status_code', None)

        # If the view already provided the final wrapped format, return as-is
        if isinstance(data, dict) and {'status_code', 'message', 'data'}.issubset(set(data.keys())):
            return super().render(data, accepted_media_type, renderer_context)

        # If the view provided {'message': ..., 'data': ...} allow that
        if isinstance(data, dict) and 'message' in data and 'data' in data and 'status_code' not in data:
            message = data.get('message')
            data = data.get('data')
        else:
            # Determine default status_code if not available
            if status_code is None:
                status_code = 200 if data is not None else 204

            # Derive a friendly message
            if isinstance(data, dict):
                if 'detail' in data:
                    message = data.get('detail')
                elif status_code >= 400:
                    first_msg = None
                    for v in data.values():
                        if isinstance(v, (list, tuple)) and v:
                            first_msg = v[0]
                            break
                        if isinstance(v, str):
                            first_msg = v
                            break
                        if isinstance(v, dict):
                            for vv in v.values():
                                if isinstance(vv, (list, tuple)) and vv:
                                    first_msg = vv[0]
                                    break
                                if isinstance(vv, str):
                                    first_msg = vv
                                    break
                            if first_msg:
                                break
                    message = first_msg if first_msg else HTTPStatus(status_code).phrase
                else:
                    message = 'OK'
            else:
                message = HTTPStatus(status_code).phrase if status_code >= 400 else 'OK'

        payload = {
            'status_code': status_code,
            'message': message,
            'data': data
        }

        return super().render(payload, accepted_media_type, renderer_context)
