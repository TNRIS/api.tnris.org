import React from 'react';

export default class CatalogCard extends React.Component {

  constructor(props) {
    super(props)
    this.cardClicked = this.cardClicked.bind(this)
  }

  cardClicked() {
    this.props.openCollectionDialog();
    this.props.selectCollection(this.props.collection.collection_id);
    if (this.props.collection.template === 'tnris-download') {
      this.props.fetchCollectionResources(this.props.collection.collection_id);
    }
  }

  render() {
    const cardClass = 'catalog-card-component mdc-image-list__item ' + this.props.collection.template;
    const collectionYear = this.props.collection.acquisition_date && this.props.collection.template === 'historical-aerial' ? this.props.collection.acquisition_date.substring(0, 4) + ' ' : '';
    let collectionCounty = '';
    if (this.props.collection.template === 'historical-aerial') {
      collectionCounty = this.props.collection.counties && !this.props.collection.counties.includes(",") ? this.props.collection.counties + ' ' : 'Multi-County ';
    }

    return (
      <li className={cardClass} onClick={this.cardClicked}>
        <div className="mdc-image-list__image-aspect-container">
            <img className="mdc-image-list__image" src={this.props.collection.thumbnail_image} alt="Dataset Thumbnail" />
        </div>
        <div className="mdc-image-list__supporting">
          <span className="mdc-image-list__label">{collectionYear}{collectionCounty}{this.props.collection.name}</span>
        </div>
      </li>
    );
  }
}
