// Vitrine-owned UI localization only. No Spotify SDK UI swizzles.
#import <Foundation/Foundation.h>
FOUNDATION_EXPORT NSString *SGT(NSString *english);

// Vitrine picker display names only; selectors, models, device IDs and stored settings remain raw.
FOUNDATION_EXPORT NSString *SGZHFontDisplayName(NSString *name);
FOUNDATION_EXPORT NSString *SGZHIconDisplayName(NSString *name, BOOL symbols);
FOUNDATION_EXPORT NSString *SGZHAutoEqCatalogDisplayName(NSString *name);
FOUNDATION_EXPORT NSString *SGZHAutoEqSourceDisplayName(NSString *source);
