var lastSliderValue = null  //TODO chcelo by to nemat public variable 


function post(data, callback) {
    $.ajax({
        type: "POST",
        url: "/chromecast",
        data: JSON.stringify(data),
        success: successFunc,
        contentType: "application/json",
        dataType: "json"
      })
        .fail(function (xhr, status, error) {
            onAjaxError(xhr, status, error)
        })

    function successFunc(data) {
        // console.log(data)
        if (callback != null) {
            callback()
        }
    };
}

function onAjaxError(jqXHR, textStatus, errorThrown) {
    console.log(jqXHR)
    console.log(textStatus)
    console.log(errorThrown)
    setVybranaText("")
    if (jqXHR.status === 0) {
        document.getElementById("statusText").innerHTML = 'ERROR Server off';
        setVybranaText("Or no internet connection.")
    } else {
        document.getElementById("statusText").innerHTML = 'ERROR Server error';
        setVybranaText(`${textStatus}:  ${errorThrown}`)
    }
}

function getPostJson(...actions) {
    let newJson = []
    newJson.push({"action": "chromecast", "value": $("input[name=selectChromecast]:checked").val()})
    for(let i = 0; i < actions.length; i++) {
        if(typeof actions[i] === "string") {
            newJson.push({"action": actions[i]})
        } else {
            newJson.push({"action": actions[i][0], "value": actions[i][1]})
        }
    }
    return newJson
}

function sendRequest(action, url = null, callback = null) {
    if (url !== null) {
        post({ 'action': action, 'url': url }, callback)
    } else {
        post({ 'action': action }, callback)
    }
}

function onDesign() {
    document.getElementById("buttonOn").style.color = "#FF0000"
    document.getElementById("buttonOff").style.color = "#000000"
}

function onStatus() {
    document.getElementById("statusText").innerHTML = 'Radio On';
}

function offDesign() {
    document.getElementById("buttonOff").style.color = "#FF0000"
    document.getElementById("buttonOn").style.color = "#000000"
}

function offStatus() {
    document.getElementById("statusText").innerHTML = 'Radio Off';
}



function zapnut() {
    onDesign()
    onStatus()
    setVybranaText(getSelectedStanica().textContent)
}

function vypnut() {
    offDesign()
    offStatus()
    setVybranaText("")
}


//UNUSED
function connect() {
    post(getPostJson('connect'))
}
function disconnect() {
    post(getPostJson('disconnect'))
}
function stop() {
    post(getPostJson('stop'))
}



$(document).ready(function () {
    // loadChromecasts()
    // loadStanice(loadSettings)
    $.when(loadChromecasts(), loadStanice()).done(function(chromecast_data, stanice_data) {
        loadSettings()

        $("input[name=selectChromecast]").change(function() {
        loadSettings() //DONT LOAD CHANNELS ALWAYS
    })
    })
})

function setVybranaText(text) {
    document.getElementById("vybrana").innerHTML = text;
}

function loadChromecasts() {
    //data = [{"name":<str>, "url:<str>"}, ...]
    data = [
    {
        "displayName": "Chomecast 1",
        "friendlyName": "Audio-Pracovna"
    },
    {
        "displayName": "Chomecast 2",
        "friendlyName": "OTHER FRIENDLY NAME"
    }
    ]
    $("#cover").show();
    chromecastsSetup(data)
    $("#cover").hide();
}

function loadStanice() {
    //data = [{"name":<str>, "url:<str>"}, ...]
    data = [
    {
        "name": "24/7 Royalty Free Music",
        "url": "https://ec3.yesstreaming.net:3585/stream"
    },
    {
        "name": "Butterflies - Zane Little",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/z4CDjchx1oLrTs1OjOtupGZpO0w9SilxK0o5ECiZ.mp3"
    },
    {
        "name": "C'est La Vie",
        "url": "https://files.freemusicarchive.org/storage-freemusicarchive-org/tracks/3RahChJRrtlnO9m1xoBAKPvuvxr6aR99sh4JIUwf.mp3"
    }
    ]
    $("#cover").show();
    staniceSetup(data)
    $("#cover").hide();
}

function loadSettings() {
    data = {"is_playing": false, "volume":69}
    $("#cover").show();
    callback(data)
    // $.ajax({
    //     type: "POST",
    //     url: "/setup",
    //     data: JSON.stringify({"chromecast": $("input[name=selectChromecast]:checked").val()}),
    //     success: callback,
    //     contentType: "application/json",
    //     dataType: "json",
    //     timeout: 15000,
    //     error: callbackError
    //     });
    
    function callback(data) {
        if (data.is_playing == true) {
            onDesign()
            onStatus()
            let stanica = getStanicaByUrl(data.url).textContent
            if (stanica != undefined) {
                setVybranaText(getStanicaByUrl(data.url).textContent)
            }
        } else {
            offDesign()
            offStatus()
            setVybranaText("")
        }

        if (data.volume >= 0) {
            slider = document.getElementById("volumeController")
            slider.value = data.volume
            lastSliderValue = slider.value
        }
        sliderInput()
        volumeTextActive()
        $("#cover").hide();

    }

    function callbackError(jqXHR, textStatus, errorThrown) {
        $("#cover").hide();
        onAjaxError(jqXHR, textStatus, errorThrown)
    }
}


function staniceSetup(links) {
    const staniceDiv = document.getElementById("stanice")
    for (let i = 0; i < links.length; i++) {
        const node = document.createElement("button");
        const textnode = document.createTextNode(links[i].name);
        node.setAttribute('data-url', links[i].url)
        node.setAttribute("data-selected", "false")
        node.setAttribute("class", getBootstrapString())
        node.setAttribute("onClick", "setSelectedStanica(this);")
        node.appendChild(textnode);
        staniceDiv.appendChild(node);
    }

    cookie = getCookie('stanica')
    const stanice = document.getElementById("stanice").children
    var success = false
    for (let i = 0; i < stanice.length; i++) {
        if (stanice[i].textContent == cookie) {
            setSelectedStanica(stanice[i])
            success = true
            break
        }
    }
    if (!success) {
        console.log('neni cookie')
        setSelectedStanica(stanice[0])
    }

}

// TODO
function chromecastsSetup(data) {
    // <input value="Audio-Kuchyna" type="radio" class="selectButton btn-check" name="selectChromecast" id="option1" autocomplete="off" checked="checked">
    // not in list: value, id, checked
    // <label class="btn btn-default chromecastSelect" for="option1">Kuchyňa</label>
    const attributesInput = [
        ["type", "radio"],
        ["class", "selectButton btn-check"],
        ["name", "selectChromecast"],
        ["autocomplete", "off"]
    ]

    const chromecastDiv = document.getElementById("chromecasts")
    for (let i = 0; i < data.length; i++) {
        const input = document.createElement("input");
        const label = document.createElement("label");
        const textnode = document.createTextNode(data[i].displayName);

        if (i == 0) {
            input.setAttribute("checked", "checked")
        }
        for (let j = 0; j < attributesInput.length; j++) {
            input.setAttribute(attributesInput[j][0], attributesInput[j][1])
        }
        input.setAttribute("value", data[i].friendlyName)
        input.setAttribute("id", `chromecastOption${i}`)

        label.setAttribute("class", "btn btn-default chromecastSelect")
        label.setAttribute("for", `chromecastOption${i}`)
        label.appendChild(textnode);
        chromecastDiv.appendChild(input);
        chromecastDiv.appendChild(label);
    }
    // MAYBE TODO CHORMECAST DO COOKIE

    // cookie = getCookie('stanica')
    // const stanice = document.getElementById("stanice").children
    // var success = false
    // for (let i = 0; i < stanice.length; i++) {
    //     if (stanice[i].textContent == cookie) {
    //         setSelectedStanica(stanice[i])
    //         success = true
    //         break
    //     }
    // }
    // if (!success) {
    //     console.log('neni cookie')
    //     setSelectedStanica(stanice[0])
    // }

}

function getBootstrapString(active = false) {
    classes = [
        "list-group-item",
        "list-group-item-action",
        "stanica-btn"
    ]
    if (active) {
        classes.push("active")
    }
    return classes.join(" ")
}

function setSelectedStanica(selected) {
    const stanice = document.getElementById("stanice").children
    for (let i = 0; i < stanice.length; i++) {
        if (stanice[i].getAttribute("data-selected") == "true") {
            stanice[i].setAttribute("data-selected", "false")
            stanice[i].setAttribute("class", getBootstrapString())
        }
    }
    selected.setAttribute("data-selected", "true")
    selected.setAttribute("class", getBootstrapString(true))

    setCookie('stanica', selected.textContent, 365 * 5);
}

function getSelectedStanica() {
    const stanice = document.getElementById("stanice").children
    for (let i = 0; i < stanice.length; i++) {
        if (stanice[i].getAttribute("data-selected") == "true") {
            return stanice[i]
        }
    }
}

function getStanicaByUrl(url) {
    const stanice = document.getElementById("stanice").children
    for (let i = 0; i < stanice.length; i++) {
        if (stanice[i].getAttribute("data-url") == url) {
            return stanice[i]
        }
    }
    return "Not found"
}

function volumeTextActive() {
    volumeText = document.getElementById("volume")
    volume.style.color = "#000000"
}

function volumeTextInactive() {
    return
    volumeText = document.getElementById("volume")
    volume.style.color = "var(--secondary-gray)"
}

function sliderInput() {
    slider = document.getElementById("volumeController")
    document.getElementById("volume").innerHTML = slider.value
    if (lastSliderValue == slider.value) {
        volumeTextActive()
    } else {
        volumeTextInactive()
    }
}

function sliderChange() {
    slider = document.getElementById("volumeController")
    volumeText = document.getElementById("volume")
    volumeTextInactive()
    lastSliderValue = slider.value

    // post(getPostJson(["volume", slider.value]), function() {
    //     volumeTextActive()
    // })
}

function setCookie(cname, cvalue, exdays) {
    const d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    let expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
