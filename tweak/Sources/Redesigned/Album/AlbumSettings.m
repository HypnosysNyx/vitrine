#import "Core/SGL10n.h"
// The redesign's Albums page: Apple Music's animated covers on album pages, whether their downloads run in Low
// Data Mode, and what the redesign takes off the page.
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "Shared/AnimatedArtwork/AnimatedArtwork.h"
#import "Album.h"

UIViewController *SGRAlbumSettingsPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Albums") intro:SGRestartNote sections:@[
        SGNotedSection(@"Apple Music", @[
            SGSwitchRow(SGT(@"Animated covers"), @"At the top of an album that has one, about 5 MB each", SGRKeyAlbumMotion),
            SGOptionRow(SGT(@"Download in Low Data Mode"), nil, SGKeyMotionLowData),
        ], @"Only the album's name is sent to Apple Music. A cover stays still in Low Power Mode."),
        SGSection(SGT(@"Hide on an album's page"), @[
            SGSwitchRow(SGT(@"Repeated track artists"), @"The artist under a track when it is the album's own", SGRKeyAlbumHideTrackArtists),
        ]),
        SGNotedSection(SGT(@"Hide under an album's tracks"), @[
            SGSwitchRow(SGT(@"More by the artist"), nil, SGRKeyAlbumHideMoreBy),
            SGSwitchRow(SGT(@"Related music videos"), nil, SGRKeyAlbumHideVideos),
            SGSwitchRow(SGT(@"Concerts"), nil, SGRKeyAlbumHideConcerts),
            SGSwitchRow(SGT(@"Merch"), nil, SGRKeyAlbumHideMerch),
            SGSwitchRow(SGT(@"You might also like"), nil, SGRKeyAlbumHideYouMightLike),
            SGSwitchRow(SGT(@"Everything else"), @"Any other section Spotify sends", SGRKeyAlbumHideOther),
        ], @"Sections are told apart by their English names. With Spotify in another language, Everything else "
           @"covers them all."),
    ] footer:nil];
}
