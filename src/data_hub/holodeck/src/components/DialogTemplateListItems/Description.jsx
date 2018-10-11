import React from 'react';

export default class Description extends React.Component {

  render() {
    return (
      <li className='mdc-image-list__item'>
        <div className='mdc-typography--headline5'>
          Description
        </div>
        <p>
          {this.props.collection.description}
        </p>
      </li>
    )
  }
}
