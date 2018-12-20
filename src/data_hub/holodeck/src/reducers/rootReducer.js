import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionFilterMap from './collectionFilterMapReducer';
import collectionFilterMapDialog from './collectionFilterMapDialogReducer';
import collectionSearcher from './collectionSearcherReducer';
import collectionSorter from './collectionSorterReducer';
import collectionTimeslider from './collectionTimesliderReducer';
import resources from './resourceReducer';
import contact from './contactReducer';
import orderCart from './orderCartReducer';
import urlTracker from './urlTrackerReducer';
import colorTheme from './colorThemeReducer';

const rootReducer = combineReducers({
  collections,
  collectionDialog,
  collectionFilter,
  collectionFilterMap,
  collectionFilterMapDialog,
  collectionSearcher,
  collectionSorter,
  collectionTimeslider,
  resources,
  contact,
  orderCart,
  urlTracker,
  colorTheme
})

export default rootReducer;
