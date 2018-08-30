import { normalize, schema } from 'normalizr';

import {
  FETCH_COLLECTIONS_BEGIN,
  FETCH_COLLECTIONS_SUCCESS,
  FETCH_COLLECTIONS_FAILURE
} from '../constants/collectionActionTypes';

export const fetchCollectionsBegin = () => ({
  type: FETCH_COLLECTIONS_BEGIN
});

export const fetchCollectionsSuccess = (collections) => ({
  type: FETCH_COLLECTIONS_SUCCESS,
  payload: { collections }
});

export const fetchCollectionsFailure = (error) => ({
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

// Normalize the api response json to a flattened state
function normalizeCollections(originalData) {
  // Define collections schema
  const collectionSchema = new schema.Entity(
    'collectionsById',
    undefined,
    { idAttribute: 'collection_id'}
  );
  return normalize(originalData, [collectionSchema]);
}

export function fetchCollections() {
  return dispatch => {
    dispatch(fetchCollectionsBegin());
    return fetch('/api/v1/collections')
      .then(handleErrors)
      .then(res => res.json())
      .then(json => {
        let normalizedJson = normalizeCollections(json.results);
        dispatch(fetchCollectionsSuccess(normalizedJson));
        return normalizedJson;
      })
      .catch(error => dispatch(fetchCollectionsFailure(error)));
  };
}
