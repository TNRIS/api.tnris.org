import { combineReducers } from "redux";

import collections from "./collectionReducer";
import resources from "./resourceReducer"

const rootReducer = combineReducers({
  collections,
  resources,
})

export default rootReducer;
