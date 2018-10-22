import { combineReducers } from "redux";

import areas from './areaReducer';
import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionFilterMap from './collectionFilterMapReducer';
import collectionFilterMapDialog from './collectionFilterMapDialogReducer';
import collectionSearcher from './collectionSearcherReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';
import contact from './contactReducer';
import orderCart from './orderCartReducer';

const rootReducer = combineReducers({
  areas,
  collections,
  collectionDialog,
  collectionFilter,
  collectionFilterMap,
  collectionFilterMapDialog,
  collectionSearcher,
  resources,
  sorter,
  contact,
  orderCart
})

export default rootReducer;
