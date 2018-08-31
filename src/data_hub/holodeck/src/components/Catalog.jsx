import React from 'react';

export default class Catalog extends React.Component {

  componentDidMount() {
    this.props.fetchCollections();
    this.props.fetchResources();
  }

  render() {
    console.log(this.props);
    const { error, loading } = this.props;
    const loadingMessage = <div>Loading...</div>;

    if (error) {
      return <div>Error! {error.message}</div>;
    }

    if (loading) {
      return loadingMessage;
    }

    return (
      <div className='catalog-component'>
        <h1 className='mdc-typography--headline1'>Welcome to the holodeck!</h1>
        <h2
          className='mdc-typography--headline2'>i'm the catalog</h2>
          <div className='mdc-layout-grid'>
          <ul className='catalog-list mdc-layout-grid__inner'>
            {this.props.collections.result ? this.props.collections.result.map(collectionId =>
              <li
                className='mdc-layout-grid__cell'
                key={collectionId}><h5>{this.props.collections.entities.collectionsById[collectionId]['name']}</h5>
                <ul>
                  {Object.entries(this.props.collections.entities.collectionsById[collectionId])
                    .map(([key, value], i) => <li key={i}><strong>{key}: </strong>{value}</li>)}
                </ul>
              </li>
            ) : 'loadingMessage'}
          </ul>
        </div>
      </div>
    );
  }
}
