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

    console.log(this.props.collection);

    const sourceCitationText = `${this.props.collection.name}, ${this.props.collection.source_name} (${this.props.collection.source_abbreviation}),`

    return (
      <div className="template-content-div">
        <div className="mdc-typography--headline5">
          Source Citation
        </div>
        <div className="source-citation">
          Copy the text below to properly cite this dataset.
        </div>
        <div className="mdc-text-field mdc-text-field--textarea">
         <textarea id="citation"
           className="mdc-text-field__input styled-input citation-style styled-input"
           rows="5"
           columns="12"
           value={sourceCitationText}
           readOnly>
         </textarea>
        </div>
        <div className="service-link-details-buttons">
          <button className="mdc-button mdc-button--raised" onClick={this.copySourceCitation}>
            <i className="material-icons">file_copy</i>{copied}
          </button>
        </div>
      </div>
    )
  }
}
