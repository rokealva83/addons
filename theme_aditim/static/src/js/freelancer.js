/*!
 * Start Bootstrap - Freelancer Bootstrap Theme (http://startbootstrap.com)
 * Code licensed under the Apache License v2.0.
 * For details, see http://www.apache.org/licenses/LICENSE-2.0.
 */

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('body').on('click', '.page-scroll a', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        },1000, 'easeInOutExpo');
        event.preventDefault();
    });
	
});

// Floating label headings for the contact form
$(function() {
    $("body").on("input propertychange", ".floating-label-form-group", function(e) {
        $(this).toggleClass("floating-label-form-group-with-value", !! $(e.target).val());
    }).on("focus", ".floating-label-form-group", function() {
        $(this).addClass("floating-label-form-group-with-focus");
    }).on("blur", ".floating-label-form-group", function() {
        $(this).removeClass("floating-label-form-group-with-focus");
    });
});

// Highlight the top nav as scrolling occurs
$('body').scrollspy({
    target: '.navbar-fixed-top'
})

// Highlight the top nav as scrolling occurs
$('body').scrollspy({
    target: '.navbar-fixed-top2'
})

// Closes the Responsive Menu on Menu Item Click
$('.navbar-collapse ul li a').click(function() {
    $('.navbar-toggle:visible').click();
});

$(function () {
    // Remove Search if user Resets Form or hits Escape!
	$('body, .navbar-coll form[role="search"] button[type="reset"]').on('click keyup', function(event) {
		if (event.which == 27 && $('.navbar-coll form[role="search"]').hasClass('active') ||
			$(event.currentTarget).attr('type') == 'reset') {
			closeSearch();
		}
	});
	function closeSearch() {
        var $form = $('.navbar-coll form[role="search"].active')
		$form.find('input').val('');
		$form.removeClass('active');
	}
	// Show Search if form is not active // event.preventDefault() is important, this prevents the form from submitting
	$(document).on('click', '.navbar-coll form[role="search"]:not(.active) button[type="submit"]', function(event) {
		event.preventDefault();
		var $form = $(this).closest('form'),
			$input = $form.find('input');
		$form.addClass('active');
		$input.focus();
	});
	// ONLY FOR DEMO // Please use $('form').submit(function(event)) to track from submission
	// if your form is ajax remember to call `closeSearch()` to close the search container
	$(document).on('click', '.navbar-coll form[role="search"].active button[type="submit"]', function(event) {
		event.preventDefault();
		var $form = $(this).closest('form'),
			$input = $form.find('input');
		$('#showSearchTerm').text($input.val());
        closeSearch()
	});
});

// showing the product popup
function openProductPopup(name ,price ,obj){
	popDiv = $('.modal.fade.pop-up-1');
	
	popDivhd = $(popDiv).find('#prod_cat');
	$(popDivhd).html(name);

	popDivPrice = $(popDiv).find('#prod_price');
	$(popDivPrice).html('Артикул ' +price);
	
	imageHtml = $(obj).html()

	popImgDiv = $(popDiv).find(".modal-main").find('.col-sm-6:first');
	$(popImgDiv).html("");
	$(popImgDiv).html(imageHtml)
}
// showing the aythentication popup
function openAuthPopup(attach_id,obj){
	var url = attach_id;
	popDiv = $('.modal.fade.pop-up-2');
	popUrl = $(popDiv).find('#url');
	$(popUrl).val(url);
}
$(document).ready(function() {
    $("#hide").click(function() {
        $(".navbar-brand").removeClass("hidden-xs");
        $(".search-box").css("display", "none");
        $("#hide").css("display", "none");
        $("#show").css("display", "block");

    });
    $("#show").click(function() {
        $(".navbar-brand").addClass("hidden-xs");
        $(".search-box").css("display", "block");
        $("#hide").css("display", "block");
    });
});

$(document).ready(function() {
    $(".search-btn").click(function() {
        $(this).hide();
    });
    randomnum();
    randomNumContact();
    $("#comment").submit(function(){
		return checkCaptcha();
	});
    $("#contact_form1").submit(function(){
		return checkCaptcha();
	});
    $("#contact_form").submit(function(){
		return checkCaptchaforContact();
	});
	$("#authentication_form").submit(function(){
		 $('#form_popup').modal('hide');
		return true
	});
	
	// Change map coordinate according to the address
	// $("#firstAddress").click(function(){
	// 	firstAddr = new ymaps.Placemark([55.34, 37.91], {
	// 		hintContent: 'derevnya Zhitnevo',
	// 		balloonContent: 'derevnya Zhitnevo'
	//     });
	// 	thirdMap.geoObjects.add(firstAddr);
	// });
	// $("#secondAddress").click(function(){
	// 	secondAddr = new ymaps.Placemark([55.34, 37.91], {
	// 		hintContent: 'derevnya Zhitnevo',
	// 		balloonContent: 'derevnya Zhitnevo'
	//     });
	// 	thirdMap.geoObjects.add(secondAddr);
	// });
	// $("#thirdAddress").click(function(){
	// 	thirdAddr = new ymaps.Placemark([55.34, 37.91], {
	// 		hintContent: 'derevnya Zhitnevo',
	// 		balloonContent: 'derevnya Zhitnevo'
	//     });
	// 	thirdMap.geoObjects.add(thirdAddr);
	// });
	// $("#fourthAddress").click(function(){
	// 	fourthAddr = new ymaps.Placemark([55.34, 37.91], {
	// 		hintContent: 'derevnya Zhitnevo',
	// 		balloonContent: 'derevnya Zhitnevo'
	//     });
	// 	thirdMap.geoObjects.add(fourthAddr);
	// });
});
window.onload = function() {
	try {
		TagCanvas.Start('myCanvas', 'tags', {
			shape: 'vcylinder',
			textColour: '#001f5d',
			outlineColour: '#001f5d',
			depth: 0.8,
			maxSpeed: 0.05
		});
	} catch (e) {
		// something went wrong, hide the canvas container
		document.getElementById('myCanvasContainer').style.display = 'none';
	}
};
function randomnum(){
	var number1 = 5;
	var number2 = 50;
	
	var randomnum = (parseInt(number2) - parseInt(number1)) + 1;
	var rand1 = Math.floor(Math.random()*randomnum)+parseInt(number1);
	var rand2 = Math.floor(Math.random()*randomnum)+parseInt(number1);
	
	$("#num1").html(rand1);
	$("#num2").html(rand2);
}
function checkCaptcha(){
	var total=parseInt($('#num1').html())+parseInt($('#num2').html());
	var total1=$('#total').val();
	if(total!=total1){		
		randomnum();
		return false;
	}
	else{
		return true;
	}
}
function randomNumContact(){
	var number1 = 5;
	var number2 = 50;
	
	var randomnum = (parseInt(number2) - parseInt(number1)) + 1;
	var rand1 = Math.floor(Math.random()*randomnum)+parseInt(number1);
	var rand2 = Math.floor(Math.random()*randomnum)+parseInt(number1);
	
	$("#cnum1").html(rand1);
	$("#cnum2").html(rand2);
}
function checkCaptchaforContact(){
	var total=parseInt($('#cnum1').html())+parseInt($('#cnum2').html());
	var total1=$('#ctotal').val();
	if(total!=total1){		
		randomNumContact();
		return false;
	}
	else{
		return true;
	}
}

// Js for Maps
ymaps.ready(init);
var firstMap, secondMap, thirdMap, 
    firstMapPlace, secondMapPlace, thirdMapPlace;

function init(){
	// first Map
	firstMap = new ymaps.Map("firstMap", {
        center: [55.710058, 37.686293],
        zoom: 15
    }); 
    
    firstMapPlace = new ymaps.Placemark([55.710058, 37.686293], {
        //hintContent: 'Moscow!',
        //balloonContent: 'Capital of Russia'
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });

    firstMap.geoObjects.add(firstMapPlace);
    
    // Second Map
    
    secondMap = new ymaps.Map("secondMap", {
        center: [55.710058, 37.686293],
        zoom: 15
    }); 
    
    secondMapPlace = new ymaps.Placemark([55.710058, 37.686293], {
        //hintContent: 'Moscow!',
        //balloonContent: 'Capital of Russia'
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });
    secondMap.geoObjects.add(secondMapPlace);
    
    // Third Map
    
    thirdMap = new ymaps.Map("thirdMap", {
        center: [56, 48],
        zoom: 5
    }); 
    
    thirdMapPlace = new ymaps.Placemark([55.341567, 37.916729], {
        //hintContent: 'Moscow!',
        //balloonContent: 'Capital of Russia'
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });    
    thirdMapPlace2 = new ymaps.Placemark([56.696624, 60.876788], {
        //hintContent: 'Moscow!',
        //balloonContent: 'Capital of Russia'
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });    
    thirdMapPlace3 = new ymaps.Placemark([54.346932, 48.606618], {
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });    
    thirdMapPlace4 = new ymaps.Placemark([55.194136, 61.418678], {
    }, {
    	iconLayout: 'default#image',
        iconImageHref: '/theme_aditim/static/src/images/map_sign.png',
        iconImageSize: [47, 53],
        iconImageOffset: [0, -53],

    });

    thirdMap.geoObjects.add(thirdMapPlace);
    thirdMap.geoObjects.add(thirdMapPlace2);
    thirdMap.geoObjects.add(thirdMapPlace3);
    thirdMap.geoObjects.add(thirdMapPlace4);
}
jQuery(document).ready(function(){
	$(".cont-bott ul li a#firstAddress").click(function(){
	    thirdMap.setCenter([55.341567, 37.916729]);
	    thirdMap.setZoom(15);
	});

	$(".cont-bott ul li a#secondAddress").click(function(){
	    thirdMap.setCenter([56.696624, 60.876788]);
	    thirdMap.setZoom(15);
	});

	$(".cont-bott ul li a#thirdAddress").click(function(){
	    thirdMap.setCenter([54.346932, 48.606618]);
	    thirdMap.setZoom(15);
	});

	$(".cont-bott ul li a#fourthAddress").click(function(){
	    thirdMap.setCenter([55.194136, 61.418678]);
	    thirdMap.setZoom(15);
	});
});
/********************* 
****uWorld team*******
*********************/

/*! Copyright (c) 2011 Brandon Aaron (http://brandonaaron.net)
 * Licensed under the MIT License (LICENSE.txt).
 *
 * Thanks to: http://adomas.org/javascript-mouse-wheel/ for some pointers.
 * Thanks to: Mathias Bank(http://www.mathias-bank.de) for a scope bug fix.
 * Thanks to: Seamus Leahy for adding deltaX and deltaY
 *
 * Version: 3.0.6
 * 
 * Requires: 1.2.2+
 */
(function(a){function d(b){var c=b||window.event,d=[].slice.call(arguments,1),e=0,f=!0,g=0,h=0;return b=a.event.fix(c),b.type="mousewheel",c.wheelDelta&&(e=c.wheelDelta/120),c.detail&&(e=-c.detail/3),h=e,c.axis!==undefined&&c.axis===c.HORIZONTAL_AXIS&&(h=0,g=-1*e),c.wheelDeltaY!==undefined&&(h=c.wheelDeltaY/120),c.wheelDeltaX!==undefined&&(g=-1*c.wheelDeltaX/120),d.unshift(b,e,g,h),(a.event.dispatch||a.event.handle).apply(this,d)}var b=["DOMMouseScroll","mousewheel"];if(a.event.fixHooks)for(var c=b.length;c;)a.event.fixHooks[b[--c]]=a.event.mouseHooks;a.event.special.mousewheel={setup:function(){if(this.addEventListener)for(var a=b.length;a;)this.addEventListener(b[--a],d,!1);else this.onmousewheel=d},teardown:function(){if(this.removeEventListener)for(var a=b.length;a;)this.removeEventListener(b[--a],d,!1);else this.onmousewheel=null}},a.fn.extend({mousewheel:function(a){return a?this.bind("mousewheel",a):this.trigger("mousewheel")},unmousewheel:function(a){return this.unbind("mousewheel",a)}})})(jQuery)

/**
 * jquery.simplr.smoothscroll
 * version 1.0
 * copyright (c) 2012 https://github.com/simov/simplr-smoothscroll
 * licensed under MIT
 * requires jquery.mousewheel - https://github.com/brandonaaron/jquery-mousewheel/
 */

;(function ($) {
  'use strict'
  
  $.srSmoothscroll = function (options) {
  
    var self = $.extend({
      step: 55,
      speed: 400,
      ease: 'swing',
      target: $('body'),
      container: $(window)
    }, options || {})

    // private fields & init
    var container = self.container
      , top = 0
      , step = self.step
      , viewport = container.height()
      , wheel = false

    var target
    if (self.target.selector == 'body') {
      target = (navigator.userAgent.indexOf('AppleWebKit') !== -1) ? self.target : $('html')
    } else {
      target = container
    }

    // events
    self.target.mousewheel(function (event, delta) {

      wheel = true

      if (delta < 0) // down
        top = (top+viewport) >= self.target.outerHeight(true) ? top : top+=step

      else // up
        top = top <= 0 ? 0 : top-=step

      target.stop().animate({scrollTop: top}, self.speed, self.ease, function () {
        wheel = false
      })

      return false
    })

    container
      .on('resize', function (e) {
        viewport = container.height()
      })
      .on('scroll', function (e) {
        if (!wheel)
          top = container.scrollTop()
      })
  
  }
})(jQuery);

$(function () {
  $.srSmoothscroll()
});