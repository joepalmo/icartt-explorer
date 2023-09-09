import React from 'react';
import Map from './Map';

function App() {
  return (
    <div>
      <Map />
      <form action="upload" method="post" encType="multipart/form-data">
        <input type="file" name="file"></input>
        <br></br>
        <input type="submit" value="Upload"></input>
      </form>
    </div>
  );
}

export default App;