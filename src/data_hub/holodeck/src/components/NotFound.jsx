import React, { Component } from 'react';
import image404 from '../images/404.jpg';

class NotFound extends Component {
  render() {
    return (
      <div className="notfound-component">
          <div className="notfound">
            <img
              src={image404}
              alt="Lieutenant Commander Data"
              className="notfound-image"
              />
            <h2>ERROR 404: Not Found</h2>
            <p>The page you're looking for does not exist.</p>
          </div>
      </div>
    )
  }
}

export default NotFound
