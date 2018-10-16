import {
  ADD_COLLECTION_TO_CART,
  REMOVE_COLLECTION_FROM_CART,

  UPLOAD_ORDER_BEGIN,
  UPLOAD_ORDER_SUCCESS,
  UPLOAD_ORDER_FAILURE,

  SUBMIT_ORDER_BEGIN,
  SUBMIT_ORDER_SUCCESS,
  SUBMIT_ORDER_FAILURE
} from '../constants/orderCartActionTypes';

export const addCollectionToCart = (collectionId, formInfo) => {
  return (dispatch) => {
    dispatch({
      type: ADD_COLLECTION_TO_CART,
      payload: { collectionId, formInfo }
    })
  }
};

export const removeCollectionFromCart = (collectionId) => {
  return (dispatch) => {
    dispatch({
      type: REMOVE_COLLECTION_FROM_CART,
      payload: { collectionId }
    })
  }
};

// --- upload lifecycle actions ---
export const uploadOrderBegin = () => ({
  type: UPLOAD_ORDER_BEGIN
});

export const uploadOrderSuccess = () => ({
  type: UPLOAD_ORDER_SUCCESS
});

export const uploadOrderFailure = (error) => ({
  type: UPLOAD_ORDER_FAILURE,
  payload: { error }
});

// --- submit order cart lifecycle actions ---
export const submitOrderBegin = () => ({
  type: SUBMIT_ORDER_BEGIN
});

export const submitOrderSuccess = () => ({
  type: SUBMIT_ORDER_SUCCESS
});

export const submitOrderFailure = (error) => ({
  type: SUBMIT_ORDER_FAILURE,
  payload: { error }
});


// Shared Handle HTTP errors since fetch won't.
function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

// --- upload order file actions ---

function getPolicy(policyUrl, dispatch) {
  return fetch(policyUrl)
         .then(handleErrors)
         .then(res => res.json())
         .then(json => {
           return json;
         })
         .catch(error => dispatch(uploadOrderFailure(error)));
}

export function uploadOrderFile(collectionId, cartInfo) {
  const url = process.env.CONTACT_URL;
  const bucket = 'https://' + process.env.CONTACT_UPLOAD_BUCKET + '.s3.amazonaws.com/';
  let policyUrl;
  if (cartInfo.description === 'AOI') {
    policyUrl = process.env.ZIP_UPLOAD_POLICY_URL;
  }
  else if (cartInfo.description === 'Screenshot') {
    policyUrl = process.env.IMAGE_UPLOAD_POLICY_URL;
  }
  return (dispatch, getState) => {
    dispatch(uploadOrderBegin());
    return getPolicy(policyUrl, dispatch)
           .then((s3policy) => {
             Array.from(cartInfo.files).forEach((file) => {
               console.log(file);
               console.log(bucket);
               console.log(file.name);
               console.log(file.type);
               console.log(file.size);


               const fileKey = 'data-tnris-org-order/' + collectionId + '_' + Date.now() + '_' + file.name;
               let formData = new FormData();
               formData.append('key', fileKey);
               formData.append('acl', 'private');
               formData.append('success_action_status', '201');
               formData.append('success_action_redirect', '');
               formData.append('Content-Type', file.type);
               formData.append('Content-Length', file.size);
               formData.append('AWSAccessKeyId', s3policy.key);
               formData.append('Policy', s3policy.policy);
               formData.append('Signature', s3policy.signature);
               formData.append('file', file, file.name);

               const payload = {
                 // url: bucket,
                 method: 'POST',
                 // headers: {
                 //    // "Content-Type": "application/x-www-form-urlencoded",
                 //    // "Content-Type": "multipart/form-data"
                 //    "Content-Type": "application/json"
                 //    // "Content-Type": 'image'
                 //    // Accept: "application/json, text/plain, */*"
                 // },
                 // mode: 'no-cors',
                 body: formData
               };

               fetch(bucket, payload)
                .then(handleErrors)
                // .then(res => res.json())
                .then(res => {
                  console.log(res);
                  if (res.status === 201) {
                    console.log(cartInfo);
                    // addCollectionToCart(collectionId, )
                    dispatch(uploadOrderSuccess());
                  }
                  else {
                    dispatch(uploadOrderFailure(res.statusText));
                  }
                })
                .catch(error => dispatch(uploadOrderFailure(error)));

             });
           })
           .catch(error => dispatch(uploadOrderFailure(error)));


    // const payload = {
    //   method: 'POST',
    //   headers: {
    //     "Content-Type": "application/json; charset=utf-8"
    //   },
    //   body: JSON.stringify(cartInfo)
    // };
    // fetch(url, payload)
    // .then(handleErrors)
    // .then(res => res.json())
    // .then(json => {
    //   console.log(json);
    //   if (json.status === "success") {
    //     dispatch(uploadOrderSuccess());
    //   }
    //   else if (json.status === "error") {
    //     dispatch(uploadOrderFailure(json.message));
    //   }
    // })
    // .catch(error => dispatch(uploadOrderFailure(error)));
  };
}
