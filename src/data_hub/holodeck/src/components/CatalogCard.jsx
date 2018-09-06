import React from 'react';

export default class CatalogCard extends React.Component {

  constructor(props) {
    super(props)
    this.cardClicked = this.cardClicked.bind(this)
  }

  cardClicked() {
    console.log(this.props.collection.name);
    this.props.openCollectionDialog();
    this.props.selectCollection(this.props.collection.collection_id)
    console.log(this.props);
  }

  render() {
    return (
      <div className='catalog-card-component mdc-card mdc-card__primary-action'
           onClick={this.cardClicked}>
        <div
          className='catalog-card__media mdc-card__media mdc-card__media--16-9'
          style={{backgroundImage: `url(${this.props.collection.thumbnail_image})`}}>
        </div>
        <p className='catalog-card__headline mdc-typography--body1'>{this.props.collection.name}</p>
        <p className='catalog-card__body mdc-typography__body2'>{this.props.collection.short_description}</p>
        <div className='catalog-card__actions mdc-card__actions'>
          <div className='mdc-card__action-buttons'>
            <button className='mdc-button mdc-card__action mdc-card__action--button'
                    onClick={e => e.stopPropagation()}>
                    Action 1
            </button>
            <button className='mdc-button mdc-card__action mdc-card__action--button'
                    onClick={e => e.stopPropagation()}>
                    Action 2
            </button>
          </div>
        </div>
      </div>
    );
  }
}
