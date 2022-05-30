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
const showHistory = function(json){
  console.log(json);
  let htmldata = document.querySelector(".js-table");
  let htmlHeader = ``;
  let htmlUitvoer = ``;
  htmlHeader = `<th>idmeting</th>
                <th>DeviceID</th>
                <th>Waarde</th>
                <th>Tijdstip</th>`
  htmlUitvoer += htmlHeader
  for(let obj of json){
    htmlUitvoer +=`
    <tr>
            <td>${obj.idMeting}</td>
            <td>${obj.DeviceID}</td>
            <td>${obj.Waarde}</td>
            <td>${obj.Tijdstip}</td>
    </tr>`;
  }
  htmldata.innerHTML = htmlUitvoer;
}
// #endregion 

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********
const getHistoriek = function () {
   handleData(`http://192.168.168.169:5000/api/v1/historiek/`, showHistory);
};
// #endregion 

// #region ***  Event Listeners - listenTo___            ***********       
const listenToSocket = function () {
  if(htmlIndex){
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
  console.log("htmlHistory?", htmlHistory)
  if(htmlHistory){
    socket.on("connect", function () {
    console.log("verbonden met socket");
  });
console.log("listen B2F_history")
    socket.on("B2F_history", (data) => {
      //console.log("B2F_history", data)
      showHistory(data)
    })
  }
  
}

// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********   
const init = function () {
  console.info("DOM geladen");
  htmlIndex = document.querySelector(".js-index");
  htmlHistory = document.querySelector(".js-history");
  listenToSocket()
}
document.addEventListener("DOMContentLoaded", init);
// #endregion