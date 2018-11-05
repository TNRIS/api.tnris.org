import React from 'react';
import {MDCTopAppBar} from '@material/top-app-bar/index';

import TnrisOutsideEntityTemplateDetails from './TnrisOutsideEntityTemplateDetails';

export default class TnrisOutsideEntityTemplate extends React.Component {
  constructor(props) {
      super(props);
      this.state = {
        view:'details'
      };
  }

  componentDidMount() {
    this.topAppBarElement = document.querySelector('.mdc-top-app-bar');
    this.topAppBar = new MDCTopAppBar(this.topAppBarElement);
  }

  render() {

    console.log(this.props);

    return (
      <div className='tnris-download-template' tabIndex='1'>
        <header className="mdc-top-app-bar">
          <div className="mdc-top-app-bar__row">
            <section className="mdc-top-app-bar__section mdc-top-app-bar__section--align-start">
              <span className="mdc-top-app-bar__title">{this.props.collection.name}</span>
            </section>
          </div>
        </header>

        <TnrisOutsideEntityTemplateDetails collection={this.props.collection} />

      </div>
    );
  }
}
