import React from 'react';

export default class CatalogCard extends React.Component {

  render() {
    // const image = 'url("https://ih0.redbubble.net/image.395829383.0893/pp,550x550.jpg")'
    return (
      <div className='catalog-card mdc-card mdc-card__primary-action'>
        <div
          className='catalog-card__media mdc-card__media mdc-card__media--16-9'
          style={{backgroundImage: `url(${this.props.collection.thumbnail_image})`}}>
          {/* style={{backgroundImage: image}}> */}
        </div>
        <p className='catalog-card__headline mdc-typography--body1'>{this.props.collection.name}</p>
        <p className='catalog-card__body mdc-typography__body2'>{this.props.collection.short_description}</p>
        <div className='catalog-card__actions mdc-card__actions'>
          <div className='mdc-card__action-buttons'>
            <button className='mdc-button mdc-card__action mdc-card__action--button'>Action 1</button>
            <button className='mdc-button mdc-card__action mdc-card__action--button'>Action 2</button>
          </div>
        </div>
      </div>
    );
  }
}
