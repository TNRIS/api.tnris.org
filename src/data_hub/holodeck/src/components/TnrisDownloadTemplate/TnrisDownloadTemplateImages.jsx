import React from 'react';

export default class TnrisDownloadTemplateImages extends React.Component {
  constructor(props) {
      super(props);
      console.log(this.props);
  }

  render() {

    return (

    <div className="tnris-download-template-images">

      <button className="mdc-button mdc-button-left mdc-button--raised"><i className="material-icons">chevron_left</i></button>

      <button className="mdc-button mdc-button-right mdc-button--raised"><i className="material-icons">chevron_right</i></button>

    </div>

    );
  }
}
