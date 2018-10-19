import {
  ADD_COLLECTION_TO_CART,
  REMOVE_COLLECTION_FROM_CART,
  EMPTY_CART,

  UPLOAD_ORDER_BEGIN,
  UPLOAD_ORDER_SUCCESS,
  UPLOAD_ORDER_FAILURE,

  SUBMIT_ORDER_BEGIN,
  SUBMIT_ORDER_SUCCESS,
  SUBMIT_ORDER_FAILURE
} from '../constants/orderCartActionTypes';

//  --- cart item management ---
export const addCollectionToCart = (collectionId, formInfo) => {
  addCollectionToLocalStorage(collectionId, formInfo);
  return (dispatch) => {
    dispatch({
      type: ADD_COLLECTION_TO_CART,
      payload: { collectionId, formInfo }
    })
  }
};

export const removeCollectionFromCart = (collectionId) => {
  removeCollectionFromLocalStorage(collectionId);
  return (dispatch) => {
    dispatch({
      type: REMOVE_COLLECTION_FROM_CART,
      payload: { collectionId }
    })
  }
};

export const emptyCart = () => {
  emptyStoredShoppingCart();
  return (dispatch) => {
    dispatch({
      type: EMPTY_CART
    })
  }
}

// --- local storage cart replication management ---
export const fetchStoredShoppingCart = () => {
  return dispatch => {
    if (typeof(Storage) !== void(0)) {
      const current = localStorage.getItem("data_shopping_cart") ? JSON.parse(localStorage.getItem("data_shopping_cart")) : null;
      console.log(current);
      if (current) {
        return Object.keys(current).map((collectionId) => {
          const formInfo = current[collectionId];
          return dispatch({
            type: ADD_COLLECTION_TO_CART,
            payload: { collectionId, formInfo }
          });
        });
      }
    }
    else {
      return true;
    }
  }
}

export const emptyStoredShoppingCart = () => {
  if (typeof(Storage) !== void(0)) {
    if (localStorage.getItem("data_shopping_cart")) {
      localStorage.removeItem("data_shopping_cart");
    }
  }
}

export const addCollectionToLocalStorage = (collectionId, formInfo) => {
  if (typeof(Storage) !== void(0)) {
    const current = localStorage.getItem("data_shopping_cart") ? JSON.parse(localStorage.getItem("data_shopping_cart")) : {};
    const formObj = {};
    formObj[collectionId] = formInfo;
    const updated = {...current, ...formObj};
    localStorage.setItem("data_shopping_cart", JSON.stringify(updated));
  }
}

export const removeCollectionFromLocalStorage = (collectionId) => {
  if (typeof(Storage) !== void(0)) {
    const current = localStorage.getItem("data_shopping_cart") ? JSON.parse(localStorage.getItem("data_shopping_cart")) : null;
    if (current) {
      const { [collectionId]:value , ...removedOrders } = current;
      localStorage.setItem("data_shopping_cart", JSON.stringify(removedOrders));
    }

  }
}

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
  const bucket = 'https://' + process.env.CONTACT_UPLOAD_BUCKET + '.s3.amazonaws.com/';
  let policyUrl;
  if (cartInfo.type === 'AOI') {
    policyUrl = process.env.ZIP_UPLOAD_POLICY_URL;
  }
  else if (cartInfo.type === 'Screenshot') {
    policyUrl = process.env.IMAGE_UPLOAD_POLICY_URL;
  }
  return (dispatch, getState) => {
    dispatch(uploadOrderBegin());
    return getPolicy(policyUrl, dispatch)
           .then((s3policy) => {
             const cartFiles = Array.from(cartInfo.files);
             const fileDetails = {};
             cartFiles.forEach((file, index) => {

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
                 method: 'POST',
                 body: formData
               };

               fileDetails[index] = {
                 'filename': file.name,
                 'link': "https://s3.amazonaws.com/contact-uploads/" + fileKey
               };

               fetch(bucket, payload)
                .then(handleErrors)
                .then(res => {
                  console.log(index);
                  if (res.status === 201 && index === cartFiles.length - 1) {
                    const filesKey = 'files';
                    const { [filesKey]:value , ...removedOrders } = cartInfo;
                    console.log(removedOrders);
                    const newCart = {
                      ...removedOrders,
                      attachments: fileDetails
                    };
                    console.log(collectionId);
                    console.log(newCart);
                    dispatch(addCollectionToCart(collectionId, newCart));
                    dispatch(uploadOrderSuccess());
                  }
                  else if (res.status !== 201) {
                    dispatch(uploadOrderFailure(res.statusText));
                  }
                })
                .catch(error => dispatch(uploadOrderFailure(error)));
             });
           })
           .catch(error => dispatch(uploadOrderFailure(error)));
  };
}

// --- submit order form actions ---
export function submitOrderCartForm(formInfo) {
  // const url = 'https://tnris.supportsystem.com/api/tickets.json';
  const url = process.env.CONTACT_URL;
  return (dispatch, getState) => {
    dispatch(submitOrderBegin());
    const payload = {
      method: 'POST',
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        // "X-API-Key": process.env.OSTICKET_API_KEY
      },
      body: JSON.stringify(formInfo)
    };
    fetch(url, payload)
    .then(handleErrors)
    .then(res => res.json())
    .then(json => {
      console.log(json);
      if (json.status === "success") {
        dispatch(emptyCart());
        dispatch(submitOrderSuccess());
      }
      else if (json.status === "error") {
        dispatch(submitOrderFailure(json.message));
      }
    })
    .catch(error => dispatch(submitOrderFailure(error)));
  };
}
