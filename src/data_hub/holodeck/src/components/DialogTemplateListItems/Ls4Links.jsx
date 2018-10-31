import React from 'react';

export default class Ls4Links extends React.Component {
  render() {
    // const source = this.props.collection.source ? (
    //   <li className="mdc-list-item">
    //     <strong>Source:</strong>{this.props.collection.source}
    //   </li>
    // ) : "";
    //
    // const agency = this.props.collection.agency_name ? (
    //   <li className="mdc-list-item">
    //     <strong>Agency Name:</strong>{this.props.collection.agency_name} ({this.props.collection.agency_abbreviation})
    //   </li>
    // ) : "";
    //
    // const agency_site = this.props.collection.agency_website ? (
    //   <li className="mdc-list-item">
    //     <strong>Agency Website:</strong>{this.props.collection.agency_website}
    //   </li>
    // ) : "";


    return (
      <div className="template-content-div ls4-links">
        <div className='mdc-typography--headline5 template-content-div-header'>
          Download and Service Links
        </div>
        <ul className="mdc-list">
          LIST
        </ul>
      </div>
    )
  }
}
