import React from 'react';

export default class TnrisDownloadTemplate extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {
    return (
      <div className='tnris-download-template mdc-layout-grid'>
        <div className='mdc-layout-grid__inner'>
          <h4 className='mdc-typography--headline4 mdc-layout-grid__cell mdc-layout-grid__cell--span-12'>
            {this.props.collection.name}
          </h4>
        </div>
          <img
            src={this.props.collection.overview_image}
            alt='Dataset Overview Image'
            className='collection-dialog__image mdc-layout-grid__cell--span-12'/>
        <div className='mdc-layout-grid__inner'>
          <p className='mdc-typography__body2 mdc-layout-grid__cell--span-12'>
            {this.props.collection.description}
          </p>
        </div>
      </div>
    );
  }
}
