import { combineReducers } from "redux";

import areas from './areaReducer';
import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionFilterMap from './collectionFilterMapReducer';
import collectionFilterMapDialog from './collectionFilterMapDialogReducer';
import collectionSearcher from './collectionSearcherReducer';
import collectionTimeslider from './collectionTimesliderReducer';
import mapDialog from './mapDialogReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';
import contact from './contactReducer';
import orderCart from './orderCartReducer';
import urlTracker from './urlTrackerReducer';

const rootReducer = combineReducers({
  areas,
  collections,
  collectionDialog,
  collectionFilter,
  collectionFilterMap,
  collectionFilterMapDialog,
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
