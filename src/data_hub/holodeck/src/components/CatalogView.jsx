import React from 'react';
import { Redirect } from 'react-router';

import CatalogCardContainer from '../containers/CatalogCardContainer';

export default class CatalogView extends React.Component {

  render() {
    return (
      <div className="catalog-view">
        <ul className='catalog-list mdc-image-list mdc-image-list--with-text-protection'>
          {this.props.visibleCollections.map(collectionId =>
            <CatalogCardContainer
              collection={this.props.collections[collectionId]}
              key={collectionId}
              match={this.props.match}
              history={this.props.history} />
          )}
        </ul>
      </div>
    );
  }
}
