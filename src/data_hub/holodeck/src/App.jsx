import React, { Component } from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import ReactGA from "react-ga";
import createBrowserHistory from "history/createBrowserHistory";

import rootReducer from './reducers/rootReducer';
import CatalogContainer from './containers/CatalogContainer';
import NotFound from './components/NotFound';

const store = createStore(rootReducer, applyMiddleware(thunk));

class App extends Component {

  ReactGA.initialize("UA-491601-16");

  ReactGA.pageview(window.location.pathname);

  render() {

    return (
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route path='/' exact component={CatalogContainer} />
            <Route path='/collection/:collectionId' exact component={CatalogContainer} />
            <Route path='/catalog/:filters' exact component={CatalogContainer} />
            <Route path='*' component={NotFound} />
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
