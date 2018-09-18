import React from 'react';

export default class TnrisDownloadTemplate extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {
    return (
      <div className='tnris-download-template mdc-layout-grid' tabIndex='1'>
        <div className='mdc-layout-grid__inner'>
          <h4 className='mdc-typography--headline4 mdc-layout-grid__cell'>
            {this.props.collection.name}
          </h4>
        </div>
        <div className='mdc-layout-grid__inner'>
          <img
            src={this.props.collection.overview_image}
            alt='Dataset Overview'
            className='collection-dialog__image mdc-layout-grid__cell'/>
        </div>
        <div className='mdc-layout-grid__inner'>
          <p className='mdc-typography__body2 mdc-layout-grid__cell'>
            {this.props.collection.description}
          </p>
        </div>
      </div>
    );
  }
}
