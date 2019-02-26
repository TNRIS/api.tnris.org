import React from 'react';

export default class SourceCitation extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      copied: false
    }

    this.copySourceCitation = this.copySourceCitation.bind(this);
  }

  copySourceCitation () {
    const input = document.getElementById("citation");
    input.select();
    document.execCommand("copy");
    this.setState({copied: true});
  }

  render() {

    const copied = this.state.copied ? "Copied!" : "Copy";
    const currentDate = new Date();
    const sourceCitationText = `${this.props.collection.source_name} (${this.props.collection.source_abbreviation}). ${this.props.collection.name}, ${this.props.collection.acquisition_date}. Web. ${currentDate}`

    return (
      <div className="template-content-div">
        <div className="citation-container">
          <div className="mdc-typography--headline5">
            Source Citation
          </div>
          <div className="citation-style">
            Copy the text below to properly cite this dataset.
          </div>
          <textarea id="citation"
            className="mdc-text-field__input copy-citation"
            rows="6"
            columns="20"
            value={sourceCitationText}
            readOnly>
          </textarea>
          <div className="services-link-details">
            <div className="service-link-details-buttons">
              <button className="mdc-button mdc-button--raised" onClick={this.copySourceCitation}>
                <i className="material-icons">file_copy</i>{copied}
              </button>
            </div>
          </div>
        </div>
      </div>
    )
  }
}
