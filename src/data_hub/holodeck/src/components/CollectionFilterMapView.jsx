import React from 'react';

import CollectionFilterMapContainer from '../containers/CollectionFilterMapContainer';

export default class CollectionFilterMapView extends React.Component {
    render() {
      return (
        <div className="filter-map-view">
          <h2 className="mdc-top-app-bar__title">
            Filter by Geography
          </h2>
          <div className="instruction-header mdc-typography--body1">
            <p>
              Use the 'polygon tool' in the top left corner  of the map to identify a geographic area to filter datasets.
            </p>
            <p id="bottom-instruction">
              Single click to begin drawing, move cursor to draw a filter extent, single click to finish drawing.
            </p>
          </div>
          <CollectionFilterMapContainer />
        </div>
      );
    }
}
