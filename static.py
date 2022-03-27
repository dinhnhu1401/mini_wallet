# List API
url_init = "/api/v1/init"
url_wallet = "/api/v1/wallet"
url_deposits = "/api/v1/wallet/deposits"
url_withdrawals = "/api/v1/wallet/withdrawals"

api_fields = {
    url_init: ['customer_xid'], # POST
    url_wallet: ['is_disabled'], # PATCH
    url_deposits: ['amount', 'reference_id'], # POST
    url_withdrawals: ['amount', 'reference_id'] # POST
}