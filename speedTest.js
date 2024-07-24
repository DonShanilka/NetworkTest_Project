document.getElementById('startTest').addEventListener('click', () => {
    testDownloadSpeed().then(downloadSpeed => {
        document.getElementById('downloadSpeed').innerText = downloadSpeed.toFixed(2);
        return testUploadSpeed();
    }).then(uploadSpeed => {
        document.getElementById('uploadSpeed').innerText = uploadSpeed.toFixed(2);
    }).catch(error => {
        console.error("Error testing network speed: ", error);
    });
});

function testDownloadSpeed() {
    return new Promise((resolve, reject) => {
        const downloadSize = 1 * 1024 * 1024; // 5 MB
        const startTime = (new Date()).getTime();

        fetch('https://api.techniknews.net/ipgeo/', { cache: 'no-cache' })
            .then(response => response.blob())
            .then(blob => {
                const endTime = (new Date()).getTime();
                const duration = (endTime - startTime) / 1024; // seconds
                const bitsLoaded = downloadSize * 8;
                const speedBps = bitsLoaded / duration;
                const speedMbps = speedBps / (1024 * 1024);
                resolve(speedMbps);
            })
            .catch(reject);
    });
}

function testUploadSpeed() {
    return new Promise((resolve, reject) => {
        const uploadSize = 1 * 1024 * 1024; // 2 MB
        const data = new Uint8Array(uploadSize);
        const startTime = (new Date()).getTime();

        fetch('http://ip-api.com/json', {
            method: 'POST',
            body: data,
            headers: {
                'Content-Type': 'application/octet-stream'
            }
        })
            .then(response => response.text())
            .then(() => {
                const endTime = (new Date()).getTime();
                const duration = (endTime - startTime) / 1000; // seconds
                const bitsUploaded = uploadSize * 8;
                const speedBps = bitsUploaded / duration;
                const speedMbps = speedBps / (1024 * 1024);
                resolve(speedMbps);
            })
            .catch(reject);
    });
}

const ipadd = document.getElementById('ip');
const contry1 = document.getElementById('contry');
const city1 = document.getElementById('city');
const provider = document.getElementById('provider');

fetch('https://api.techniknews.net/ipgeo/')
    .then(res => res.json())
    .then(res => {
        console.log(res);
        ipadd.textContent = res.query;
        contry1.textContent = res.country;
        city1.textContent = res.city;
        provider.textContent = res.isp;
    });

$.getJSON("https://api.techniknews.net/ipgeo/", function (data) {
    $("#myIp").html(data.ip);
});

$.getJSON('https://api.techniknews.net/ipgeo/', function (data) {
    $('#gmps').attr("src", "https://www.google.com/maps?q=" + data.lat + "," + data.lon + "&output=embed")
});


let resDiv = document.querySelector('#internet_info');
let ipElem = document.querySelector('#ipValue')
getIpaddress();

function getIpaddress() {
    fetch('https://api.techniknews.net/ipgeo/').then(res => {
        return res.json()
    }).then(data => {
        getInternet_info(data.ip)
        ipElem.innerHTML = data.ip;
    }).catch(err => {
        console.log(`There was an error ${err}`)
    })
}


function getInternet_info(ip) {
    let ipAddress = ip;
    let output = "";

    fetch(`https://api.techniknews.net/ipgeo/${ipAddress}`).then(res => {
        return res.json()
    }).then(data => {
        output += `
      <ul class="collection">
        <li class="collection-item">Country:: <strong>${data.country}</strong></li>
        <li class="collection-item">City:: <strong>${data.city}</strong></li>
        <li class="collection-item">Region:: <strong>${data.regionName}</strong></li>
        <li class="collection-item">Timezone:: <strong>${data.timezone}</strong></li>
        <li class="collection-item">Lat:: <strong>${data.lat}</strong></li>
        <li class="collection-item">Lon:: <strong>${data.lon}</strong></li>
        <li class="collection-item">Internet Organisation:: <strong>${data.org}</strong></li>
        <li class="collection-item">Zip Code:: <strong>${data.zip ? data.zip : 'Unavailable(no Zip)'}</strong></li>
      </ul>
    `;
        resDiv.innerHTML = output;
        console.log(data)
    }).catch(err => {
        console.log(`There was an error in the info function:: ${err}`)
    })
}
