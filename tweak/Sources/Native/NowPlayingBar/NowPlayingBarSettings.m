#import "Core/SGL10n.h"
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "NowPlayingBar.h"

UIViewController *SGNowPlayingBarSettingsPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Now playing bar") intro:SGRestartNote sections:@[
        SGSection(nil, @[
            SGHideRow(SGT(@"Hide the device button"), nil, SGHideBarConnect),
        ]),
        SGSection(@"Spotify's flags", @[
            SGFlagRow(SGT(@"Two lines of track info"), @"ios-feature-nowplayingbar.two_lines_information_unit"),
            SGFlagRow(SGT(@"Save button"), @"ios-feature-nowplayingbar.add_button"),
            SGFlagRow(SGT(@"Queue badge"), @"ios-feature-nowplayingbar.queue_badge"),
            SGFlagRow(SGT(@"Hold and drag to resize"), @"ios-feature-nowplayingbar.hold_and_drag_to_resize"),
            SGFlagRow(SGT(@"Video in the mini player"), @"ios-feature-nowplaying.video_in_miniplayer"),
            SGFlagRow(SGT(@"Bar to cover art animation"), @"ios-feature-nowplaying.bartocoverart_animation_enabled"),
            SGFlagRow(SGT(@"Mini player transition animations"), @"ios-feature-nowplaying.miniplayer_transition_animations"),
        ]),
    ] footer:nil];
}
