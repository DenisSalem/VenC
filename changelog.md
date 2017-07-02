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
	DONE | Notify when found invalid entry filename in entries folder
	DONE | Remove CSS field from entry
	DONE | Catch exception when Yaml canno't parse blog configuration.
	WIP  | No more awkward silence when something is successfully done.
	WIP  | Add more coloration for message!
	WIP  | Speed up blog exportation
	WIP  | Massive refactorisation, code cleaning and optimisation.
	WIP  | Change nomenclature: entry_name -> title. Fix doc.
	WIP  | Change nomenclature: remove underscore from blog_configuration, using camelCase instead. Fix doc.
	TODO | Auto include CSS
	TODO | Warn about missing mandatory field in entry.
	TODO | Add function GetIfExist.
	TODO | Add function Include.
	TODO | Fix vertical scroll bar in code snippet.
	TODO | Reorganize themes dependencies in setup.
	TODO | Clean up installation
	TODO | Client-side search engine.
	TODO | Add translation for Deutsch and Spanish
