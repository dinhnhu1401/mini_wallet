###############################################################################
# This file performed how the project can be manually tested.
# You can leverage it as a reference for your own test cases.
# Using Linux with curl command
###############################################################################

curl --location --request POST 'http://localhost:5000/api/v1/init' --form 'customer_xid="ea0212d3-abd6-406f-8c67-868e814a2436"'
curl --location --request POST 'http://localhost:5000/api/v1/init' --form 'customer_xid="abc12345-abd6-406f-8c67-868e814a2436"'
# {
#   "data": {
#     "token": "978559859abd0efceefe3a71ab7b06ae"
#   },
#   "status": "success"
# }
# {
#   "data": {
#     "token": "ae79fc28d1435aa6181e939f9f7af44c"
#   },
#   "status": "success"
# }
curl --location --request POST 'http://localhost:5000/api/v1/init' --form 'customer_xid="ea0212d3-abd6-406f-8c67-868e814a2436"'
# {
#   "data": {
#     "error": {
#       "customer_xid": [
#         "Existed Token"
#       ]
#     }
#   },
#   "status": "fail"
# }
curl --location --request POST 'http://localhost:5000/api/v1/wallet' --header 'Authorization: Token 978559859abd0efceefe3a71ab7b06ae'
# {
#   "data": {
#     "wallet": {
#       "balance": 0,
#       "enabled_at": "2022-03-27 16:56:47",
#       "id": "3713fb48-adb4-11ec-8def-b0227ae96d22",
#       "owned_by": "ea0212d3-abd6-406f-8c67-868e814a2436",
#       "status": "enabled"
#     }
#   },
#   "status": "success"
# }
curl --location --request GET 'http://localhost:5000/api/v1/wallet' --header 'Authorization: Token 978559859abd0efceefe3a71ab7b06ae'
# {
#   "data": {
#     "wallet": {
#       "balance": 0,
#       "enabled_at": "2022-03-27 16:56:47",
#       "id": "3713fb48-adb4-11ec-8def-b0227ae96d22",
#       "owned_by": "ea0212d3-abd6-406f-8c67-868e814a2436",
#       "status": "enabled"
#     }
#   },
#   "status": "success"
# }
curl --location --request GET 'http://localhost:5000/api/v1/wallet' --header 'Authorization: Token wrong_token'
# {
#   "data": {
#     "error": "This wallet is not activated."
#   },
#   "status": "fail"
# }
curl --location --request POST 'http://localhost:5000/api/v1/wallet' --header 'Authorization: Token wrong_token'
# {
#   "data": {
#     "error": "This wallet need to be initialized first."
#   },
#   "status": "fail"
# }