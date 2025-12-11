from flask import jsonify, request

#### Test API pour un filtrage dynamique ####

# def get_data(srv_Flask):

#     @srv_Flask.route('/api/data')
#     def api_data():
#         year = request.args.get('year', type=int)
#         DATA = [
#             {"year": 2018, "value": 1},
#             {"year": 2019, "value": 3},
#             {"year": 2020, "value": 4},
#             {"year": 2021, "value": 2}
#         ]

#         if year:
#             DATA = [d for d in DATA if d["year"] == year]
#         return jsonify(DATA)