'use strict';

$(function () {
    var D2L_NEXT_BUTTON_SELECTOR = '.d2l-iterator-button-next, .mobile_next',
        D2L_PREV_BUTTON_SELECTOR = '.d2l-iterator-button-prev, .mobile_prev',
        D2L_POPUP_NAV_SELECTOR = '#d2l-popup-nav',
        HIDDEN_CLASS = 'd2l-hidden',
        DISABLED_BUTTON_CLASS = 'd2l-button-disabled';

    D2LnavHost.init(overrideNavigation);

    function overrideNavigation(data) {
        var $next = $(D2L_NEXT_BUTTON_SELECTOR),
            $prev = $(D2L_PREV_BUTTON_SELECTOR);

        // the buttons will always do the same thing, sending a message to the child window;
        // if the child window has no link for that action, the button will do nothing
        D2LnavHost.override($next, 'next');
        D2LnavHost.override($prev, 'prev');

        if (data.hasNext) {
            enable($next);
        } else {
            disable($next);
        }

        if (data.hasPrev) {
            enable($prev);
        } else {
            disable($prev);
        }

        $(D2L_POPUP_NAV_SELECTOR).removeClass(HIDDEN_CLASS);
    }

    function enable($el) {
        $el.removeClass(DISABLED_BUTTON_CLASS).removeAttr('aria-disabled');
    }

    function disable($el) {
        $el.addClass(DISABLED_BUTTON_CLASS).attr('aria-disabled', true);
    }
});