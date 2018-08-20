import React, { Component } from 'react';
import {connect} from 'react-redux';

import {collections} from '../actions';


class Catalog extends Component {
  componentDidMount() {
    this.props.fetchCollections();
    console.log(this.props);
  }

  render() {
    return (
      <div>
        <h2>Welcome to the holodeck catalog!</h2>
        <hr />

        <h3>Collections</h3>
        <table>
          <tbody>
            {this.props.collections.map(collection => (
              <tr>
                <td>{collection.name}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    )
  }
}


const mapStateToProps = state => {
  return {
    collections: state.collections,
  }
}

const mapDispatchToProps = dispatch => {
  return {
    fetchCollections: () => {
      dispatch(collections.fetchCollections());
    }
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(Catalog);
