export fetchCollections = () => {
  return dispatch => {
      let headers = {"Content-Type": "application/json"};
      return fetch("/api/v1/collections/", {headers, })
        .then(res => res.json())
        .then(collections => {
          return dispatch({
            type: 'FETCH_COLLECTIONS',
            collections
          })
        })
  }
}
