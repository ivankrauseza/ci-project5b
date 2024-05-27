console.log("sanity check");

// Get Stripe publishable key
fetch("/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});

$(document).ready(function(){
  var adminBar = $(".adminbar");
  var adminBarHeight = adminBar.outerHeight();
  var scrollThreshold = 100; // Pixels from top to start animation
  
  // Function to handle scrolling
  $(window).scroll(function() {
      var scroll = $(this).scrollTop();
      
      // If scrolled down past the threshold, slide the admin bar into position
      if (scroll > scrollThreshold) {
        // Initially hide the admin bar
          adminBar.css({top: -adminBarHeight, position: 'fixed', width: '100%', zIndex: 9999});
          adminBar.stop().animate({top: 0}, 300);
      } else {
          // If not, hide the admin bar
          adminBar.css({top: -0, position: 'relative', width: '100%', zIndex: 9999});
          adminBar.stop().animate({top: -0}, 300);
      }
  });
});