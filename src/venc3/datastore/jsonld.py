#! /usr/bin/env python3

#    Copyright 2016, 2023 Denis Salem
#
#    This file is part of VenC.
#
#    VenC is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    VenC is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with VenC.  If not, see <http://www.gnu.org/licenses/>.

class JSONLD:
    def init_jsonld(self):
        self.enable_jsonld = self.blog_configuration["enable_jsonld"]
        self.enable_jsonp =  self.blog_configuration["enable_jsonp"]
        self.jsonld_required = self.enable_jsonld or self.enable_jsonp

        # Build JSON-LD doc if any
        # TODO
        # ~ if self.enable_jsonld or self.enable_jsonp:
            # ~ if "https://schema.org" in self.blog_configuration.keys():
                # ~ self.optionals_schemadotorg = self.blog_configuration["https://schema.org"]
                
            # ~ else:
                # ~ self.optionals_schemadotorg = {}
            
            # ~ self.entries_as_jsonld = {}
            # ~ self.archives_as_jsonld = {}
            # ~ self.categories_as_jsonld = {}
            # ~ self.root_site_to_jsonld()

        # ~ # Once entries are loaded, build datastore
        # ~ jsonld_callback = self.entry_to_jsonld_callback if (self.enable_jsonld or self.enable_jsonp) else None
        
        # ~ for entry in self.entries:
            # ~ if jsonld_callback != None:
                # ~ jsonld_callback(entry)

    def entry_to_jsonld_callback(self, entry):
        if hasattr(entry, "schemadotorg"):
            optionals = entry.schemadotorg
                
        else:
            optionals = {}
        
        authors = [{"name":author, "@type": "Person"} for author in entry.authors]
        if "publisher" in entry.schemadotorg.keys():
            publisher = entry.schemadotorg["publisher"]
            
        elif "publisher" in self.blog_configuration["https://schema.org"].keys():
            publisher = self.blog_configuration["https://schema.org"]["publisher"]
        
        elif authors != []:
            publisher = authors
        
        else:
            publisher = {
                "@type":"Person",
                "name":self.blog_configuration["author_name"]
            }
        blog_url = self.blog_configuration["blog_url"]
        blog_url = blog_url+'/' if blog_url[-1] != '/' else blog_url
        entry_url = entry.path.replace("\x1a", blog_url)
        doc = {
            "@context": "http://schema.org",
            "@type" : ["BlogPosting", "WebPage"],
            "@id" : blog_url+entry.sub_folder+str(entry.id)+".jsonld",
            "keywords" : ','.join(tuple(set( [keyword.strip() for keyword in entry.tags + tuple(categories_to_keywords(entry.raw_categories))] ))),
            "headline" : entry.title,
            "name" : entry.title,
            "datePublished" : entry.date.isoformat(),
            "inLanguage" : self.blog_configuration["blog_language"],
            "author" : authors if authors != [] else self.blog_configuration["author_name"],
            "publisher" : publisher,
            "url" : entry_url,
            "breadcrumb" : {
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"root.jsonld",
                        "url": blog_url,
                        "name": self.blog_configuration["blog_name"]
                    }
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "item": {
                        "@id": blog_url+entry.sub_folder+str(entry.id) + ".jsonld",
                        "url": entry_url,
                        "name": entry.title
                    }
                }]
            },
            "relatedLink" : [ c.path for c in entry.categories_leaves],
            **optionals
        }
        self.entries_as_jsonld[entry.id] = doc
                
        blog_post = { "headline" : entry.title }
        blog_post.update({
            key : doc[key] for key in [
                "@type",
                "@id",
                "author",
                "publisher",
                "datePublished",
                "keywords",
                "url"
            ]
        })

        self.root_as_jsonld["blogPost"].append(blog_post)
        
        # Setup archives as jsonld if any
        entry_formatted_date = entry.formatted_date
        if entry_formatted_date not in self.archives_as_jsonld.keys():
            self.archives_to_jsonld(entry_formatted_date)
            
        self.archives_as_jsonld[entry.formatted_date]["blogPost"].append(blog_post)

        # Setup categories as jsonld if any
        self.walk_entry_categories_tree_and_make_jsonld(entry.categories_tree, blog_post)

    def root_site_to_jsonld(self):
        self.root_as_jsonld = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "@id" : self.blog_configuration["blog_url"]+"/root.jsonld",
            "name": self.blog_configuration["blog_name"],
            "url": self.blog_configuration["blog_url"],
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : {
                "@type": "CreativeWork",
                "name": self.blog_configuration["license"]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }

    def category_to_jsonld(self, category_path, category_value):
        blog_url = self.blog_configuration["blog_url"]
        blog_name = self.blog_configuration["blog_name"]
        self.categories_as_jsonld[category_path] = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "@id" : blog_url+'/'+category_path+"/categories.jsonld",
            "url": blog_url+'/'+category_path,
            "name": blog_name + ' | ' + category_value,
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : self.root_as_jsonld["license"],
            "breadcrumb" : {
                "@type": "BreadcrumbList",
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"/root.jsonld",
                        "url": blog_url,
                        "name": blog_name
                    }
                }]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }
                
    def archives_to_jsonld(self, archive_value):
        blog_url = self.blog_configuration["blog_url"]
        blog_name = self.blog_configuration["blog_name"]
        
        self.archives_as_jsonld[archive_value] = {
            "@context": "http://schema.org",
            "@type": ["Blog","WebPage"],
            "name": blog_name + ' | ' + archive_value,
            "description": self.blog_configuration["blog_description"],
            "author": {
                "@type" : "Person",
                "email" : self.blog_configuration["author_email"],
                "description" : self.blog_configuration["author_description"],
                "name" : self.blog_configuration["author_name"]
            },
            "keywords" : self.blog_configuration["blog_keywords"],
            "inLanguage" : self.blog_configuration["blog_language"],
            "license" : self.root_as_jsonld["license"],
            "breadcrumb" : {
                "@type": "BreadcrumbList",
                "itemListElement": [{
                    "@type": "ListItem",
                    "position": 1,
                    "item": {
                        "@id": blog_url+"/root.jsonld",
                        "url": blog_url,
                        "name": blog_name
                    }
                }]
            },
            "blogPost" : [],
            **self.optionals_schemadotorg
        }

    # TODO 3.x.x it may be possible to factorize code with a unique tree walking function
    def walk_entry_categories_tree_and_make_jsonld(self, categories_branch, blog_post):
        for category in categories_branch:
            if not category.path in self.categories_as_jsonld.keys():
                self.category_to_jsonld(category.path, category.value)
            
            self.categories_as_jsonld[category.path]["blogPost"].append(blog_post)
            self.walk_entry_categories_tree_and_make_jsonld(category.childs, blog_post)
