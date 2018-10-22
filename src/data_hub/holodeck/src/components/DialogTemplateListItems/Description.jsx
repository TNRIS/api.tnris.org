import React from 'react';

export default class Description extends React.Component {

  render() {
    return (
      <div className="template-content-div">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Description
        </div>
        <p>
          {this.props.collection.description}
        </p>
      </div>
    )
  }
}
