#import "Core/SGL10n.h"
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "Album.h"

UIViewController *SGAlbumSettingsPage(void) {
    NSArray<SGModSection *> *sections = @[
        SGSection(SGT(@"Header"), @[
            SGOptionRow(SGT(@"Artwork background"), nil, SGKeyAlbumBackdrop),
        ]),
        SGSection(SGT(@"Hide in the header"), @[
            SGHideRow(SGT(@"Explore (video deck)"), nil, SGHideAlbumExplore),
            SGHideRow(SGT(@"Add to library"), nil, SGHideAlbumAddTo),
            SGHideRow(SGT(@"Download"), nil, SGHideAlbumDownload),
            SGHideRow(SGT(@"More options"), nil, SGHideAlbumMore),
        ]),
        SGNotedSection(SGT(@"Hide on the page"), @[
            SGHideRow(SGT(@"More by the artist"), nil, SGHideAlbumMoreBy),
            SGHideRow(SGT(@"Related music videos"), nil, SGHideAlbumVideos),
            SGHideRow(SGT(@"Concerts"), nil, SGHideAlbumConcerts),
            SGHideRow(SGT(@"Merch"), nil, SGHideAlbumMerch),
            SGHideRow(SGT(@"You might also like"), nil, SGHideAlbumYouMightLike),
        ], @"Works only with Spotify in English."),
    ];
    return [[SGModPage alloc] initWithTitle:SGT(@"Album") intro:nil sections:sections footer:nil];
}
