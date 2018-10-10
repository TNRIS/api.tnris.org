import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionFilterMapDialog from './collectionFilterMapDialogReducer';
import collectionSearcher from './collectionSearcherReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';
import contact from './contactReducer';

const rootReducer = combineReducers({
  collections,
  collectionDialog,
  collectionFilter,
  collectionFilterMapDialog,
  collectionSearcher,
  resources,
  sorter,
  contact
})

export default rootReducer;
