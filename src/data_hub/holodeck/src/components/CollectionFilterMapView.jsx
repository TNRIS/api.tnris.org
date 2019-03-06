import React from 'react';

import CollectionFilterMapContainer from '../containers/CollectionFilterMapContainer';

export default class CollectionFilterMapView extends React.Component {
    render() {
      return (
        <div className="filter-map-view">
          <h2 className="mdc-top-app-bar__title">
            Filter by Geography
          </h2>
          <CollectionFilterMapContainer />
        </div>
      );
    }
}
