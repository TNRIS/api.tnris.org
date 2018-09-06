import React from 'react';

export default class DialogContent extends React.Component {
  render() {
    return (
      <div className='collection-card-component mdc-layout-grid'>
        <div className='mdc-layout-grid__inner'>
          <h4 className='mdc-typography--headline4 mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
            {this.props.collection.name}
          </h4>
        </div>
          <img src={this.props.collection.overview_image} alt=''
               className='collection-card__image mdc-layout-grid__cell--span-12'/>
        <div className='mdc-layout-grid__inner'>
          <p className='mdc-typography__body2 mdc-layout-grid__cell--span-12'>
            {this.props.collection.description}
          </p>
        </div>
      </div>
    );
  }
}
