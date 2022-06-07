"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
// #region ***  DOM references   ***********
let htmlIndex,htmlHistory;
let htmlCards;
let htmlSingleCard;
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
const showFood = function (json) {
  console.log(json);
  
  let htmlUitvoer = ``;

  for(let obj of json){
    console.log(obj.houdbaarheidsdatum);
    htmlUitvoer += `<div class="c-card js-card"  data-id="${obj.idproduct}">
              <div class="c-card__image-container ">
                <img src="https://fakeimg.pl/400x300/f1db26/000/" alt="" class="c-card__img">
                <h3 class="c-card--name">${obj.Naam}</h3>
              </div>
                <div class="c-card__content">
                <p><span class="c-card--date">${obj.houdbaarheidsdatum}</span> <span class="material-icons u-icons">notifications</span><span class="material-icons u-icons">edit</span><span class="material-icons u-icons">delete</span></p>
                </div>
            </div>`;
  }
  htmlCards.innerHTML = htmlUitvoer;
  listenToUI();
}
// #endregion 

// #region ***  Callback-No Visualisation - callback___  ***********
// #endregion

// #region ***  Data Access - get___                     ***********

// #endregion 

// #region ***  Event Listeners - listenTo___            ***********     

const listenToUI = function(){
  if(htmlIndex){
    
    htmlSingleCard = document.querySelectorAll(".js-card");
    for(let obj of htmlSingleCard){
      console.log("kiekeboe");
      obj.addEventListener("click",function(){
        console.log(obj.getAttribute("data-id"));
      })
    }
  }
}
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
  socket.on("B2F_connected",function(json){
    showFood(json);
  });
  }

  if(htmlHistory){
    socket.on("connect", function () {
    console.log("verbonden met socket");
  });
    console.log("listen B2F_history")
    socket.on("B2F_history", (data) => {
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
  htmlCards = document.querySelector(".js-cards");
  listenToSocket();
}
document.addEventListener("DOMContentLoaded", init);
// #endregion