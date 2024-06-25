/* global notificationUpdateSettings */

/**
 * This script refreshed the notification icon in the top menu
 * on a regular basis so to keep the user apprised about newly arrived
 * notifications without having to reload the page.
 *
 * The refresh rate can be changed via the Django setting NOTIFICATIONS_REFRESH_TIME.
 * See documentation for details.
 */
$(() => {
    'use strict';

    const notificationRefreshTime = notificationUpdateSettings.refreshTime;
    const userNotificationCountViewUrl = notificationUpdateSettings.userNotificationsCountViewUrl;
    const elementNotificationIcon = $('#menu_item_notifications .fa-bell');

    /**
     * Update the notification icon in the top menu
     */
    const updateNotificationIcon = () => {
        fetch(userNotificationCountViewUrl)
            .then((response) => {
                if (response.ok) {
                    return response.json();
                }

                throw new Error('Something went wrong');
            })
            .then((responseJson) => {
                const unreadCount = responseJson.unread_count;

                if (unreadCount > 0) {
                    elementNotificationIcon.addClass('text-danger');
                } else {
                    elementNotificationIcon.removeClass('text-danger');
                }
            })
            .catch((error) => {
                console.log(`Failed to load HTMl to render notifications item. Error: ${error.message}`);
            });
    };

    let myInterval;

    /**
     * Activate automatic refresh every x seconds
     */
    const activateIconUpdate = () => {
        if (notificationRefreshTime > 0) {
            myInterval = setInterval(
                updateNotificationIcon, notificationRefreshTime * 1000
            );
        }
    };

    /**
     * Deactivate automatic refresh
     */
    const deactivateIconUpdate = () => {
        if ((notificationRefreshTime > 0) && (typeof myInterval !== 'undefined')) {
            clearInterval(myInterval);
        }
    };

    /**
     * Refresh only on active browser tabs
     */
    $(window)
        // Tab active
        .focus(() => {
            activateIconUpdate();
        })
        // Tab inactive
        .blur(function() {
            deactivateIconUpdate();
        });

    // Initial start of refreshing on script loading
    activateIconUpdate();
});
