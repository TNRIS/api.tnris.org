import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionSearcher from './collectionSearcherReducer';
import collectionTimeslider from './collectionTimesliderReducer';
import mapDialog from './mapDialogReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';
import contact from './contactReducer';
import orderCart from './orderCartReducer';
import urlTracker from './urlTrackerReducer';

const rootReducer = combineReducers({
  collections,
  collectionDialog,
  collectionFilter,
  collectionSearcher,
  collectionTimeslider,
  mapDialog,
  resources,
  sorter,
  contact,
  orderCart,
  urlTracker
})

export default rootReducer;
