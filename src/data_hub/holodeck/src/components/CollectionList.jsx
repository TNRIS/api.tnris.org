import React from 'react';

class CollectionList extends React.Component {

  render() {
    const collections = this.props.collections;

    return (
      <div className='container'>
        <div className='row'>
          <h3 className='col text-left'>Collections</h3>
        </div>
        <ul className='list-group'>
          {collections.result ? collections.result.map(collectionId =>
            <li
              className='list-group-item'
              key={collectionId}><h5>{collections.entities.collectionsById[collectionId]['name']}</h5>
              <ul>
                {Object.entries(collections.entities.collectionsById[collectionId])
                  .map(([key, value], i) => <li key={i}><strong>{key}: </strong>{value}</li>)}
              </ul>
            </li>
          ) : 'loadingMessage'}
        </ul>
      </div>
    );
  }
}

export default CollectionList;
