import { combineReducers } from "redux";

import collections from './collectionReducer';
import resources from './resourceReducer';
import dialog from './dialogReducer';

const rootReducer = combineReducers({
  collections,
  resources,
  dialog
})

export default rootReducer;
