import React from 'react';

export default class Drawer extends React.Component {

  render() {
    return (
      <div className="drawer-component">
        <aside className="mdc-drawer mdc-drawer--modal">
          <div className="mdc-drawer__content">
            <nav className="mdc-list">
              <a className="mdc-list-item mdc-list-item--activated" href="#" aria-selected="true">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">inbox</i>Inbox
              </a>
              <a className="mdc-list-item" href="#">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">send</i>Outgoing
              </a>
              <a className="mdc-list-item" href="#">
                <i className="material-icons mdc-list-item__graphic" aria-hidden="true">drafts</i>Drafts
              </a>
            </nav>
          </div>
        </aside>
        <div className="mdc-drawer-scrim"></div>
      </div>
    );
  }
}
