import React from 'react';

export default class Ls4Links extends React.Component {
  constructor (props) {
    super(props);
    this.state = {
      indexCopied: false,
      mosaicCopied: false,
      framesCopied: false
    }
    this.copyUrl = this.copyUrl.bind(this);
  }

  copyUrl (inputId, stateKey) {
    const nextState = {
      indexCopied: false,
      mosaicCopied: false,
      framesCopied: false
    };
    const input = document.getElementById(inputId);
    input.select();
    document.execCommand("copy");
    nextState[stateKey] = true;
    this.setState(nextState);
  }

  render() {
    let scanLinks;
    const scans = this.props.scans ? JSON.parse("[" + this.props.scans + "]") : [];
    if (scans.length > 0) {
      scanLinks = (
        <div className="ls4-scans">
          <p className="mdc-typography--body2">
            This Historic Imagery dataset has scanned indexes (.tif format) available for download.
          </p>
          <ul className="mdc-list">
            {scans.map((scan, index) => {
              const odd = index % 2 === 1 ? "mdc-list-item odd" : "mdc-list-item even";
              return (
                <li key={index} className={odd}>
                  <div>Sheet #{scan.sheet}</div>
                  <div>{scan.size}</div>
                  <div>
                    <a href={scan.link} target="_blank">Download</a>
                  </div>
                </li>
              )}
            )}
          </ul>
        </div>
      );
    }

    const indexCopied = this.state.indexCopied ? "Copied!" : "Copy URL";
    const indexUrl = this.props.index && this.props.index !== "" ? (
      <div className="ls4-links">
        <p className="mdc-typography--body2">
          <strong>Index WMS Service</strong>
        </p>
        <input type="text" id="ls4-links-index-input"
               className="mdc-text-field__input"
               value={this.props.index} readOnly/>
        <div className="ls4-links-buttons">
          <button className="mdc-button mdc-button--raised" onClick={() => this.copyUrl('ls4-links-index-input', 'indexCopied')}>
            <i className="material-icons">file_copy</i>{indexCopied}
          </button>
        </div>
      </div>
    ) : "";

    const mosaicCopied = this.state.mosaicCopied ? "Copied!" : "Copy URL";
    const mosaicUrl = this.props.mosaic && this.props.mosaic !== "" ? (
      <div className="ls4-links">
        <p className="mdc-typography--body2">
          <strong>Mosaic WMS Service</strong>
          <br />
          <span className='mdc-typography--caption'>
            (Comprised only of the currently scanned dataset frames for this dataset)
          </span>
        </p>
        <input type="text" id="ls4-links-mosaic-input"
               className="mdc-text-field__input"
               value={this.props.mosaic} readOnly/>
             <div className="ls4-links-buttons">
          <button className="mdc-button mdc-button--raised" onClick={() => this.copyUrl('ls4-links-mosaic-input', 'mosaicCopied')}>
            <i className="material-icons">file_copy</i>{mosaicCopied}
          </button>
        </div>
      </div>
    ) : "";

    const framesCopied = this.state.framesCopied ? "Copied!" : "Copy URL";
    const framesUrl = this.props.frames && this.props.frames !== "" ? (
      <div className="ls4-links">
        <p className="mdc-typography--body2">
          <strong>Individual Frames WMS Service</strong>
          <br />
          <span className='mdc-typography--caption'>
            (Comprised only of the currently scanned dataset frames for this dataset)
          </span>
        </p>
        <input type="text" id="ls4-links-frames-input"
               className="mdc-text-field__input"
               value={this.props.frames} readOnly/>
             <div className="ls4-links-buttons">
          <button className="mdc-button mdc-button--raised" onClick={() => this.copyUrl('ls4-links-frames-input', 'framesCopied')}>
            <i className="material-icons">file_copy</i>{framesCopied}
          </button>
        </div>
      </div>
    ) : "";

    return (
      <div className="template-content-div ls4-links-container">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Download and Service Links
        </div>
        {scanLinks}
        {indexUrl}
        {mosaicUrl}
        {framesUrl}
      </div>
    )
  }
}
