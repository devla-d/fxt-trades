(function ($) {
  "user strict";
  
    var prevScrollpos = window.pageYOffset;
    var scrollPosition = window.scrollY;
    if (scrollPosition >= 1) {
      $(".header-bottom").addClass('active');
    }
    window.onscroll = function () {
      var currentScrollPos = window.pageYOffset;
      if (prevScrollpos > currentScrollPos) {
        $(".header-bottom").addClass('active');
      } else {
        $(".header-bottom").removeClass('active');
      }
      prevScrollpos = currentScrollPos;
      if (currentScrollPos === 0) {
        $(".header-bottom").removeClass('active');
      } 
    }
    if ($('.client-slider').length) {
        $('.client-slider').owlCarousel({
            center: true,
            items: 1,
            autoplay: true,
            autoplayTimeout: 5000,
            loop: true,
            margin: 0,
            singleItem: true,
            nav: true,
            dots: false,
            thumbs: true,
            thumbsPrerendered: true,
            navText: ["<i class='fas fa-angle-right'></i>", "<i class='fas fa-angle-right'></i>"
            ],
        });
    }
  $('.mon_wr').owlCarousel({
    loop: true,
    dots: true,
    margin: 30,
    item: 1,
    autoplay: true,
    autoplayTimeout: 2000,
    responsive: {
        0: {
            items: 1
        },
        768: {
            items: 1
        },
        960: {
            items: 5
        },
        1200: {
            items: 5
        },
        1920: {
            items: 5
        }
    }
  });

    //Odometer
    $(".counter-item").each(function () {
        $(this).isInViewport(function (status) {
            if (status === "entered") {
                for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
                    var el = document.querySelectorAll('.odometer')[i];
                    el.innerHTML = el.getAttribute("data-odometer-final");
                }
            }
        });
    });


    /* -----------------------------------------------
  /* How to use? : Check the GitHub README
  /* ----------------------------------------------- */

/* To load a config file (particles.json) you need to host this demo (MAMP/WAMP/local)... */
/*
particlesJS.load('particles-js', 'particles.json', function() {
  console.log('particles.js loaded - callback');
});
*/

/* Otherwise just put the config content (json): */

particlesJS('particles-js',
  
{
  "particles": {
    "number": {
      "value": 80,
      "density": {
        "enable": true,
        "value_area": 800
      }
    },
    "color": {
      "value": "#f00"
    },
    "shape": {
      "type": "circle",
      "stroke": {
        "width": 0,
        "color": "#000000"
      },
      "polygon": {
        "nb_sides": 5
      },
      "image": {
        "src": "img/github.svg",
        "width": 100,
        "height": 100
      }
    },
    "opacity": {
      "value": 0.5,
      "random": false,
      "anim": {
        "enable": false,
        "speed": 1,
        "opacity_min": 0.1,
        "sync": false
      }
    },
    "size": {
      "value": 5,
      "random": true,
      "anim": {
        "enable": false,
        "speed": 40,
        "size_min": 0.1,
        "sync": false
      }
    },
    "line_linked": {
      "enable": true,
      "distance": 150,
      "color": "#f00",
      "opacity": 0.4,
      "width": 1
    },
    "move": {
      "enable": true,
      "speed": 3,
      "direction": "none",
      "random": false,
      "straight": false,
      "out_mode": "out",
      "attract": {
        "enable": false,
        "rotateX": 600,
        "rotateY": 1200
      }
    }
  },
  "interactivity": {
    "detect_on": "canvas",
    "events": {
      "onhover": {
        "enable": true,
        "mode": "repulse"
      },
      "onclick": {
        "enable": true,
        "mode": "push"
      },
      "resize": true
    },
    "modes": {
      "grab": {
        "distance": 400,
        "line_linked": {
          "opacity": 1
        }
      },
      "bubble": {
        "distance": 400,
        "size": 40,
        "duration": 2,
        "opacity": 8,
        "speed": 3
      },
      "repulse": {
        "distance": 200
      },
      "push": {
        "particles_nb": 4
      },
      "remove": {
        "particles_nb": 2
      }
    }
  },
  "retina_detect": true,
  "config_demo": {
    "hide_card": false,
    "background_color": "#b61924",
    "background_image": "",
    "background_position": "50% 50%",
    "background_repeat": "no-repeat",
    "background_size": "cover"
  }
}

);


  })(jQuery);
   
        