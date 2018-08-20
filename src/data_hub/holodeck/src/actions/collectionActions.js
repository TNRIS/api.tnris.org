export const FETCH_COLLECTIONS_BEGIN   = 'FETCH_COLLECTIONS_BEGIN';
export const FETCH_COLLECTIONS_SUCCESS = 'FETCH_COLLECTIONS_SUCCESS';
export const FETCH_COLLECTIONS_FAILURE = 'FETCH_PRODUCTS_FAILURE';

export const fetchCollectionsBegin = () => ({
  type: FETCH_COLLECTIONS_BEGIN
});

export const fetchCollectionsSuccess = collections => ({
  type: FETCH_COLLECTIONS_SUCCESS,
  payload: { collections }
});

export const fetchCollectionsFailure = error => ({
  type: FETCH_COLLECTIONS_FAILURE,
  payload: { error }
});

// Handle HTTP errors since fetch won't.
function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

export function fetchCollections() {
  return dispatch => {
    dispatch(fetchCollectionsBegin());
    return fetch('/api/v1/collections')
      .then(handleErrors)
      .then(res => res.json())
      .then(json => {
        dispatch(fetchCollectionsSuccess(json.results));
        return json.results;
      })
      .catch(error => dispatch(fetchCollectionsFailure(error)));
  };
}
