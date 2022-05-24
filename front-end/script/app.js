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
const listenToSocket = function () {
  socket.on("connect", function () {
    console.log("verbonden met socket");
  });
  socket.on("B2F_temperatuur",function (json) {
    const temp = `${json.temperatuur.waarde}°C`
    console.log(
      `huidige temperatuur : ${temp}`
    );
  })
}
// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********   
const init = function () {
  console.info("DOM geladen");
  listenToSocket()
} 
document.addEventListener("DOMContentLoaded", init);
// #endregion