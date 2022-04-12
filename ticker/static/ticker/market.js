function inp_control(field, btn) {
   // Disable submit if input field is empty
   if (field.value > 0) {
      btn.disabled = false;
   } else {
      btn.disabled = true;
   }
}


document.addEventListener('DOMContentLoaded', function() {


   // Show buy view by default
   view_control('buy-view');

   // Send a GET request to fetch BTC price
   fetch('https://openexchangerates.org/api/latest.json?app_id=0a457942bd3f46de80adf3a783cfbd74')
   .then(response => response.json())
   .then(data => {

      // USD/BTC
      const rate = data.rates['BTC'];

      // 1 satoshi = 0.00000001 BTC
      const sat_multiplier = 100000000;

      // Validate data
      if (rate != undefined) {

         /* Ticker displays */

         // Convert to satoshi
         satoshi = rate * sat_multiplier;
         // Display results
         document.querySelector('#satoshi').innerHTML = `1 USD = ${satoshi.toFixed()} SATS`;

         // Calculate BTC/USD value
         const btc_usd = (1/rate).toFixed(2);

         // Display BTC ticker
         document.querySelector('#ticker').innerHTML = `$${btc_usd}`;


         /* Buy orders */

         // Variables for buy form
         var sell_cash = document.querySelector('#sell-cash');
         var buy_asset = document.querySelector('#buy-asset');
         const buy = document.querySelector('#buy');

         // Pre-fill buy form fields
         sell_cash.value = 1;
         buy_asset.value = rate.toFixed(8);
         document.querySelector('#current-buy-price').value = btc_usd;

         // Change asset field when cash field changes
         sell_cash.onkeyup = () => {
            inp_control(sell_cash, buy);
            // Calculate corresponding asset value
            buy_asset.value = (sell_cash.value * rate).toFixed(8);
         };

         // Change cash field when asset value changes
         buy_asset.onkeyup = () => {
            inp_control(buy_asset, buy);
            // Calculate corresponding cash value
            sell_cash.value = (buy_asset.value * btc_usd).toFixed(2);

         };

         /* Sell Orders */

         // Variables for sell form
         var buy_cash = document.querySelector('#buy-cash');
         var sell_asset = document.querySelector('#sell-asset');
         const sell = document.querySelector('#sell');

         // Pre-fill sell form fields
         buy_cash.value = 1;
         sell_asset.value = rate.toFixed(8);
         document.querySelector('#current-sell-price').value = btc_usd;

         // Change cash field when asset value changes
         sell_asset.onkeyup = () => {
            inp_control(sell_asset, sell);
            buy_cash.value = (sell_asset.value * btc_usd).toFixed(2);
         };

         // Change asset field when cash value changes
         buy_cash.onkeyup = () => {
            inp_control(buy_cash, sell);
            // Calculate corresponding value
            sell_asset.value = (buy_cash.value * rate).toFixed(8);
         };

      // Event handler for controlling view
      document.querySelectorAll('button').forEach(button => {

         // Select all buttons
         button.onclick = function() {
            if (this.dataset.val === 'buy-view' || this.dataset.val === 'sell-view' ) {
               // When clicked, modify view accordingly
               view_control(this.dataset.val);
            }
            return false;
         }
      })


      } else {
         // Display error message
         document.querySelector('#satoshi').innerHTML = 'Invalid Currency';
      }
   }).catch(error => {
      console.log('Error', error);
   })

   // Tooltips
   var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
   var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
     return new bootstrap.Tooltip(tooltipTriggerEl)
   })
});

function view_control(view) {
   document.querySelectorAll('.view-control').forEach(div => {
      div.style.display = 'none';
   });
   document.querySelector(`#${view}`).style.display = 'block';
}
