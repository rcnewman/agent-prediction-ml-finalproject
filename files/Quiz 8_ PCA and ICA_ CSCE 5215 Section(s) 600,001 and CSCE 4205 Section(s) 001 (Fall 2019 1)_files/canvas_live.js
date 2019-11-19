////////////////////////////////////////////////////
////////////////////////////////////////////////////
// UNT CLEARAPPS CONTENT OBSERVER                 //
////////////////////////////////////////////////////

var targetNodes = $("#content");
var MutationObserver = window.MutationObserver || window.WebKitMutationObserver;
var myObserver = new MutationObserver (mutationHandler);
var obsConfig = { childList: true, characterData: false, attributes: false, subtree: true };
var contentUpdated = new Event('UNTCLEARcontentUpdated');
var CLEARContentChangesLoaded=false;

targetNodes.each(function () {
    myObserver.observe(this, obsConfig);
});
function mutationHandler (mutationRecords) {
    if (!CLEARContentChangesLoaded) {
        if (targetNodes.find(".user_content").html()!=null) {
            UNTCLEARRunOnContentLoad();
            CLEARContentChangesLoaded=true;
        }
    }
}
function UNTCLEARRunOnContentLoad() {
    UNTCLEARappendCourseInfo();
    UNTCLEARgetResources();
    UNTCLEARLoadWidgets();
}
////////////////////////////////////////////////////
// END UNT CLEARAPPS CONTENT OBSERVER             //
////////////////////////////////////////////////////

////////////////////////////////////////////////////
// UNT CLEARAPPS CANVAS WIDGETS                   //
////////////////////////////////////////////////////

function UNTCLEARLoadWidgets() {

  // SWAP //
  // OUTPUT: hides all child divs except the one selected by value

  // PRESET FIRST SELECTION
  $(document).find(".clear_widget_swap").each(function() {
    $(this).children().eq(0).addClass("clear_widget_show");
  });

  // TRIGGER HANDLER
  $(document).find(".clear_widget_swap").on("CLEARtrigger", function(event, value) {
    $(this).children().removeClass("clear_widget_show");
    $(this).children().eq(parseInt(value)-1).addClass("clear_widget_show");
    $(this).children().eq(parseInt(value)-1).find("video").each(function() {
      $(this).get(0).play();
    });
  });

  // BUTTON //
  // INPUT: send trigger with associated value
  // OUTPUT: highlight selected button

  // PRESET FIRST SELECTION
  $(document).find(".clear_widget_buttonset").each(function() {
    $(this).children().eq(0).addClass("clear_widget_selected");
  });

  // TRIGGER HANDLER
  $(document).find(".clear_widget_buttonset").on("CLEARtrigger", function(event, value) {
    $(this).children().removeClass("clear_widget_selected");
    $(this).children('*[data-value="'+value+'"]').addClass("clear_widget_selected");
  });

  // CLICK EVENT TRIGGER
  $(document).find(".clear_widget_button").on("click", function() {
    thisbutton=$(this);
    targets=thisbutton.data("target").replace(" ","").split(",");
    targets.forEach(function(element) {
      $(document).find("."+element).trigger("CLEARtrigger", thisbutton.data("value"));
    });
  });

  // DROPDOWN //
  // INPUT: send trigger for selection

  // BUILD DROPDOWN
  $(document).find(".clear_widget_select").each(function() {
    $(this).children().each(function() {
      $(this).after('<option value="'+$(this).data("value")+'">'+$(this).html()+'</option>');
      $(this).remove();
    });
    $(this).after('<select class="clear_widget_select" data-target="'+$(this).data("target")+'">'+$(this).html()+'</select>');
    $(this).remove();
  });

  // ON CHANGE
  $(document).find(".clear_widget_select").on("change", function() {
    thisbutton=$(this);
    targets=thisbutton.data("target").replace(" ","").split(",");
    targets.forEach(function(element) {
      $(document).find("."+element).trigger("CLEARtrigger", thisbutton.val());
    });
  });

  // MULTI REQUIREMENT //
  // OUTPUT: hides until all requirements are met

  // PRESET FIRST SELECTION
  $(document).find(".clear_widget_multirequirement").children().each(function() {
    $(this).addClass("clear_widget_null");
  });

  // TRIGGER HANDLER
  $(document).find(".clear_widget_multirequirement").children().on("CLEARtrigger", function(event, value) {
    $(this).parent().removeClass("clear_widget_show");
    $(this).removeClass("clear_widget_valid");
    $(this).removeClass("clear_widget_null");
    if (value!="") {
      if ($(this).data("value")[0]=='!') {
        if ($(this).data("value").substr(1)!=value) $(this).addClass("clear_widget_valid");
      } else {
        if ($(this).data("value")==value) $(this).addClass("clear_widget_valid");
      }
      var correct;
      if ($(this).parent().data("mode")=="any") {
        correct=false;
        $(this).parent().children().each(function() {
          if ($(this).hasClass("clear_widget_valid")) correct=true;
        });
        $(this).parent().children().each(function() {
          if ($(this).hasClass("clear_widget_null")) correct=false;
        });
      } else {
        correct=true;
        $(this).parent().children().each(function() {
          if (!$(this).hasClass("clear_widget_valid")) correct=false;
        });
      }
      if (correct) $(this).parent().addClass("clear_widget_show");
    } else {
      $(this).addClass("clear_widget_null");
    }
  });

};

////////////////////////////////////////////////////
// END UNT CLEARAPPS CANVAS WIDGETS               //
////////////////////////////////////////////////////

////////////////////////////////////////////////////
// UNT CLEARAPPS LINK COURSE INFO APPEND          //
////////////////////////////////////////////////////
function UNTCLEARappendCourseInfo() {
    var $clearappslinks=$('a[href^="https://clearapps.unt.edu"]');
    if ($clearappslinks.size()>0) {
        var courseID=0;
        var courseString=window.location.pathname;
        var courseStringSplit=courseString.split('/');
        if (courseStringSplit.length>=2) courseID=parseInt(courseStringSplit[2]);
        $clearappslinks.each(function() {
            var newHref=$(this).attr("href");
            newHref=newHref.replace("course=INJECTED_COURSE_ID", "course="+courseID);
            $(this).attr("href", newHref);
        });
    }
}
////////////////////////////////////////////////////
// END UNT CLEARAPPS LINK COURSE INFO APPEND      //
////////////////////////////////////////////////////

////////////////////////////////////////////////////
// UNT CLEAR DYNAMIC RESOURCE LOADING             //
////////////////////////////////////////////////////
function UNTCLEARgetResources() {
    $(".UNTCLEARsource").each(function() {
        if (typeof $(this).data("css")!='undefined') {
            $("<link/>", {
                rel: "stylesheet",
                type: "text/css",
                href: "https://clear.unt.edu/apps/lmstools/buildcss.php?css="+$(this).data("css")
            }).appendTo("head");
        }
        if (typeof $(this).data("js")!='undefined') {
            $.getScript("https://clear.unt.edu/apps/lmstools/buildjs.php?js="+$(this).data("js"));
        }
    });
}
////////////////////////////////////////////////////
// END CLEAR DYNAMIC RESOURCE LOADING             //
////////////////////////////////////////////////////

////////////////////////////////////////////////////
// UNT CLEAR UI CUSTOMIZATIONS                    //
////////////////////////////////////////////////////
function UNTCLEARAppendLoginFooter() {
    if ($(document).find('.ic-Login__content').html()!=null || $('#login_form').html()!=null) {
        var loginHTML='<div style="width:100%; background-color:white; text-align:center;">'
        loginHTML+='<div class="content-box" style="background: white; color:black; padding: 12px; max-width:680px; text-align:left; margin: 20px auto; font-size:0.8em">';
        loginHTML+='<div class="grid-row">';
        loginHTML+='<div class="col-xs-12 col-md-6" style="text-align:center">';
        loginHTML+='<h3>Student Helpdesk</h3>';
        loginHTML+='<ul class="fa-ul" style="text-align:left; width:110px; margin:auto">';
        loginHTML+='<li><i class="fa-li fas fa-map-marker-alt"> </i>Sage Hall 330</li>';
        loginHTML+='<li><i class="fa-li fa fa-phone "> </i>(940) 565-2324</li>';
        loginHTML+='<li><i class="fa-li fa fa-envelope "> </i><a href="mailto:helpdesk@unt.edu%20">helpdesk@unt.edu</a></li>';
        loginHTML+='<li><i class="fa-li fas fa-external-link-alt"> </i><a href="https://helpdesk.unt.edu%20">helpdesk.unt.edu</a></li>';
        loginHTML+='</ul>';
        loginHTML+='</div>';
        loginHTML+='<div class="col-xs-12 col-md-6" style="text-align:center">';
        loginHTML+='<h3>Faculty Helpdesk</h3>';
        loginHTML+='<ul class="fa-ul" style="text-align:left; width:110px; margin:auto">';
        loginHTML+='<li><i class="fa-li fas fa-map-marker-alt"> </i>Chilton Hall 112C</li>';
        loginHTML+='<li><i class="fa-li fa fa-phone "> </i>(940) 369-7394</li>';
        loginHTML+='<li><i class="fa-li fa fa-envelope "> </i><a href="mailto:clearhelp@unt.edu%20">clearhelp@unt.edu</a></li>';
        loginHTML+='<li><i class="fa-li fas fa-external-link-alt"> </i><a href="https://clear.unt.edu/services/lms-support">clear.unt.edu/clearhelp</a></li>';
        loginHTML+='</ul>';
        loginHTML+='</div>';
        loginHTML+='<div class="col-xs-12 col-md-12 center-md" style="text-align:center">';
        loginHTML+='<p style="margin-top:20px"><a href="http://www.unt.edu/disclaimer.htm">Disclaimer</a> | <a href="http://www.unt.edu/ada.htm">AA/EOE/ADA</a> | <a href="http://policy.unt.edu/policy-by-number/5">Electronic Accessibility</a> | <a href="https://www.unt.edu/required-links">Required Links</a></p>';
        loginHTML+='<p style="text-align:left;margin-top:-10px">This system is the property of the University of North Texas System and your use of this resource constitutes an agreement to abide by relevant federal and state laws and institutional policies. Unauthorized use of this system is prohibited. Violations can result in penalties and criminal prosecution. Usage may be subject to security testing and monitoring. Users have no expectation of privacy except as otherwise provided by applicable privacy laws. Please see <a href="https://www.untsystem.edu/about-us/policies">https://www.untsystem.edu/about-us/policies</a> for more details.</p>';
        loginHTML+='</div>';
        loginHTML+='<div class="col-xs-12 col-md-12 center-md" style="text-align:center"><a href="http://nc-sara.org" target="_blank "><img src="https://clear.unt.edu/sites/default/files/uploads/nc-sara-mod-b.png" style="width: 158px; height: auto;" /></a></div>';
        loginHTML+='</div>';
        loginHTML+='</div>';
        loginHTML+='</div>';
        if ($('#content').html()!=null) $("#content").after(loginHTML);
        if ($('#f1_container').html()!=null) $("#f1_container").after(loginHTML);
        $('#footer-links .help_dialog_trigger').html('Help');
        $('#footer-links a[href*="facebook.com"]').remove();
        $('#footer-links a[href*="twitter.com"]').remove();
    }
}
$(document).ready(function(){
    var getUrl = window.location;
    var baseUrl = getUrl.protocol + "//" + getUrl.host;
    UNTCLEARAppendLoginFooter();
});
////////////////////////////////////////////////////
// END UNT CLEAR UI CUSTOMIZATIONS                //
////////////////////////////////////////////////////

////////////////////////////////////////////////////
// DESIGN TOOLS CONFIG                            //
////////////////////////////////////////////////////
// Copyright (C) 2017  Utah State University
var DT_variables = {
        iframeID: '',
        // Path to the hosted USU Design Tools
        path: 'https://designtools.ciditools.com/',
        templateCourse: '2782',
        // OPTIONAL: Button will be hidden from view until launched using shortcut keys
        hideButton: true,
         // OPTIONAL: Limit by course format
         limitByFormat: false, // Change to true to limit by format
         // adjust the formats as needed. Format must be set for the course and in this array for tools to load
         formatArray: [
            'online',
            'on-campus',
            'blended'
        ],
        // OPTIONAL: Limit tools loading by users role
        limitByRole: false, // set to true to limit to roles in the roleArray
        // adjust roles as needed
        roleArray: [
            'student',
            'teacher',
            'admin'
        ],
        // OPTIONAL: Limit tools to an array of Canvas user IDs
        limitByUser: false, // Change to true to limit by user
        // add users to array (Canvas user ID not SIS user ID)
        userArray: [
            '1234',
            '987654'
        ]
};
// Run the necessary code when a page loads
$(document).ready(function () {
    'use strict';
    // This runs code that looks at each page and determines what controls to create
    $.getScript(DT_variables.path + 'js/master_controls.js', function () {
        console.log('master_controls.js loaded');
    });
});
////////////////////////////////////////////////////
// END DESIGN TOOLS CONFIG                        //
////////////////////////////////////////////////////
