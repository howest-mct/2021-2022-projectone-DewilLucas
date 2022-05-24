"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
// #region ***  DOM references   ***********
// #endregion 
// #region ***  Callback-Visualisation - show___         ***********      
// #endregion 

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
// #endregion 

// #region ***  Event Listeners - listenTo___            ***********       
// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********    
document.addEventListener("DOMContentLoaded", function () {
  console.info("DOM geladen");
});
// #endregion