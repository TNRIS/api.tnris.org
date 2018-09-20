import React from 'react';

export default class CatalogCard extends React.Component {

  constructor(props) {
    super(props)
    this.cardClicked = this.cardClicked.bind(this)
  }

  cardClicked() {
    this.props.openCollectionDialog();
    this.props.selectCollection(this.props.collection.collection_id)
    console.log(this.props);
  }

  render() {
    const cardClass = 'catalog-card-component mdc-card mdc-card__primary-action ' + this.props.collection.template;

    return (
      <div className={cardClass}
           onClick={this.cardClicked}>
        <div
          className='catalog-card__media mdc-card__media mdc-card__media--square'
          style={{backgroundImage: `url(${this.props.collection.thumbnail_image})`}}
          alt="Dataset Thumbnail">
          <p className='catalog-card__headline mdc-typography--body1'>{this.props.collection.name}</p>
        </div>

      </div>
    );
  }
}
