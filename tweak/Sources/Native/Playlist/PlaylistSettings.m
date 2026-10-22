#import "Core/SGL10n.h"
#import "Settings/SGModPage.h"
#import "Playlist.h"

UIViewController *SGPlaylistSettingsPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Playlists") intro:nil sections:@[
        SGSection(SGT(@"Header"), @[
            SGOptionRow(SGT(@"Artwork background"), nil, SGKeyPlaylistBackdrop),
        ]),
        SGSection(@"Hide in the playlist header", @[
            SGHideRow(SGT(@"Cover artwork"), nil, SGHidePlaylistArtwork),
            SGHideRow(SGT(@"Description"), nil, SGHidePlaylistDescription),
            SGHideRow(SGT(@"Creator and collaborators"), nil, SGHidePlaylistCreator),
            SGHideRow(SGT(@"Length and saves"), nil, SGHidePlaylistLength),
        ]),
        SGSection(SGT(@"Hide playlist buttons"), @[
            SGHideRow(@"Video", nil, SGHidePlaylistVideo),
            SGHideRow(SGT(@"Add to library"), nil, SGHidePlaylistAddTo),
            SGHideRow(SGT(@"Download"), nil, SGHidePlaylistDownload),
            SGHideRow(SGT(@"Share"), nil, SGHidePlaylistShare),
            SGHideRow(SGT(@"More"), nil, SGHidePlaylistMore),
        ]),
        SGSection(SGT(@"Hide above the tracks"), @[
            SGHideRow(@"Curation pills", nil, SGHidePlaylistPills),
            SGHideRow(@"Find and sort bar", nil, SGHidePlaylistFind),
        ]),
    ] footer:nil];
}
