import { combineReducers } from 'redux';

import products from './productReducer';
import collections from './collectionReducer';

const rootReducer = combineReducers({
  collections,
  products
})

export default rootReducer;
