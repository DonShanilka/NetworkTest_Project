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
        const downloadSize = 5 * 1024 * 1024; // 5 MB
        const startTime = (new Date()).getTime();

        fetch('http://ip-api.com/json', { cache: 'no-cache' })
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
        const uploadSize = 4 * 1024 * 1024; // 2 MB
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

fetch('http://ip-api.com/json')
    .then(res => res.json())
    .then(res => {
        console.log(res);
        ipadd.textContent = res.query;
        contry1.textContent = res.country;
        city1.textContent = res.city;
        provider.textContent = res.isp;
    });

// $.getJSON("https://api.ipify.org?format=json", function (data) {
//     $("#myIp").html(data.ip);
// });

$.getJSON('http://ip-api.com/json', function (data) {
    $('#gmps').attr("src", "https://www.google.com/maps?q=" + data.lat + "," + data.lon + "&output=embed");
});
