import datetime, uuid, base64, hmac, os, hashlib
api_url = str(os.environ.get('API_URL'))

def computeSignature(requestURI: str, requestMethod: str, payLoad: str, accountId: str, key: str):
    """
    Compute a HMAC signature for fiserv
    """
    requestTimeStamp: str = str(int(datetime.datetime.now().timestamp()))
    nonce: str = str(uuid.uuid4())
    requestContentBase64String: str = payLoad
    signatureRawData: str = accountId + requestMethod + requestURI + requestTimeStamp +  nonce + requestContentBase64String
    secretKeyByteArray = base64.b64decode(key)
    signature = signatureRawData.encode("utf8")
    signatureBytes = hmac.new(secretKeyByteArray, signature, hashlib.sha256)
    requestSignatureBase64String = base64.b64encode(signatureBytes.digest())
    HmacRaw = f"{accountId}:{requestSignatureBase64String.decode()}:{nonce}:{requestTimeStamp}"
    HmacValue = base64.b64encode(HmacRaw.encode("utf8"))
    return HmacValue

def generate_fiserv_hmac(
    url: str,
    method: str,
    payLoad: str,
    accountId: str,
    key: str
):
    return computeSignature(url, method, payLoad, accountId, key)

def generate_basic_auth():
    """
    Generate basic authentication token for fiserv
    """
    basic = f"{os.environ.get('FISERV_API_BASIC_AUTH_USERNAME')}:{os.environ.get('FISERV_API_BASIC_AUTH_PWD')}"
    basic = base64.b64encode(basic.encode("utf8"))
    return basic

def generate_fiserv_post_body(
        payment_method: str,
        order_details_id: str,
        template_id: int,
        total: float,
        transactionfee: float,
        order_details: dict,
        charge: bool = False
    ):
    """
    Return an object to be used in fdms body.
    Args:
        payment_method (str): Payment type of this transaction. Either ACH or CC.
        order_details_id (str): unique order id.
        template_id (str): Template id.
        total (float): Total of purchase without fee.
        transactionfee (float): DIR fee.
        order_details (dict): Order details object.
        charge (bool): Whether we are using the charge api. Defaults to False
    """

    f_tran_amount  = "{:.2f}".format(round(total + transactionfee, 2))
    f_total_amount = "{:.2f}".format(total)
    f_tran_fee = "{:.2f}".format(transactionfee)

    clx_struct = generate_clx_stream(f_total_amount, f_tran_fee, order_details_id, payment_method)

    # In the HPP v3 api as of June 5, 2025 clxstream must be enclosed in an array.
    if not charge:
        clx_struct = [clx_struct]

    post_body = {
        "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),  # required
        "companycode": os.environ.get("FISERV_COMPANY_CODE"),  # required
        "currencycode": "USD",  # required
        "customerid": os.environ.get("FISERV_CUSTOMER_ID"),  # required
        "userid": os.environ.get("FISERV_USER_ID"),  # required
        "redirecturl": "https://" + api_url + "/api/v2/contact/order/redirect?status=success",
        "cancelredirecturl": "https://" + api_url +"/api/v2/contact/order/redirect?status=cancel",  # Optional but we can use it.
        "reference": "UPI",  # Required
        "templateid": template_id,  # required
        "transactiontype": "S",  # required: S means for a sale.
        "transactionamount": f_tran_amount,  # required
        "paymentmode": payment_method,  # As needed.
        "sendemailreceipts": "Y",
        "cof": "C",  # Optional, means Card on file, and C means customer.
        "cofscheduled": "N",  # Optional, N means no don't schedule card to be filed.
        "ecomind": "E",  # Optional, E means ECommerce, this is a note on the origin of transaction
        "orderid": "580WD" + order_details_id,  # Local order ID; we use it as a reference to get transaction info.
        # "purchaseorder": "", Optional,
        "type": "C",  # Optional, but C means customer.
        "savepaymentmethod": "N",  # Optional
        "saveatcustomer": "N",  # Optional
        "displaycardssavedatcustomer": "N",  # Optional
        "customer": {  # Optional customer data
            "customername": order_details["name"],
            "addressline1": order_details["address"],
            "addressline2": "",
            "city": order_details["city"],
            "state": order_details["state"],
            "zipcode": order_details["zipcode"],
            "country": "",  # Add state to order_details
            "phone": order_details["phone"],
            "email": order_details["email"],
        },
        "payments": [  # required
            {
                "mode": payment_method,
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
            }
        ],
        "level3": generate_level_three(f_total_amount, f_tran_fee),
        "clxstream": clx_struct
    }

    if payment_method == "ACH":
        post_body["payments"]["achseccode"] = "WEB"
        post_body["payments"]["achsecdescriptor"] = "PURCHASE"
        post_body["payments"]["feeachseccode"] = "WEB"
        post_body["payments"]["feeachsecdescriptor"] = "PURCHASE"

    return post_body

def generate_clx_stream(f_total_amount, f_tran_fee, order_details_id, payment_method):
    """
    """
    return {
            "transaction": {
                "agency": "580",
                "batchid": "",
                "company": "Texas Water Development Board",
                "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
                "department": "Texas Geographic Information Office",
                "description": "TxGIO DataHub order",
                "fee": f_tran_fee,
                "localreferenceid": "580WD" + order_details_id,
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
                "paymenttype": payment_method,
                "quantity": "1",
                "reportlines": "3",  # This should be how many report line details attributes.
                "sku": "DHUB",  # Should be correct.
                "type": "ecommerce",
                "unitprice": f_total_amount,
                "vendorid": os.environ.get("FISERV_SERVICE_CODE"),
                "reportlinedetails": [{
                    "id": "USAS1",
                    "attributes": [
                        {
                            "name": "USAS1COBJ",
                            "value": "3719",
                            "type": "String",
                        },
                        {
                            "name": "USAS1PCA",
                            "value": "19001",
                            "type": "String",
                        },
                        {
                            "name": "USAS1TCODE",
                            "value": "195",
                            "type": "String",
                        },
                        {
                            "name": "USAS1AMOUNT",
                            "value": f_total_amount,
                            "type": "DOLLAR",
                        },
                    ],
                },
                {
                    "id": "USAS2",
                    "attributes": [
                        {
                            "name": "USAS2COBJ",
                            "value": "3879",
                            "type": "String",
                        },
                        {
                            "name": "USAS2PCA",
                            "value": "07768",
                            "type": "String",
                        },
                        {
                            "name": "USAS2TCODE",
                            "value": "179",
                            "type": "String",
                        },
                        {
                            "name": "USAS2AMOUNT",
                            "value": f_tran_fee,
                            "type": "DOLLAR",
                        },
                    ],
                },
                {
                    "id": "USAS3",
                    "attributes": [
                        {
                            "name": "USAS3COBJ",
                            "value": "7219",
                            "type": "String",
                        },
                        {
                            "name": "USAS3TCODE",
                            "value": "265",
                            "type": "String",
                        },
                        {
                            "name": "USAS3PCA",
                            "value": "07768",
                            "type": "String",
                        },
                        {
                            "name": "USAS3AMOUNT",
                            "value": f_tran_fee,
                            "type": "DOLLAR",
                        },
                    ],
                }],
                "additionalinfo": [
                    {
                        "key": "servicecode",
                        "value": os.environ.get("FISERV_SERVICE_CODE"),
                    }
                ],
            }
        }
    

def generate_level_three(f_total_amount, f_tran_fee): 
    return [
        {
            "linenumber": "1.000",
            "productcode": "TXGIO_DATA",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "TxGIO DataHub order",
            "unitcost": f_total_amount,
            "lineitemtotal": f_total_amount,
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA",
        },
        {
            "linenumber": "2.000",
            "productcode": "TXDIR_FEE",
            "taxrate": "0",
            "quantity": "1",
            "itemdescriptor": "Texas.gov fee**",
            "unitcost": f_tran_fee,
            "lineitemtotal": f_tran_fee,
            "taxamount": "0",
            "commoditycode": "",
            "unitofmeasure": "EA",
        },
    ]