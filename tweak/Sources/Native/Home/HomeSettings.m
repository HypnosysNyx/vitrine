#import "Core/SGL10n.h"
#import "Core/SGCore.h"
#import "Settings/SGModPage.h"
#import "Home.h"
#import "Native/Playlist/Playlist.h"
#import "Native/Artist/Artist.h"
#import "Native/Album/Album.h"

static SGModRow *choiceRow(NSString *title, NSString *subtitle, SGHomeChoice choice) {
    return SGChoiceRow(title, subtitle, SGHomeChoiceKey(choice), SGHomeChoiceNames(choice),
                       SGHomeChoiceDefault(choice));
}

UIViewController *SGHomeGradientPage(void) {
    return [[SGModPage alloc] initWithTitle:@"Gradient"
                                      intro:@"Turning it on or off applies after you restart Spotify."
                                   sections:@[
        SGSection(@"Gradient", @[
            SGOptionRow(@"Show", nil, SGKeyHomeGradient),
            choiceRow(@"Color", nil, SGHomeChoiceTint),
            choiceRow(@"Strength", nil, SGHomeChoiceStrength),
            choiceRow(@"Height", nil, SGHomeChoiceHeight),
        ]),
    ] footer:nil];
}

static UIViewController *libraryPage(void) {
    return [[SGModPage alloc] initWithTitle:SGT(@"Library") intro:nil sections:@[
        SGSection(SGT(@"Library"), @[
            SGFlagRow(SGT(@"Denser rows"), @"ios-feature-yourlibaryx.denser_rows_enabled"),
            SGFlagRow(SGT(@"Sort playlists by recently updated"), @"ios-feature-yourlibaryx.recently_updated_playlists_sort_enabled"),
            SGFlagRow(SGT(@"Sort artists by recently updated"), @"ios-feature-yourlibaryx.recently_updated_artists_sort_enabled"),
            SGFlagRow(SGT(@"Recents"), @"ios-feature-yourlibaryx.recents_enabled"),
            SGFlagRow(SGT(@"Recents sort order"), @"ios-feature-yourlibaryx.recents_sort_order_enabled"),
            SGFlagRow(SGT(@"Library settings"), @"ios-feature-yourlibaryx.library_settings_enabled"),
            SGFlagRow(SGT(@"Library Pro"), @"ios-feature-yourlibaryx.your_library_pro_enabled"),
        ]),
    ] footer:nil];
}

UIViewController *SGHomeSettingsPage(void) {
    // The row reads its own state out, so the section says which color is set without being opened.
    SGModRow *gradient = SGPageRow(@"Gradient", ^UIViewController *{ return SGHomeGradientPage(); });
    gradient.value = ^NSString *{
        if (!SGFlag(SGKeyHomeGradient, NO)) return @"Off";
        return SGHomeChoiceNames(SGHomeChoiceTint)[(NSUInteger)SGHomeChoiceValue(SGHomeChoiceTint)];
    };

    NSArray<SGModSection *> *sections = @[
        SGSection(nil, @[
            SGWithSymbol(SGPageRow(SGT(@"Playlists"), ^UIViewController *{ return SGPlaylistSettingsPage(); }), @"music.note.list"),
            SGWithSymbol(SGPageRow(SGT(@"Library"), ^UIViewController *{ return libraryPage(); }), @"books.vertical"),
            SGWithSymbol(SGPageRow(SGT(@"Album"), ^UIViewController *{ return SGAlbumSettingsPage(); }), @"square.stack"),
            SGWithSymbol(SGPageRow(SGT(@"Artist"), ^UIViewController *{ return SGArtistSettingsPage(); }), @"music.mic"),
        ]),
        SGSection(SGT(@"Home"), @[
            SGWithSymbol(gradient, @"rectangle.tophalf.inset.filled"),
            SGFlagRow(SGT(@"Pull to refresh"), @"ios-home-evopage-impl.pull_to_refresh_enabled"),
        ]),
        SGSection(SGT(@"Hide on Home"), @[
            SGHideRow(SGT(@"Filter pills"), nil, SGHideHomePills),
            SGHideRow(SGT(@"Shortcuts grid"), nil, SGHideHomeShortcuts),
            SGHideRow(SGT(@"Promo cards"), nil, SGHideHomePromo),
            SGHideRow(SGT(@"Preview cards"), nil, SGHideHomePreviews),
            SGHideRow(SGT(@"DJ card"), nil, SGHideHomeDJ),
            SGKillRow(SGT(@"DJ button"), @"ios-home-evopage-impl.idj_show_dj_button"),
            SGKillRow(SGT(@"DJ beta badge"), @"ios-home-evopage-impl.dj_mdc_beta_badge_enabled"),
        ]),
    ];
    return [[SGModPage alloc] initWithTitle:SGT(@"Home & Library") intro:nil sections:sections footer:nil];
}
