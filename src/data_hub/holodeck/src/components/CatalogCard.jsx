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
    const cardClass = 'catalog-card-component mdc-image-list__item ' + this.props.collection.template;

    return (
      <li className={cardClass} onClick={this.cardClicked}>
        <div className="mdc-image-list__image-aspect-container">
            <img className="mdc-image-list__image" src={this.props.collection.thumbnail_image} alt="Dataset Thumbnail" />
        </div>
        <div className="mdc-image-list__supporting">
          <span className="mdc-image-list__label">{this.props.collection.name}</span>
        </div>
      </li>
    );
  }
}
