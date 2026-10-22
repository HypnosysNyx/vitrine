#import "Core/SGL10n.h"
// The redesign's Artists page: Apple Music's logo in place of the name on an artist's page, and what the redesign
// takes off the page.
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "Artist.h"

UIViewController *SGRArtistSettingsPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Artists") intro:SGRestartNote sections:@[
        SGNotedSection(@"Apple Music", @[
            SGSwitchRow(@"Artist logos", @"In place of the name on an artist's page", SGRKeyArtistLogo),
        ], @"Only the artist's name is sent to Apple Music."),
        SGSection(SGT(@"Hide on an artist's page"), @[
            SGSwitchRow(SGT(@"Videos"), @"In the Music list, and in the Video tab", SGRKeyArtistHideVideos),
            SGSwitchRow(SGT(@"Music, Video and Merch tabs"), @"Without them the Music list is the page", SGRKeyArtistHideTabs),
            SGHideRow(SGT(@"Artist pick"), nil, SGRKeyArtistHidePick),
            SGHideRow(SGT(@"Release countdown"), @"The pre-save of an upcoming release", SGRKeyArtistHideCountdown),
            SGHideRow(SGT(@"About"), nil, SGRKeyArtistHideAbout),
        ]),
    ] footer:nil];
}
