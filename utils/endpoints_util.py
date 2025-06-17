class EndpointsUtils:
    status_success = "success"
    status_error = "error"

    def create_message_endpoint_response(status, message):
        response = {"status": status, "message": message}

        return response

    def convert_string_request_param_to_boolean(request_param):
        return True if request_param.lower() == "true" else False
