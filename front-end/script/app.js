"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
// #region ***  DOM references   ***********
let htmlIndex,htmlHistory;
// #endregion 
// #region ***  Callback-Visualisation - show___         ***********      
const showTemp = function(temp) {
  let htmlTemp = document.querySelector(".js-temperatuur");
  let htmlUitvoer = `Huidige temperatuur: ${temp}`;
  htmlTemp.innerHTML = htmlUitvoer;
}
const showHistory = function(){

}
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
    let temp = `${json.temperatuur.waarde}°C`;
    console.log(
      `huidige temperatuur : ${temp}`
    );
    showTemp(temp);
  });
  
}
const listenToSocketHistory = function(){
  socket.on("connect", function () {
    console.log("verbonden met socket");
  });
  socket.on("B2F_history",function (json) {
    console.log("kiekeboe");
  });
}
// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********   
const init = function () {
  console.info("DOM geladen");
  htmlIndex = document.querySelector(".js-index");
  htmlIndex?listenToSocket():false;
  htmlHistory = document.querySelector(".js-history");
  htmlHistory?listenToSocketHistory():false;
}
document.addEventListener("DOMContentLoaded", init);
// #endregion