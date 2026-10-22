#import "Core/SGL10n.h"
// The native player's settings: Spotify's own player screen and the parts of it to hide, and the queue
// and devices flags. The Player page that holds them is App/Pages.m's.
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "NowPlaying.h"

NSArray<SGModSection *> *SGNativePlayerScreenSections(void) {
    return @[
        SGSection(SGT(@"Player screen"), @[
            SGOptionRow(SGT(@"Artwork background"), nil, SGKeyPlayerBackdrop),
            SGOptionRow(@"Glass header buttons", nil, SGKeyPlayer),
            SGKillRow(@"Disable Canvas", @"ios-feature-canvas.canvas_enabled"),
            SGFlagRow(@"Sheet style player", @"ios-feature-nowplaying.sheet_style_npv"),
            SGFlagRow(@"Redesigned header", @"ios-feature-nowplaying.new_redesign_header_with_context_menu_enabled"),
            SGFlagRow(@"New progress slider", @"ios-feature-encoreexperiments.new_npv_slider_enabled"),
            SGFlagRow(@"Expand the sticky header on tap", @"ios-feature-nowplaying.expand_sticky_header_on_tap"),
        ]),
        SGSection(@"Hide cards below the player", @[
            SGHideRow(SGT(@"Lyrics"), nil, SGHideLyricsCard),
            SGHideRow(@"About the artist", nil, SGHideAboutArtist),
            SGHideRow(SGT(@"Related videos"), nil, SGHideRelatedVideos),
            SGHideRow(@"SongDNA", nil, SGHideSongDNA),
            SGHideRow(@"Live events", nil, SGHideLiveEvents),
            SGHideRow(SGT(@"Explore the artist"), nil, SGHideExploreArtist),
            SGHideRow(@"Credits", nil, SGHideCredits),
            SGHideRow(SGT(@"Merch"), nil, SGHideMerch),
            SGHideRow(SGT(@"Recommendations"), nil, SGHideRecommendations),
        ]),
        SGSection(SGT(@"Hide on the player"), @[
            SGHideRow(SGT(@"Lyrics preview"), nil, SGHideLyricsInline),
            SGHideRow(SGT(@"Shuffle"), nil, SGHideShuffle),
            SGHideRow(SGT(@"Repeat"), nil, SGHideRepeat),
            SGHideRow(SGT(@"Add to playlist"), nil, SGHideAddTo),
            SGHideRow(SGT(@"Queue"), nil, SGHideQueue),
            SGHideRow(SGT(@"Share"), nil, SGHideShare),
            SGHideRow(SGT(@"Connect to a device"), nil, SGHideConnect),
        ]),
    ];
}

SGModRow *SGGlassLyricsRow(void) {
    return SGOptionRow(SGT(@"Glass lyrics"), nil, SGKeyLyricsCard);
}

UIViewController *SGQueueSettingsPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Queue & devices") intro:SGRestartNote sections:@[
        SGSection(SGT(@"Bottom sheets"), @[
            SGFlagRow(SGT(@"Queue as a bottom sheet"), @"ios-feature-nowplaying.bottom_sheet_queue_enabled"),
            SGFlagRow(SGT(@"Connect as a bottom sheet"), @"ios-feature-nowplaying-elements.enable_connect_bottom_sheet"),
            SGFlagRow(@"Connect sheet from the video switcher", @"ios-playbackcontrol-audiovideoswitcher-impl.enable_connect_bottom_sheet"),
        ]),
        SGSection(SGT(@"Queue"), @[
            SGFlagRow(SGT(@"Queue flip transition"), @"ios-feature-nowplaying.queue_flip_transition_enabled"),
            SGFlagRow(SGT(@"Play next in the context menu"), @"ios-feature-queue.is_play_next_context_menu_enabled"),
        ]),
    ] footer:nil];
}
