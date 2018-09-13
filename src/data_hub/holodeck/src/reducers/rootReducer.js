import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import mapDialog from './mapDialogReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';

const rootReducer = combineReducers({
  collections,
  collectionDialog,
  collectionFilter,
  mapDialog,
  resources,
  sorter
})

export default rootReducer;
