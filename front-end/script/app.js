"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
// #region ***  DOM references   ***********
let htmlIndex,htmlHistory;
let htmlCards;
let htmlSingleCard;
let htmlImgContainer;
let htmlEdit;
let htmlAdd;
let htmlOff;
let htmlEditPro;
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
  htmlUitvoer += htmlHeader;
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
const showEdit = function (json) {
  let htmlName = document.querySelector(".js-name");
  let htmlDate = document.querySelector(".js-datum");
  let htmlaantal = document.querySelector(".js-aantall");
  htmlName.value= json.Naam;
  htmlDate.value = json.HoudbaarheidsDatum;
  htmlaantal.value = json.Aantal;
}
const showFood = function (json) {
  console.log(json);
  
  let htmlUitvoer = ``;

  for(let obj of json){
    htmlUitvoer += `<div class="c-card js-card">
              <div class="c-card__image-container js-img-card" data-id="${obj.idAanwezig}">
                <a href="edit_product.html?idaanwezig=${obj.idAanwezig}"><img src="https://fakeimg.pl/400x300/f1db26/000/" alt="${obj.Naam}" class="c-card__img">
                </a>
                <h3 class="c-card--name">${obj.Naam}</h3>
              </div>
                <div class="c-card__content">
                <p><span class="c-card--date">${obj.houdbaarheidsdatum}</span> <span class="material-icons u-icons">notifications</span><a href="edit_product.html?idaanwezig=${obj.idAanwezig}"><span class="material-icons u-icons js-edit"data-id="${obj.idAanwezig}">edit</span></a><span class="material-icons u-icons">delete</span></p>
                </div>
            </div>`;
  }
  htmlCards.innerHTML = htmlUitvoer;
  listenToUI();
}
// #endregion 

// #region ***  Callback-No Visualisation - callback___  ***********
const callbackWindow = function () {
  window.location.href = "history.html";
}
// #endregion

// #region ***  Data Access - get___                     ***********
const getrain = function(){
  let urlParams = new URLSearchParams(window.location.search);
  let get= urlParams.get("idaanwezig");
  socket.emit("F2B_edit",get);
  listenToSocket();
}
// #endregion 

// #region ***  Event Listeners - listenTo___            ***********     

const listenToUI = function(){
  if(htmlIndex){
    htmlImgContainer = document.querySelectorAll(".js-img-card")
    htmlEdit = document.querySelectorAll(".js-edit");
    for(let obj of htmlImgContainer){
      obj.addEventListener("click",function(){
        //console.log(obj.getAttribute("data-id"));
      });
    }
    for(let obj of htmlEdit){
      obj.addEventListener("click",function() {
        console.log(obj.getAttribute("data-id"));
      });
    }
  }
  
}
const listenToInput = function(){
    let barcode = document.querySelector(".js-barcode-offline");
    barcode.focus();
    if (barcode.value.length != 13) {
      barcode.addEventListener("input",function () {
      console.log("invoer");
      socket.emit("F2B_barcode",barcode.value);
    });
    }
}
const listenToAdd = function(){
    const htmlButton = document.querySelector(".js-add-button");
    htmlButton.addEventListener("click",function(){
      console.log("toevoegen van nieuwe product");
      const jsonObj = {
        naam : document.querySelector(".js-naam").value,
        datum : document.querySelector(".js-date").value,
        aantal : document.querySelector(".js-aantal").value,
        barcode : document.querySelector(".js-barcode").value
      };
      console.log(jsonObj);
      socket.emit("F2B_add-product",jsonObj);
    })
}
const listenToSocket = function () {
  if(htmlAdd){
    socket.on("B2F_alAanwezig",function (json) {
      console.log(json);
    })
  }
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
    console.log("listen B2F_history");
    socket.on("B2F_history", (data) => {
      showHistory(data);
    })
  }
  if(htmlEditPro){
    socket.on("B2F_edit",function(data){
      console.log(data);
      if(data == -1){
        console.log("niet gevonden");
      }
      else{
        console.log(data);
        showEdit(data);
      }
      const button = document.querySelector(".js-edit-button");
      button.addEventListener("click",function(){
        const jsonObj = {
          naam : document.querySelector(".js-name").value,
          datum : document.querySelector(".js-datum").value,
          aantal : document.querySelector(".js-aantall").value
        };
        socket.emit("F2B_edit_product",jsonObj);
      });
    });
  }
  
}

// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********   
const init = function () {
  console.info("DOM geladen");
  htmlIndex = document.querySelector(".js-index");
  htmlHistory = document.querySelector(".js-history");
  htmlCards = document.querySelector(".js-cards");
  htmlAdd = document.querySelector(".js-form");
  htmlOff = document.querySelector(".js-offline");
  htmlEditPro = document.querySelector(".js-edit_pro")
  if (htmlOff) {
    listenToInput();
  }
  if(htmlAdd){
    listenToAdd();
  }
  if(htmlEditPro){
    getrain();
  }
  listenToSocket();
}
document.addEventListener("DOMContentLoaded", init);
// #endregion