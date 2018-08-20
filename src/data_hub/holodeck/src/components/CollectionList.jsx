import React from "react";
import { connect } from "react-redux";

import { collectionActions } from "../actions";

class CollectionList extends React.Component {
  componentDidMount() {
    this.props.fetchCollections();
  }

  render() {
    console.log(this.props);
    const { error, loading, collections } = this.props;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return <div>Loading...</div>;
    }

    return (
      <ul>
        {collections.map(collection =>
          <li key={collection.collection_id}>{collection.name}</li>
        )}
      </ul>
    );
  }
}

const mapStateToProps = state => ({
  collections: state.collections.items,
  loading: state.collections.loading,
  error: state.collections.error
});

const mapDispatchToProps = dispatch => ({
  fetchCollections: () => {
    dispatch(collectionActions.fetchCollections());
  }
})

export default connect(mapStateToProps, mapDispatchToProps)(CollectionList);
