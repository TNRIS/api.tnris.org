import React, { Component } from 'react';
import { Route, Switch, BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import thunk from 'redux-thunk';
import ReactGA from 'react-ga';

import rootReducer from './reducers/rootReducer';
import CatalogContainer from './containers/CatalogContainer';
import NotFound from './components/NotFound';

const store = createStore(rootReducer, applyMiddleware(thunk));

let path = window.location.pathname;

// const checkPath = (p) => {
//   if (p != window.location.pathname) {
//     console.log(window.location.pathname);
//     p = window.location.pathname;
//     ReactGA.pageview(p);
//   };
// }

class App extends Component {

  render() {

    // console.log(window.location);
    ReactGA.initialize('UA-491601-16');

    return (
      <Provider store={store}>
        <BrowserRouter>
          <Switch>
            <Route path='/collection/:collectionId' exact component={CatalogContainer} />
            <Route path='/catalog/:filters' exact component={CatalogContainer} />
            <Route path='/' exact component={CatalogContainer} />
            <Route path='*' component={NotFound} />
            {ReactGA.pageview(path)}
            {
              history.listen(location => ReactGA.pageview(window.location.pathname));
            }
          </Switch>
        </BrowserRouter>
      </Provider>
    );
  }
}

export default App;
