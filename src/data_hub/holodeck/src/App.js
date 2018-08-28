import React, { Component } from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';

import rootReducer from './reducers/rootReducer';

import CatalogContainer from './containers/CatalogContainer';
import MapContainer from './containers/MapContainer';

const store = createStore(rootReducer, applyMiddleware(thunk));

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route exact path='/' component={CatalogContainer} />
            <Route path='/map'component={MapContainer} />
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
