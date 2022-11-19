from flask import request

class ApiHelper:
    def __init__(self):
        pass

    def convert_query_params(self, page = 1, limit = 15):
        try:
            if "page" in request.args and int(request.args["page"]):
                page = int(request.args["page"])

            if "limit" in request.args and (int(request.args["limit"]) and (int(request.args["limit"]) < 16 and int(request.args["limit"]) > 0)):
                limit = int(request.args["limit"])
        except Exception as e:
            raise Exception(e)

        return [page, limit]

    def pagination_model(self, current_page, total_results, page_total):
        return {
            "current_page" : current_page,
            "current_total_results" : total_results,
            "page_total" : page_total,
        }
