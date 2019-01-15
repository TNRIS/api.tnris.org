import React from 'react';

export default class TnrisDownloadMapNote extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        noteHover: false
      };
  }

  render() {
    const noteContent = this.state.noteHover ? (
      <p>
        Every dataset (excluding External Link availability) is available for order directly from TNRIS. Click the Order tab if the quantity of data needed is too large to download.
        <br />
        Every downloadable dataset is publically available via an AWS S3 bucket and can be accessed using the AWS CLI for bulk and programmatic downloads. Click the Contact tab to inquire with TNRIS about details related to S3 bulk access.
      </p>
    ) : (
      <i className="material-icons">toys</i>
    );

    return (
      <div id='tnris-download-note' className='mdc-typography--caption' onMouseEnter={() => {this.setState({noteHover:true})}} onMouseLeave={() => {this.setState({noteHover:false})}}>
        {noteContent}
      </div>
    );
  }
}
