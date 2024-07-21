
// <html lang="en">
// <head>
//     <meta charset="UTF-8">
//     <meta name="viewport" content="width=device-width, initial-scale=1.0">
//     <title>Document</title>
//     <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
// </head>
// <body>
//     <p id="ip"></p>
//     <p id="contry"></p>
//     <p id="city"></p>
//     <p id="provider"></p>
//     <label for="">My IP: </label>
//     <label for="" id="myIp"></label>
//     <button></button>

// <script>
        
//         const ipadd = document.getElementById('ip');
//         const contry1 = document.getElementById('contry');
//         const city1 = document.getElementById('city');
//         const provider = document.getElementById('provider');
        
//         fetch('http://ip-api.com/json/?fields=61439')
//             .then(res => res.json())
//             .then(res => {
//                 console.log(res);
//                 ipadd.textContent = res.query;
//                 contry1.textContent = res.country;
//                 city1.textContent = res.city;
//                 provider.textContent = res.isp;
//             });

//             $.getJSON("https://api.ipify.org?format=json",function(data){
//                 $("#myIp").html(data.ip);
//             });



//     </script>
// </body>
// </html> --></head>