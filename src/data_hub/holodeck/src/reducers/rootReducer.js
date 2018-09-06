import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import mapDialog from './mapDialogReducer';
import resources from './resourceReducer';

const rootReducer = combineReducers({
  collections,
  collectionDialog,
  mapDialog,
  resources,

})

export default rootReducer;
