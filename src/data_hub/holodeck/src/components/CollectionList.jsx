import React from 'react';
import { connect } from 'react-redux';

import { collectionActions, resourceActions } from '../actions';

class CollectionList extends React.Component {

  componentDidMount() {
    this.props.fetchCollections();
    // this.props.fetchResources();
  }

  render() {
    console.log(this.props);
    const { error, loading, collections } = this.props;
    const loadingMessage = <div>Loading...</div>;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

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
          ) : loadingMessage}
        </ul>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  collections: state.collections.items,
  resources: state.resources.items,
  loading: state.collections.loading,
  error: state.collections.error
});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  },
  fetchResources: () => {
    dispatch(resourceActions.fetchResources());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionList);
