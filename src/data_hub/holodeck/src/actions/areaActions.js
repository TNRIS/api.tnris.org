import { normalize, schema } from 'normalizr';

import {
  FETCH_AREAS_BEGIN,
  FETCH_AREAS_SUCCESS,
  FETCH_AREAS_FAILURE,
} from '../constants/areaActionTypes';

// -------------
// Initial Store of all areas
// -------------

// --- retrieval lifecycle actions ---
export const fetchAreasBegin = () => ({
  type: FETCH_AREAS_BEGIN
});

export const fetchAreasSuccess = (areas) => ({
  type: FETCH_AREAS_SUCCESS,
  payload: { areas }
});

export const fetchAreasFailure = (error) => ({
  type: FETCH_AREAS_FAILURE,
  payload: { error }
});

// --- retrieve and normalize areas actions ---
function handleErrors(response) {
  // Handle HTTP errors since fetch won't.
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}

function normalizeAreas(originalData) {
  // Normalize the api response json to a flattened state
  // Define areas schema
  const areaSchema = new schema.Entity(
    'areasById',
    undefined,
    { idAttribute: 'area_type_id'}
  );
  return normalize(originalData, [areaSchema]);
}

function areasRecursiveFetcher(dispatch, apiQuery, response) {
  // recursive api endpoint fetcher for handling pagination
  fetch(apiQuery)
  .then(handleErrors)
  .then(res => res.json())
  .then(json => {
    let allResults = response.concat(json.results);
    if (json.next) {
      areasRecursiveFetcher(dispatch, json.next, allResults);
    }
    else {
      let normalizedJson = normalizeAreas(allResults);
      dispatch(fetchAreasSuccess(normalizedJson));
      return normalizedJson;
    }
  })
  .catch(error => dispatch(fetchAreasFailure(error)));
}

export function fetchAreas() {
  const apiQuery = '/api/v1/areas';
  return dispatch => {
    dispatch(fetchAreasBegin());
    return areasRecursiveFetcher(dispatch, apiQuery, []);
  };
}
