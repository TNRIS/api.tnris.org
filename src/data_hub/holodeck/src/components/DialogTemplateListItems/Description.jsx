import React from 'react';

export default class Description extends React.Component {

  render() {
    return (
      <li className='mdc-image-list__item'>
        <div className='mdc-typography--headline4'>
          DESCRIPTION
        </div>
        <div>
          {this.props.collection.description}
        </div>
      </li>
    )
  }
}
