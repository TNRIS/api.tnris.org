import React from 'react';

export default class CatalogCard extends React.Component {

  constructor(props) {
    super(props)
    this.cardClicked = this.cardClicked.bind(this)
  }

  componentDidMount () {
    if (Object.keys(this.props.match.params).includes('collectionId') &&
        this.props.match.params.collectionId === this.props.collection.collection_id) {
      this.cardClicked();
    }
  }

  cardClicked() {
    // console.log(this.props);
    this.props.closeToolDrawer();
    this.props.openCollectionDialog();
    this.props.selectCollection(this.props.collection.collection_id);
    if (this.props.collection.template === 'tnris-download') {
      this.props.fetchCollectionResources(this.props.collection.collection_id);
    }
    this.props.setUrl('/collection/' + this.props.collection.collection_id, this.props.history);
  }

  render() {
    // const cardClass = 'catalog-card-component mdc-image-list__item ' + this.props.collection.template;
    const collectionYear = this.props.collection.acquisition_date && this.props.collection.template !== 'outside-entity' ? this.props.collection.acquisition_date.substring(0, 4) : '';

    return (
      <div
        className="catalog-card-component mdc-card mdc-card__primary-action"
        onClick={this.cardClicked}>
        <div
          className="mdc-card__media mdc-card__media--16-9"
          style={{backgroundImage: `url(${this.props.collection.thumbnail_image})`}}>
        </div>
        <p className='catalog-card__headline mdc-typography--headline6'>
          {this.props.collection.name}
        </p>
        <p className='catalog-card__year mdc-typography--subtitle1'>
          {collectionYear}
        </p>
        <p className='catalog-card__agency mdc-typography--body1'>
          {this.props.collection.agency_abbreviation}
        </p>
      </div>
    );
  }
}
