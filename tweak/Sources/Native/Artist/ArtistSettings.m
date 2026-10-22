#import "Core/SGL10n.h"
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "Artist.h"

UIViewController *SGArtistSettingsPage(void) {
    NSArray<SGModSection *> *sections = @[
        SGSection(SGT(@"Photo"), @[
            SGOptionRow(SGT(@"Fade into a blur"), nil, SGKeyArtistPhotoFade),
        ]),
        SGSection(SGT(@"Hide in the header"), @[
            SGHideRow(SGT(@"Explore (video deck)"), nil, SGHideArtistExplore),
            SGHideRow(SGT(@"Follow"), nil, SGHideArtistFollow),
            SGHideRow(SGT(@"More options"), nil, SGHideArtistMore),
            SGHideRow(SGT(@"Shuffle"), nil, SGHideArtistShuffle),
            SGHideRow(SGT(@"Verified badge"), nil, SGHideArtistVerified),
            SGHideRow(SGT(@"Monthly listeners"), nil, SGHideArtistListeners),
        ]),
        SGSection(SGT(@"Tabs"), @[
            SGHideRow(@"Hide the tab bar", nil, SGHideArtistTabBar),
        ]),
        SGNotedSection(SGT(@"Hide on the page"), @[
            SGHideRow(SGT(@"Songs you liked"), nil, SGHideArtistLikedSongs),
            SGHideRow(SGT(@"Popular"), nil, SGHideArtistPopular),
            SGHideRow(SGT(@"Artist pick"), nil, SGHideArtistPick),
            SGHideRow(SGT(@"Popular releases"), nil, SGHideArtistReleases),
            SGHideRow(SGT(@"Featuring"), nil, SGHideArtistFeaturing),
            SGHideRow(SGT(@"Music videos"), nil, SGHideArtistVideos),
            SGHideRow(SGT(@"About"), nil, SGHideArtistAbout),
            SGHideRow(SGT(@"Artist playlists"), nil, SGHideArtistPlaylists),
            SGHideRow(SGT(@"Fans also like"), nil, SGHideArtistFansAlsoLike),
            SGHideRow(SGT(@"Appears on"), nil, SGHideArtistAppearsOn),
            SGHideRow(SGT(@"Discovered on"), nil, SGHideArtistDiscoveredOn),
        ], @"Works only with Spotify in English."),
        SGSection(@"Spotify's own", @[
            SGFlagRow(@"Share button in the header", @"ios-creator-impl.share_in_action_row_enabled_artist"),
            SGFlagRow(@"More options in the navigation bar", @"ios-creator-impl.context_menu_in_navigation_bar_enabled_artist"),
            SGFlagRow(SGT(@"Top collaborators"), @"ios-creator-impl.is_top_collaborators_enabled"),
            SGFlagRow(SGT(@"Artist facts"), @"ios-creator-impl.is_artist_facts_enabled"),
        ]),
    ];
    return [[SGModPage alloc] initWithTitle:SGT(@"Artist") intro:nil sections:sections footer:nil];
}
