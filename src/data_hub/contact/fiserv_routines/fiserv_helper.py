import datetime, uuid, base64, hmac, os, hashlib


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
        order: object,
        template_id: str,
        total: float,
        transactionfee: float,
        order_details: object
    ):
    """
    Return an object to be used in fdms body.
    Args:
        payment_method (str): Payment type of this transaction. Either ACH or CC.
        order (object): Order object with details.
        template_id (str): Template id.
        total (float): Total of purchase without fee.
        transactionfee (float): DIR fee.
        order_details (object): Order details object.
    """
    return {
        "accountid": os.environ.get("FISERV_DEV_ACCOUNT_ID"),  # required
        "companycode": os.environ.get("FISERV_COMPANY_CODE"),  # required
        "currencycode": "USD",  # required
        "customerid": os.environ.get("FISERV_CUSTOMER_ID"),  # required
        "userid": os.environ.get("FISERV_USER_ID"),  # required
        "redirecturl": "https://localhost:8000/api/v1/contact/order/redirect?status=success",
        "cancelredirecturl": "https://data.geographic.texas.gov/order/redirect?status=cancel",  # Optional but we can use it.
        "reference": "UPI",  # Required
        "templateid": template_id,  # required
        "transactionType": "S",  # required: S means for a sale.
        "transactionamount": round(total + transactionfee, 2),  # required
        "paymentmode": payment_method,  # As needed.
        "sendemailreceipts": "Y",
        "cof": "C",  # Optional, means Card on file, and C means customer.
        "cofscheduled": "N",  # Optional, N means no don't schedule card to be filed.
        "ecomind": "E",  # Optional, E means ECommerce, this is a note on the origin of transaction
        "orderid": "580"
        + str(
            order.order_details_id
        ),  # Optional Local order ID; we use it as a reference to get transaction info.
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
                "mode": payment_method,  # Check these. CC has been checked TODO: Check ACH
                "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
            }
        ],
        "level3": [
            {
                "linenumber": "1.000",
                "productcode": "TXGIO_DATA",
                "taxrate": "0",
                "quantity": "1",
                "itemdescriptor": "TxGIO DataHub order",
                "unitcost": total,
                "lineitemtotal": total,
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
                "unitcost": transactionfee,
                "lineitemtotal": transactionfee,
                "taxamount": "0",
                "commoditycode": "",
                "unitofmeasure": "EA",
            },
        ],
        "clxstream": [
            {
                "transaction": {
                    "agency": "580",
                    "batchid": "",
                    "company": "Texas Water Development Board",
                    "customerid": os.environ.get("FISERV_CUSTOMER_ID"),
                    "department": "Texas Geographic Information Office",
                    "description": "TxGIO DataHub order",
                    "fee": str(transactionfee),
                    "localreferenceid": "580" + str(order.order_details_id),
                    "merchantid": os.environ.get("FISERV_MERCHANT_ID"),
                    "paymenttype": payment_method,
                    "quantity": "1",
                    "reportlines": "3",  # This should be how many report line details attributes.
                    "sku": "DHUB",  # Should be correct.
                    "type": "ecommerce",
                    "unitprice": total,
                    "vendorid": os.environ.get("FISERV_SERVICE_CODE"),
                    "reportlinedetails": [
                        {
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
                                    "value": total,
                                    "type": "String",
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
                                    "value": transactionfee,
                                    "type": "String",
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
                                    "value": transactionfee,
                                    "type": "String",
                                },
                            ],
                        },
                    ],
                    "additionalinfo": [
                        {
                            "key": "servicecode",
                            "value": os.environ.get("FISERV_SERVICE_CODE"),
                        }
                    ],
                }
            }
        ],
    }
