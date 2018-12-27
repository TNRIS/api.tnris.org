import { combineReducers } from "redux";

import collections from './collectionReducer';
import collectionDialog from './collectionDialogReducer';
import collectionFilter from './collectionFilterReducer';
import collectionFilterMap from './collectionFilterMapReducer';
import collectionFilterMapDialog from './collectionFilterMapDialogReducer';
import collectionSearcher from './collectionSearcherReducer';
import collectionTimeslider from './collectionTimesliderReducer';
import colorTheme from './colorThemeReducer';
import contact from './contactReducer';
import orderCart from './orderCartReducer';
import resources from './resourceReducer';
import sorter from './sortReducer';
import toolDrawer from './toolDrawerReducer';
import urlTracker from './urlTrackerReducer';


const rootReducer = combineReducers({
  collections,
  collectionDialog,
  collectionFilter,
  collectionFilterMap,
  collectionFilterMapDialog,
  collectionSearcher,
  collectionTimeslider,
  colorTheme,
  contact,
  orderCart,
  resources,
  sorter,
  toolDrawer,
  urlTracker,
})

export default rootReducer;
