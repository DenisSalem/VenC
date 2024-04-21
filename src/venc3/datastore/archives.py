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

from venc3.datastore.metadata import MetadataNode
from venc3.datastore.metadata import WeightTracker
from venc3.helpers import quirk_encoding

class Archives:
    def init_archives(self):
        self.entries_per_archives = []
        self.archives_weight_tracker = WeightTracker()

        path_archives_sub_folders = self.blog_configuration["paths"]["archives_sub_folders"]
        compute_archives = self.blog_configuration["paths"]["archives_directory_name"] != '' and not self.blog_configuration["disable_archives"]

        if compute_archives:
            for entry_index in range(0, len(self.entries)):
                current_entry = self.entries[entry_index]
                formatted_date = current_entry.formatted_date
                archives_index = self.get_archives_index_for_given_date(formatted_date)
                if archives_index != None:
                    self.entries_per_archives[archives_index].count +=1
                    self.entries_per_archives[archives_index].weight_tracker.update()
                    self.entries_per_archives[archives_index].related_to.append(entry_index)

                else:
                    self.entries_per_archives.append(
                        MetadataNode(
                            formatted_date,
                            entry_index,
                            path= ("\x1a/"+path_archives_sub_folders+'/'+quirk_encoding(formatted_date)).replace('//','/'),
                            weight_tracker=self.archives_weight_tracker
                        )
                    )

    def get_archives_index_for_given_date(self, value):
        index = 0
        for metadata in self.entries_per_archives:
            if value == metadata.value:
                return index
            index += 1
