/*global $ */
$(document).ready(function () {
/*------------------
   SignUp And Login
--------------------*/
$('.scroll_top').click(function(){
  $('html,body').animate({ 
    'scrollTop': 0 
  }, 'slow');
});
$("#login-show").click(function() {
  $("#login-modal").fadeIn();
});

$(".signup-show").click(function() {
  $("#signup-modal").fadeIn();
});

$('.close-modal').click(function() {
  $('#login-modal').fadeOut();
  $('#signup-modal').fadeOut();
});



    "use strict";

    $(function () {
        $('[data-toggle="popover"]').popover()
      });

      $(function () {
        $('.example-popover').popover({
          container: 'body'
        });
      });

    $('.menu > ul > li:has( > ul)').addClass('menu-dropdown-icon');
    //Checks if li has sub (ul) and adds class for toggle icon - just an UI


    $('.menu > ul > li > ul:not(:has(ul))').addClass('normal-sub');
    //Checks if drodown menu's li elements have anothere level (ul), if not the dropdown is shown as regular dropdown, not a mega menu (thanks Luka Kladaric)

    $(".menu > ul").before("<a href=\"#\" class=\"menu-mobile\">Navigation</a>");

    //Adds menu-mobile class (for mobile toggle menu) before the normal menu
    //Mobile menu is hidden if width is more then 959px, but normal menu is displayed
    //Normal menu is hidden if width is below 959px, and jquery adds mobile menu
    //Done this way so it can be used with wordpress without any trouble

    $(".menu > ul > li").hover(
        function (e) {
            if ($(window).width() > 943) {
                $(this).children("ul").fadeIn(150);
                e.preventDefault();
            }

        }, function (e) {
            if ($(window).width() > 943) {
                $(this).children("ul").fadeOut(150);
                e.preventDefault();
            }
        }
    );
    //If width is more than 943px dropdowns are displayed on hover


    //the following hides the menu when a click is registered outside
    $(document).on('click', function(e){
        if($(e.target).parents('.menu').length === 0)
            $(".menu > ul").removeClass('show-on-mobile');
    });

    $(".menu > ul > li").click(function() {
        //no more overlapping menus
        //hides other children menus when a list item with children menus is clicked
        var thisMenu = $(this).children("ul");
        var prevState = thisMenu.css('display');
        $(".menu > ul > li > ul").fadeOut();
        if ($(window).width() < 943) {
            if(prevState !== 'block')
                thisMenu.fadeIn(150);
        }
    });
    //If width is less or equal to 943px dropdowns are displayed on click

    $(".menu-mobile").click(function (e) {
        $(".menu > ul").toggleClass('show-on-mobile');
        e.preventDefault();
    });
    //when clicked on mobile-menu, normal menu is shown as a list, classic rwd menu story

    /*-------------------
		Quantity change
	--------------------- */
// var proQty = $('.pro-qty');
// proQty.prepend('<a href="{% url "item_decrement" value.product_id %}"><span class="dec qtybtn">-</span></a>');
// proQty.append('<a href="{% url "item_increment" value.product_id %}"><span class="inc qtybtn">+</span></a>');
// proQty.on('click', '.qtybtn', function () {
//     var $button = $(this);
//     var oldValue = $button.parent().find('input').val();
//     if ($button.hasClass('inc')) {
//         var newVal = parseFloat(oldValue) + 1;
//     } else {
//         // Don't allow decrementing below zero
//         if (oldValue > 0) {
//             var newVal = parseFloat(oldValue) - 1;
//         } else {
//             newVal = 0;
//         }
//     }
//     $button.parent().find('input').val(newVal);
// });

/*------------------
    Single Product
--------------------*/
$('.product-thumbs-track > .pt').on('click', function(){
    $('.product-thumbs-track .pt').removeClass('active');
    $(this).addClass('active');
    var imgurl = $(this).data('imgbigurl');
    var bigImg = $('.product-big-img').attr('src');
    if(imgurl != bigImg) {
        $('.product-big-img').attr({src: imgurl});
        $('.zoomImg').attr({src: imgurl});
    }
});


$('.product-pic-zoom').zoom();

/*------------------
    Accordions
--------------------*/
$('.panel-link').on('click', function (e) {
    $('.panel-link').removeClass('active');
    var $this = $(this);
    if (!$this.hasClass('active')) {
        $this.addClass('active');
    }
    e.preventDefault();
});

/*------------------
    Brands Slider
--------------------*/
$('.product-slider').owlCarousel({
    loop: true,
    nav: true,
    dots: false,
    margin : 30,
    autoplay: true,
    navText: ['<i class="flaticon-left-arrow-1"></i>', '<i class="flaticon-right-arrow-1"></i>'],
    responsive : {
        0 : {
            items: 1,
        },
        480 : {
            items: 2,
        },
        768 : {
            items: 3,
        },
        1200 : {
            items: 4,
        }
    }
});



});


//////////////////////////// Js For Submit Form for payment
// Create a Stripe client.
var stripe = Stripe('pk_test_TYooMQauvdEDq54NiTphI7jx');

// Create an instance of Elements.
var elements = stripe.elements();

// Custom styling can be passed to options when creating an Element.
// (Note that this demo uses a wider set of styles than the guide below.)
var style = {
  base: {
    color: '#32325d',
    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
    fontSmoothing: 'antialiased',
    fontSize: '16px',
    '::placeholder': {
      color: '#aab7c4'
    }
  },
  invalid: {
    color: '#fa755a',
    iconColor: '#fa755a'
  }
};

// Create an instance of the card Element.
var card = elements.create('card', {style: style});

// Add an instance of the card Element into the `card-element` <div>.
card.mount('#card-element');

// Handle real-time validation errors from the card Element.
card.on('change', function(event) {
  var displayError = document.getElementById('card-errors');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

// Handle form submission.
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.createToken(card).then(function(result) {
    if (result.error) {
      // Inform the user if there was an error.
      var errorElement = document.getElementById('card-errors');
      errorElement.textContent = result.error.message;
    } else {
      // Send the token to your server.
      stripeTokenHandler(result.token);
    }
  });
});

// Submit the form with the token ID.
function stripeTokenHandler(token) {
  // Insert the token ID into the form so it gets submitted to the server
  var form = document.getElementById('payment-form');
  var hiddenInput = document.createElement('input');
  hiddenInput.setAttribute('type', 'hidden');
  hiddenInput.setAttribute('name', 'stripeToken');
  hiddenInput.setAttribute('value', token.id);
  form.appendChild(hiddenInput);

  // Submit the form
  form.submit();
}


{/* <html>
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
        <link rel="stylesheet" href="index.css">
    </head>
    <body>
   <div class="container">
  <textarea type="text" id="string" placeholder="Type in the box"></textarea>
  <div id="counterFooter"><span class="reduce">140</span>/140</div>

    <button id="btn"><h2>Tweet</h2></button>
</div>
        <script src="index.pack.js"></script>
    </body>
</html>

$(function() {
  $('#string').keydown(function() {
    var typedString = $('#string').val().length;
    
    
    
    
    if(typedString > 120){
      $('#counterFooter').css('color','red');
  }
  if(typedString>140){
      $('#btn').addClass('buttonDisabled');
  }
  
});

});

$(function() {
  $('#string').keydown(function() {
    var typedString = $('#string').val().length;
    
    var textLeft= 140;
     if(typedString != ''){
         textLeft -= typedString;
     }
    
    $('.reduce').text(textLeft);
    
    
    
    
    if(typedString > 120){
        $('#counterFooter').css('color','red');
    }
    if(typedString>140){
        $('#btn').addClass('buttonDisabled');
    }
    
});

}); */}
