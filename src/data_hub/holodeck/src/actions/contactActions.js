import {
  SUBMIT_CONTACT_BEGIN,
  SUBMIT_CONTACT_SUCCESS,
  SUBMIT_CONTACT_FAILURE
} from '../constants/contactActionTypes';


// --- retrieval lifecycle actions ---
export const submitContactBegin = () => ({
  type: SUBMIT_CONTACT_BEGIN
});

export const submitContactSuccess = () => ({
  type: SUBMIT_CONTACT_SUCCESS
});

export const submitContactFailure = (error) => ({
  type: SUBMIT_CONTACT_FAILURE,
  payload: { error }
});

// --- submit contact information to contact-app actions ---
//

// Handle HTTP errors since fetch won't.
function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

export function submitContactTnrisForm(formInfo) {
  // const url = 'https://tnris.supportsystem.com/api/tickets.json';
  const url = 'http://localhost:8001/';
  return (dispatch, getState) => {
    dispatch(submitContactBegin());
    const payload = {
      method: 'POST',
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        // "X-API-Key": process.env.OSTICKET_API_KEY
      },
      // mode: 'no-cors',
      // data: JSON.stringify(formInfo),
      // dataType: 'json'
      body: JSON.stringify(formInfo)
    };
    console.log(payload);
    fetch(url, payload)
    .then(handleErrors)
    .then(res => res.json())
    .then(json => {
      console.log(json);
      if (json.status === "success") {
        dispatch(submitContactSuccess());
      }
      else if (json.status === "error") {
        dispatch(submitContactFailure(json.message));
      }
    })
    .catch(error => dispatch(submitContactFailure(error)));
  };
}
