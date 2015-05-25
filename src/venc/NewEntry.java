/* This software is under GNU/GPL v3 license, see
http://www.gnu.org/copyleft/gpl.html */

package venc;

import java.util.HashMap;
import java.util.Map;
import org.yaml.snakeyaml.DumperOptions;
import org.yaml.snakeyaml.Yaml;

/**
 *
 * @author anonyme
 */
public class NewEntry {
    public NewEntry(Core core, String templateName, String entryName) {
        Map<String, Object> entry = new HashMap<String, Object>();
        int latestEntryId = core.getLatestEntryId();
        if (templateName.equals("default")) {
                    entry.put("entry_name", entryName);
                    entry.put("author_name", ""); // Better load the default author
                    entry.put("tags", "");
                    entry.put("categories", "");
        }
        else {
            // load and fill another template
        }
        
        DumperOptions options = new DumperOptions();
        options.setDefaultFlowStyle(DumperOptions.FlowStyle.BLOCK);
        Yaml yamlDumper = new Yaml(options);
        core.writeFile("./entries/"+latestEntryId+"__"+core.getDateTime()+"__"+entryName.replaceAll(" ","_"), yamlDumper.dump(entry));
    }
}
