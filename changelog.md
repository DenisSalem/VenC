# version 1.0.0 Last minute edition :p

	DONE | Copy recursively, if necessary, data from extra.
	DONE | Copy recursively, if necessary data from assets.
	DONE | Copy if necessary data from assets.
	DONE | Export RSS recusively (for each thread and sub category thread).

# version 1.1.0

	DONE | Fix wrong association with entry id and entry filename.
	DONE | Fix wrong dates listing order.
	DONE | Fix categories list input.
	DONE | Fix wrong entries sorting when getting latest ID.
	DONE | Fix wrong relative path when categories are empty.
	DONE | EntryCategoriesTop turns to EntryCategoriesLeafs.
	DONE | Make pattern processor recursive.
	DONE | IfInThread special pattern must act like if/else statement.
	DONE | Notice missing variables in blog_conf.
	DONE | Add command to edit and automatically re-export the blog.
	DONE | Syntax coloration via pygmentize.
	DONE | Must implement weight exploitation for BlogCategoriesLeaf and BlogDates.
	DONE | Must support FTP.

# version 1.1.1

	DONE | Fix entries skipping.
	DONE | Remove BlogCategoriesLeafs.
	DONE | Fix wrong dates sorting.
	DONE | Implement weight exploitation for BlogCategories anf fix mess with RecursiveFor.
	DONE | Sort entries in categories tree.
	DONE | Add verbose when export blog
	DONE | Notice malformed entries.

# version 1.1.2

	DONE | Fix entries from RSS feed order.
	DONE | Add relativeLocation .:Get::RelativeLocation:.
	DONE | Turns EntryCategoriesLeafs to EntryCategoriesLeaves.

# version 1.2.0

	DONE | Fix CodeHighlight and markdown collision.
	DONE | Fix wrong line number with codehighlight.
	DONE | Add more verbose on corrupt Entry. Stop nicely.
	DONE | Fix empty entry creation when passing wrong or none template.
	DONE | Add custom metadata to entries. CSS and doNotUseMarkdown.
	DONE | Add remote copy commande.
	DONE | Make markdown optional.
	DONE | Fix parsing when reading template.
	DONE | Print errors when pattern processor fail.
	DONE | Add -h commande to print reminder
	DONE | Add english language.
	DONE | Clean blog folder on compilation.
	DONE | Fix documentation about .:PagesList:.
	DONE | Fix Entry tags index out of range. 
	DONE | Print ressource and current string when pattern processor fail.
	DONE | Fix infinite scroll : opacity transition and loading image issue. Upgrade the whole plugin :).
	DONE | Fix index_file_name issue: GetPreviousPage and GetNextPage were ignoring blog_configuration.yaml value.
	DONE | GetPrevious and GetNextPage should work outside thread.
	DONE | Optimize I/O stream.
	DONE | Optimize pattern processor to get it twice faster.
	DONE | Installation via pypi.
	DONE | Add some themes.
	DONE | Choose theme to apply while export.
	DONE | Display available themes.
	DONE | Modified default blog_configuration structure, replace url by blog_url.
	DONE | Fix dummy theme.
	DONE | Fix edit-and-export NoneType error.

# version 1.2.1

	DONE | Fix wrong css style name on C++.
	DONE | Fix key errors in templates.
	DONE | Fix wrong parsing with semi-colon on CodeHighlight.
	DONE | Warn about possible missing code highlight CSS.
	DONE | Install theme command.

# version 2.0.0

	DONE | Subprocess call catch exception.
	DONE | Subprocess support args.
	DONE | Remove extra newlines from PrintThemes.
	DONE | Print nicer warnings when found unknown values in chunks.
	DONE | Notify when found invalid entry filename in entries folder.
	DONE | Remove CSS field from entry.
	DONE | Catch exception when Yaml cannot parse blog configuration.
	DONE | Hardcoded opening,closing and separator symbols in pattern processor.
	DONE | Add a copyright notice and term of use in each source files.
	DONE | Warn about missing mandatory field in entry.
	DONE | Add function GetBlogMetadataIfExists and GetEntryMetadataIfExists.
	DONE | Catch exception nicely in CodeHighLight.
	DONE | Catch KeyError exception due to wrong blog path configuration.
	DONE | Moar comments in the code.
	DONE | No more awkward silence when something is successfully done.
	DONE | Add more coloration for message!
	DONE | Specify where error occurs when parsing patterns.
	DONE | More verbosity about wrong pattern arguments.
	DONE | More verbosity about malformed entry.
	DONE | Clear white spaces in error messages.
	DONE | Implement RelativeLocation.
	DONE | Optimisation of categories tree.
	DONE | Code should be a little bit more PEP 8 compliant.
	DONE | Handle currentLocale = locale.getlocale()[0].split('_')[0] AttributeError: 'NoneType'.
	DONE | Clean up installation.
	DONE | Add random number generator.
	DONE | Add function Include. (Add a directory force included ressources)
	DONE | Create theme folder if missing while setup new theme.
	DONE | Auto include CodeHighlight CSS.
	DONE | Add CodeHighlight css override option in blog configuration.
	DONE | Raise error if unknown markup language required.
	DONE | Fix markup language collision AGAIN...
	DONE | Massive refactorisation, code cleaning and optimisation.
	DONE | Fix pattern recursion issue (CodeHighlight).
	DONE | Fix vertical scroll bar in code snippet.
	DONE | Adding Tex math to mathml support (depend on latex2mathml)
	DONE | Add reStructuredText support, remove do_not_use_markdown option.
	DONE | Improve reStructuredText integration with VenC.
	DONE | Quit gracefully when ftp timeout error.
	DONE | add entry preview / full content.
	DONE | Support for video.
	DONE | Support for audio.
	DONE | Optimise entries access with linked list.
	DONE | Add more specific pattern to detect location (IfInCategories,IfInArchives,IfInFirstPage, etc).
	DONE | Fix: Import asset from external theme if necessary.
	DONE | Export empty blog.
	DONE | Allow disabling exportation of specific kind of thread.
	DONE | Add categories tree in entry.
	DONE | Remove illegal character from paths.
	DONE | Add support for embed content (oEmbed).
	DONE | Add custom subfolders.
	DONE | Add GetRootPage.
	DONE | Add SetColor.
	DONE | Split install and blog creation chapter in tutorial.
	DONE | Fix prevent crash from invalid entry id.
	DONE | Support for migration.
	DONE | Catch UnicodeEncodeError.
	DONE | Serv page.
	DONE | Replace python-markdown by markdown2.
	DONE | Replace white spaces in url by dashes.
	DONE | Add support for Atom feed.
	DONE | Add blog generation timestamp.
	DONE | Split unit-test from main branch
      	DONE | Support ForPage in entries thread.
	DONE | Update command help with.
	DONE | Handle ftp encoding error.
	DONE | Sort by metadata.
	DONE | Speed up blog exportation (almost nine times faster!).
	DONE | Escape patterns.
	DONE | Chapters engine.
	DONE | Fix pattern (i.e .:GetEntryTitle:.) access in template's metadata.
	DONE | Infinite scroll use html anchor instead of harcoded indexing.
	WIP  | Prevent Infinite scroll to block when ressource isn't available.
	TODO | Fix unit test.
	TODO | Open with navigator manual.
	TODO | Client-side search engine.
	TODO | Reorganize themes dependencies in setup (adding default templates, scripts, and pages to include).
	TODO | Add relevant templates for themes.
	TODO | fix FAQ https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting.
	WIP  | fix FAQ latex2mathml is incomplete.
	WIP  | fix FAQ categories separator is ' > ', not '>'
	WIP  | fix FAQ subfolders must not start with '/'
	WIP  | Change nomenclature: Most of the usual patterns are changed. Fix doc.

# version 2.x.x
	TODO | Make some dependencies optional.
	TODO | Split themes from main branch
	TODO | Add translation for Deutsch and Spanish.
	TODO | Add ForMetadata, ForMetadataIfExists
	TODO | Add docutils reStructuredText parser settings override.
	TODO | Decrease halt_level to render reStructuredText even if errors occurs.
	TODO | Access {count} and {weight} from LeavesForEntrycategories.
	TODO | Add Yaml comments in blog configuration.
	TODO | Catch invalid encoding at startup.
	TODO | Add nice 404 errors page.
	TODO | Improve Feed.
	TODO | Print out what's going on while FTP transfert.
	TODO | Fix gvim / -ex.
	TODO | run local server as daemon.
	TODO | Warn about entry title duplicates.
