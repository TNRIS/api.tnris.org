import React from 'react';

export default class Services extends React.Component {

  render() {
    return (
      <li className='mdc-image-list__item'>
        <div className='mdc-typography--headline4'>
          SERVICES
        </div>
        <ul className="mdc-list">
          <li className="mdc-list-item">WMS Service: <a href={this.props.collection.wms_link}>{this.props.collection.wms_link}</a></li>
        </ul>
      </li>
    )
  }
}
