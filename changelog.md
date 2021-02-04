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
    DONE | Prevent Infinite scroll to block when ressource isn't available.
    DONE | Rewrite pattern processor unit tests.
    DONE | fix FAQ latex2mathml is incomplete.
    DONE | fix FAQ categories separator is ' > ', not '>'
    DONE | fix FAQ subfolders must not start with '/'
    DONE | fix FAQ https://stackoverflow.com/questions/14547631/python-locale-error-unsupported-locale-setting.
    DONE | Refactor DatesThread to ArchivesThread.
    DONE | Fix Shabang issue for compatibility.
    DONE | Semantic-web features.
    DONE | Theme must have it's own yaml configuration.
    DONE | Fix pattern processing within included file.
    DONE | Add ForEntryMetadata
    DONE | Add ForEntryRange
    DONE | Add IfChapters and use it in academik to hide/show chapters navigation.
    DONE | Fix and clean Tessellation theme.
    DONE | Add IfInMainThread pattern.
    DONE | Make entry URL nicer when filename is index.html and has subfolder.
    DONE | Fix url with special char in chapter.
    DONE | Add CodeHighlightInclude
    DONE | Reorganize themes dependencies in setup.
    DONE | Print out what's going on while FTP transfert.
    WIP  | Add relevant templates for themes.
    WIP  | Client-side search engine.
    WIP  | Add definition in documentation for optional fields in blog configuration.
    WIP  | Change nomenclature: Most of the usual patterns are changed. Fix doc.
    DONE | Documenter le type des métadonnées: list, str ou dict
    DONE | Fix chapters rendering (only first level sub-chapter were rendered)
    
# version 2.1.x
    TODO | Override theme config override.
    TODO | venc -xb should also work in subdirectories
    TODO | Replace aside element by nav
    TODO | Improve context / ressource naming for error management
    TODO | Because of fully recursive pattern, some contextual variable are now useless, like {relative_origin}
    TODO | SetBackgroundColor for text
    TODO | Include threads preview in entry
    TODO | Add command for reorder entries by criteria
    TODO | Use built in list in yaml instead to turn str to list.
    TODO | Allow markdown2 setup.
    TODO | Add --insert-chapter command.
    TODO | Warn about metadata that should be list but are str.
    TODO | Add folder for blog_configuration, with multiple configuration file (for splitting the actual one).
    TODO | Automatically merge all known entry authors into blog authors.
    TODO | Force preview / full content in thread, for single entry.
    TODO | If previous theme empty, juste remove it.
    TODO | Add plural form at the end of blog creation if multiple blog has been made.
    TODO | Fix gvim / -ex.
    TODO | Fix encoding issue in JSON-LD document.
    TODO | Catch "OSError: [Errno 98] Address already in use".
    TODO | Catch invalid encoding at startup. (???)
    TODO | Create entry with default template, if defined.
    TODO | Make some dependencies optional.
    TODO | Split themes from main branch.
    TODO | Add translation for Deutsch and Spanish.
    TODO | Add ForMetadata, ForMetadataIfExists.
    TODO | Add docutils reStructuredText parser settings override.
    TODO | Decrease halt_level to render reStructuredText even if errors occurs.
    TODO | Access {count} and {weight} from LeavesForEntrycategories.
    TODO | Add Yaml comments in blog configuration.
    TODO | Add nice 404 errors page.
    TODO | Warn about entry title duplicates.
    TODO | Handle missing args in case of unknown number of args (Pattern).
    TODO | Add configuration field type check.
    TODO | Optimize modules importation.
    TODO | Concatenate user defined blog keywords with entries keywords.
    TODO | Add more informations into JSON-LD document.
    TODO | Optimize and refine JSON-LD processing.
    TODO | Embed as much as possible microdata/JSON-LD into blog.
    TODO | Improve sub folder management in Entry and EntriesThread.
    TODO | Optimize objects dereferencing.
    TODO | Add draft support.
    TODO | Add CPU threads support.
    TODO | Enhance FTP transfert with multiple connections.
    TODO | Regenerate any missing folders.
    TODO | Override server port with extra arg.
    TODO | Try to install an up to date oembed providers from https://oembed.com/providers.json with pip
	
# version 3.x.x
    TODO | Replace categories with taxonomy support.
    TODO | Add support for plugin.
    TODO | Add Incremental blog update.
    TODO | Add support for sub-sites within main site.
    TODO | Add support for single pages.
