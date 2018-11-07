import {
  SET_COLLECTION_TIMESLIDER,
  // SET_COLLECTION_TIMESLIDER_RANGE
} from '../constants/collectionTimesliderActionTypes';

export const setCollectionTimeslider = (collectionTimeslider) => {
  return (dispatch) => {
    dispatch({
      type: SET_COLLECTION_TIMESLIDER,
      payload: { collectionTimeslider }
    })
  }
};

// export const setCollectionTimesliderRange = (collectionTimesliderRange) => {
//   return (dispatch) => {
//     dispatch({
//       type: SET_COLLECTION_TIMESLIDER_RANGE,
//       payload: { collectionTimesliderRange }
//     })
//   }
// };
