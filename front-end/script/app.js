"use strict";
const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);
// #region ***  DOM references   ***********
let hamburger;
let htmlIndex, htmlHistory;
let htmlCards;
let htmlSingleCard;
let htmlImgContainer;
let htmlEdit;
let htmlAdd;
let htmlOff;
let htmlEditPro;
let htmlDelete;
let htmlDeletePage;
let htmlLogin;
let htmlloadlogin;
let htmlloadAccount;
let htmlAccount;
let htmlLoadUpdatedAccount;
let htmlCreateAccount;
let htmlloadDeleteAccount;
let htmlTest;
let chart;
let chartActive = false;
let datumVandaag = new Date();
let tdatum = datumVandaag.getDate();
let month = datumVandaag.getMonth() + 1;
if (month < 10) {//indien getal geen 2waarden heeft voeg er een nul aan toe
  month = '0' + month;
}
if (tdatum < 10) {
  tdatum = '0' + tdatum;
}
let year = datumVandaag.getUTCFullYear();
let minimumDatum = year + '-' + month + '-' + tdatum;
// #endregion 
// #region ***  Callback-Visualisation - show___         ***********      
const showTemp = function (temp) {
  let htmlTemp = document.querySelector(".js-temperatuur");
  let htmlUitvoer;
  if (htmlIndex) {
    htmlUitvoer = `Temperature: 
    ${temp}`;
  }
  else {
    htmlUitvoer = `Current temperature: 
    ${temp}`;
  }

  htmlTemp.innerHTML = htmlUitvoer;
};
const showChart = function (datax, dataY) {
  let options = {
    chart: {
      type: 'line',
      colors: '#FFC200',
      forecolor: '#FFC200',
      height: '400px'
    },
    title: {
      text: 'Temperatuur',
      style: {
        color: '#fff'
      }
    },
    dataLabels: {
      enabled: true,
    },
    colors: ['#FFC200', '#FFC200'],
    tooltip: {
      enabled: true,
      theme: 'dark'
    },
    series: [{
      name: 'temperatuur',
      data: dataY
    }],
    xaxis: {
      labels: {
        style: {
          colors: '#fff'
        }
      },
      categories: datax

    }, yaxis: {
      labels: {
        style: {
          colors: '#fff'
        }
      }
    },
    markers: {
      size: 5,
      colors: ["#FFC200"]
    },
    noData: {
      text: 'Loading...',
    }
  };
  chart = new ApexCharts(document.querySelector("#js-chart"), options);
  chart.render();
};
const showHistory = function (json) {
  let datax = [];
  let dataY = [];
  for (let obj of json) {
    datax.push(obj.Tijdstip);
    dataY.push(obj.Waarde);
  }
  datax.reverse();
  dataY.reverse();
  if (chartActive == false) {
    showChart(datax, dataY);
    chartActive = true;

  }
  else if (chartActive == true) {
    chart.updateOptions({
      xaxis: {
        categories: datax,
      },
      series: [
        {
          data: dataY,
        },
      ],
    });
  }

  //htmldata.innerHTML = htmlUitvoer;
};
const showEdit = function (json) {
  let htmlName = document.querySelector(".js-name");
  let htmlDate = document.querySelector(".js-datum");
  htmlDate.setAttribute("min", minimumDatum);
  let htmlaantal = document.querySelector(".js-aantall");
  let htmlbarcode = document.querySelector(".js-bar");
  let htmlImage = document.querySelector('.js-image');
  let dropdown = document.querySelector(".js-foto");
  htmlName.value = json.Naam;
  htmlDate.value = json.HoudbaarheidsDatum;
  htmlaantal.value = json.Aantal;
  htmlbarcode.value = json.Barcode;
  let str = json.Afbeelding;
  dropdown.selectedIndex = 0;
  if (str != null && str != 'https://fakeimg.pl/400x300/f1db26/000/') {
    dropdown.value = str;
  }
  else { dropdown.selectedIndex = 0; }
  htmlImage.src = json.Afbeelding == null || json.Afbeelding == 'https://fakeimg.pl/400x300/f1db26/000/' ? json.Afbeelding = 'https://fakeimg.pl/400x300/f1db26/000/' : `images/${json.Afbeelding}`;
};
const showFood = function (json) {
  console.log(json);

  let htmlUitvoer = ``;

  for (let obj of json) {

    let date = Date.parse(obj.HoudbaarheidsDatum);
    let vergelijk = Date.parse(datumVandaag);
    if (date < vergelijk) {
      htmlUitvoer += `<div class="c-card js-card">
              <div class="c-card__image-container js-img-card" data-id="${obj.idAanwezig}">
                <a style="display: flex;height: 187.5px;width: 250px;" href="edit_product.html?idaanwezig=${obj.idAanwezig}"><img src="${obj.Afbeelding == null || obj.Afbeelding == '' || obj.Afbeelding.length == 0 ? obj.Afbeelding = 'https://fakeimg.pl/400x300/f1db26/000/' : `images/${obj.Afbeelding}`}" alt="${obj.Naam}" class="c-card__img">
                </a>
                <h3 class="c-card--name">${obj.Naam}</h3>
              </div>
                <div class="c-card__content--overdatum">
                <span class="c-card--date">${obj.HoudbaarheidsDatum}(ex)</span><a href="edit_product.html?idaanwezig=${obj.idAanwezig}" class="u-icons"><span class="material-icons u-icons js-edit"data-id="${obj.idAanwezig}">edit</span></a><a href="delete.html?idaanwezig=${obj.idAanwezig}" class="u-icons"><span  class="material-icons u-icons js-delete">delete</span></a>
                </div>
            </div>`;
    }
    else {
      htmlUitvoer += `<div class="c-card js-card">
              <div class="c-card__image-container js-img-card" data-id="${obj.idAanwezig}">
                <a style="display: flex;height: 187.5px;width: 250px;" href="edit_product.html?idaanwezig=${obj.idAanwezig}"><img src="${obj.Afbeelding == null ? obj.Afbeelding = 'https://fakeimg.pl/400x300/f1db26/000/' : `images/${obj.Afbeelding}`}" alt="${obj.Naam}" class="c-card__img">
                </a>
                <h3 class="c-card--name">${obj.Naam}</h3>
              </div>
                <div class="c-card__content">
                <span class="c-card--date">${obj.HoudbaarheidsDatum}</span><a href="edit_product.html?idaanwezig=${obj.idAanwezig}" class="u-icons"><span class="material-icons u-icons js-edit"data-id="${obj.idAanwezig}">edit</span></a><a href="delete.html?idaanwezig=${obj.idAanwezig}" class="u-icons"><span  class="material-icons u-icons js-delete">delete</span></a>
                </div>
            </div>`;
    }

  }
  htmlCards.innerHTML = htmlUitvoer;
  listenToUI();
};
const showAccount = function (json) {
  let admin = document.querySelector(".js-admin");
  let admin2 = document.querySelector(".js-admin-2");
  const deleteButton = document.querySelector(".js-delete-user-button");
  if (json.idgebruiker == 1) {
    deleteButton.classList.add("u-hide--button");
    admin.innerHTML = `<a href="createAccount.html?id=1" class="c-nav__link">create account</a>`;
    admin2.innerHTML = `<a href="createAccount.html?id=1" class="c-nav__link">create account</a>`;
  }
  let naam = document.querySelector(".js-first").value = json.Naam;
  let voornaam = document.querySelector(".js-last").value = json.voornaam;
  let email = document.querySelector(".js-e-mail").value = json['E-mail'];
  if (naam == undefined || voornaam == undefined || email == undefined) {
    window.location.href = "index.html?gevonden=0";
  }
  listenToUpdateUser(json);
};
// #endregion 

// #region ***  Callback-No Visualisation - callback___  ***********
const callbackWindow = function () {
  window.location.href = "history.html";
};
// #endregion

// #region ***  Data Access - get___                     ***********
const getrain = function () {
  let urlParams = new URLSearchParams(window.location.search);
  let get = urlParams.get("idaanwezig");
  socket.emit("F2B_edit", get);
  listenToSocket();

};
// #endregion 

// #region ***  Event Listeners - listenTo___            ***********     

const listenToUI = function () {
  if (htmlIndex) {
    htmlDelete = document.querySelectorAll(".js-delete");
    for (let obj of htmlDelete) {
      obj.addEventListener("click", function () {
        console.log(obj.getAttribute("data-id"));
      });
    }
  }

};
const listenToClickBurger = function () {
  const burger = document.querySelector(".js-hamburger");
  const nav = document.querySelector(".js-nav");
  let teller = 0;
  burger.addEventListener('click', function () {
    teller++;
    if (teller === 1) {

      burger.classList.add("c-active");
    }
    else {
      burger.classList.remove("c-active");
      teller = 0;
    }
    console.log("CLICKE");
    document.querySelector("body").classList.toggle("has-mobile-nav");
  });
};
const listenToAddUser = function () {
  const button = document.querySelector(".js-add-user-button");
  button.addEventListener("click", function () {
    let user = document.querySelector(".js-first").value;
    let voornaamU = document.querySelector(".js-last").value;
    let emailU = document.querySelector(".js-e-mail").value;
    let passwoordU = document.querySelector(".js-pass-user").value;
    socket.emit("F2B_add_user", {
      naam: user,
      voornaam: voornaamU,
      email: emailU,
      passwoord: passwoordU
    });
  });
};
const listenToUpdateUser = function (json) {
  const button = document.querySelector(".js-update-user-button");
  const deleteButton = document.querySelector(".js-delete-user-button");
  deleteButton.addEventListener("click", function () {
    socket.emit('F2B_delete_account', json);
    window.location.href = "loadDeleteUser.html";
  });
  button.addEventListener("click", function () {
    let naamU = document.querySelector(".js-first").value;
    let voornaamU = document.querySelector(".js-last").value;
    let emailU = document.querySelector(".js-e-mail").value;
    let passwoordU = document.querySelector(".js-pass-user").value;
    console.log(passwoordU);
    if (passwoordU == "") {
      passwoordU = json.Passwoord;
      console.log(passwoordU);
    }
    socket.emit("F2B_update_user", {
      id: json.idgebruiker,
      naam: naamU,
      voornaam: voornaamU,
      email: emailU,
      passwoord: passwoordU
    });
  });
};
const listenToLogin = function () {
  const button = document.querySelector(".js-login-button");
  button.addEventListener("click", function () {
    socket.emit("F2B_gebruiker", {
      mail: document.querySelector(".js-email").value,
      passwoord: document.querySelector(".js-passwoord").value
    });
  });
  listenToSocket();
};
const listenToLoad = function () {
  window.addEventListener("load", function () {
    document.querySelector(".js-loader").classList.add("c-loader--hidden");
  });
};
const listenToChoiceDelete = function () {
  const buttonJa = document.querySelector(".js-ja");
  buttonJa.addEventListener("click", function () {
    let urlParams = new URLSearchParams(window.location.search);
    let get = urlParams.get("idaanwezig");
    socket.emit("F2B_delete_product", get);
  });
};
const listenTochangeDropdown = function () {
  let dropdown = document.querySelector(".js-foto");
  let img = document.querySelector(".js-image");
  dropdown.addEventListener("change", function () {
    img.src = `images/${dropdown.value}`;
    console.log(img.src);
  });
};
const listenToInput = function () {
  let barcode = document.querySelector(".js-barcode-offline");
  barcode.focus();
  let teller = 0;
  if (barcode.value.length != 13) {
    barcode.addEventListener("input", function () {
      console.log("invoer");
      socket.emit("F2B_barcode", barcode.value);
      teller++;
      console.log(teller);
      if (teller == 13) {
        barcode.value = "";
        window.location.reload(true);
      }
    });

  }

};
const listenToAdd = function () {
  const htmlButton = document.querySelector(".js-add-button");
  let datumPicker = document.querySelector(".js-date");
  datumPicker.setAttribute("min", minimumDatum);
  htmlButton.addEventListener("click", function () {
    console.log("toevoegen van nieuwe product");
    const jsonObj = {
      naam: document.querySelector(".js-naam").value,
      datum: datumPicker.value,
      aantal: document.querySelector(".js-aantal").value,
      barcode: document.querySelector(".js-barcode").value,
      foto: document.querySelector(".js-foto").value == '' ? null : document.querySelector(".js-foto").value
    };
    console.log(jsonObj);
    socket.emit("F2B_add-product", jsonObj);
  });
};
const listenToSocket = function () {
  if (htmlAdd) {
    socket.on("B2F_alAanwezig", function (json) {
      console.log(json);
    });
    listenToClickBurger();
  }
  if (htmlIndex) {
    socket.on("connect", function () {
      console.log("verbonden met socket");
    });
    socket.on("B2F_temperatuur", function (json) {
      let temp = `${json.temperatuur.waarde}°C`;
      console.log(
        `Current temperature : ${temp}`
      );
      showTemp(temp);
    });
    socket.on("B2F_connected", function (json) {
      showFood(json);
    });
    socket.on("B2F_deleted", function (json) {
      console.log(json);
    });
  }

  if (htmlHistory) {
    listenToClickBurger();
    socket.on("connect", function () {
      console.log("verbonden met socket");
    });
    socket.on("B2F_temperatuur", function (json) {
      let temp = `${json.temperatuur.waarde}°C`;
      console.log(
        `Current temperature : ${temp}`
      );
      showTemp(temp);
    });
    socket.on("B2F_aantal", function (json) {
      let htmlAantal = document.querySelector(".js-totaantal");
      htmlAantal.innerHTML = `Number of products present: ${json.aantal}`;
    });
    console.log("listen B2F_history");
    socket.on("B2F_history", (data) => {
      showHistory(data);
    });
  }
  if (htmlEditPro) {


    socket.on("B2F_edit", function (data) {
      console.log(data);
      if (data == -1) {
        console.log("niet gevonden");
      }
      else {
        console.log(data);
        showEdit(data);
      }
      const button = document.querySelector(".js-edit-button");
      button.addEventListener("click", function () {
        const jsonObj = {
          naam: document.querySelector(".js-name").value,
          datum: document.querySelector(".js-datum").value,
          aantal: document.querySelector(".js-aantall").value,
          barcode: document.querySelector(".js-bar").value,
          foto: document.querySelector(".js-foto").value == '' ? null : document.querySelector(".js-foto").value
        };
        socket.emit("F2B_edit_product", jsonObj);
        window.location.href = "index.html";
      });
    });
  }
  if (htmlloadDeleteAccount) {
    socket.emit("F2B_loadPage", 1);
    socket.on("B2F_user_delete", function (data) {
      console.log(data);

    });

    window.location.href = "index.html?del=1";

  }
  if (htmlloadlogin) {
    socket.emit("F2B_loadPage", 1);
    socket.on("B2F_user", function (data) {
      if (data == -1) {
        window.location.href = "index.html?gevonden=0";
      }
      else {
        window.location.href = `home.html?name=${data.voornaam}`;
      }
    });
  }
  if (htmlloadAccount) {
    socket.emit("F2B_account", 1);
    socket.on("B2F_account", function (data) {
      console.log(data);
      if (data == -1) {
        window.location.href = "index.html?gevonden=0";
      }
      else {
        window.location.href = `account.html?idgebruiker=${data['idgebruiker']}`;
      }
    });
  }
  if (htmlAccount) {
    listenToClickBurger();
    socket.emit("F2B_account", 1);
    socket.on("B2F_account", function (data) {
      showAccount(data);
    });
    socket.on("B2F_updated_user", function (data) {
      console.log(data);
      showAccount(data);
    });
  }
  if (htmlCreateAccount) {
    listenToClickBurger();
  }
};

// #endregion      
// #region ***  Init / DOMContentLoaded                  ***********   
const init = function () {

  listenToLoad();

  console.info("DOM geladen");

  htmlIndex = document.querySelector(".js-index");
  htmlHistory = document.querySelector(".js-history");
  htmlCards = document.querySelector(".js-cards");
  htmlAdd = document.querySelector(".js-form");
  htmlOff = document.querySelector(".js-offline");
  htmlEditPro = document.querySelector(".js-edit_pro");
  htmlDeletePage = document.querySelector(".js-delete-page");
  htmlLogin = document.querySelector(".js-login");
  htmlloadlogin = document.querySelector(".js-tussen");
  htmlloadAccount = document.querySelector(".js-tussen-account");
  htmlAccount = document.querySelector(".js-account");
  htmlLoadUpdatedAccount = document.querySelector(".js-update-account-load");
  htmlCreateAccount = document.querySelector(".js-create-account");
  htmlloadDeleteAccount = document.querySelector(".js-delete-account-load");
  htmlTest = document.querySelector(".js-test");
  if (htmlTest) {
    listenToClickBurger();
  }
  if (htmlLogin) {
    listenToLogin();
  }
  if (htmlIndex) {
    listenToClickBurger();
    let loginParam = new URLSearchParams(window.location.search);
    let getUser = loginParam.get("name");
    let urlParams = new URLSearchParams(window.location.search);
    let get = urlParams.get("del");
    let urlParam2 = new URLSearchParams(window.location.search);
    let getEdit = urlParam2.get("edit");
    let getAdd = new URLSearchParams(window.location.search);
    let add = getAdd.get("add");
    if (get != null || get != 'undefind' || get != 0) {
      console.log(get);
      console.log("product verwijderd");
    }
    if (getUser == null && get == null && getEdit == null && add == null) {
      window.location.href = "index.html";
    }
  }
  if (htmlOff) {
    listenToInput();
  }
  if (htmlAdd) {
    listenToAdd();
    listenTochangeDropdown();
  }
  if (htmlEditPro) {
    getrain();
    listenToClickBurger();
    listenTochangeDropdown();
  }
  if (htmlDeletePage) {
    listenToChoiceDelete();
  }
  if (htmlCreateAccount) {
    let urlParams = new URLSearchParams(window.location.search);
    let get = urlParams.get("id");
    if (get == null || get != 1) {
      window.location.href = "index.html?gevonden=0";
    }
    else {
      listenToAddUser();
    }
  }
  listenToSocket();
};
document.addEventListener("DOMContentLoaded", init);
// #endregion