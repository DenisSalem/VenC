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
    public NewEntry(Core core, String entryName) {
        Map<String, Object> entry = new HashMap<String, Object>();
        int latestEntryId = core.getLatestEntryId();
        
        entry.put("entry_name", entryName);
        entry.put("author_name", ""); // Better load the default author
        entry.put("tags", "");
        entry.put("categories", "");
        
        DumperOptions options = new DumperOptions();
        options.setDefaultFlowStyle(DumperOptions.FlowStyle.BLOCK);
        Yaml yamlDumper = new Yaml(options);

        core.writeFile("./entries/"+latestEntryId+"__"+core.getDateTime()+"__"+entryName.replaceAll(" ","_"), yamlDumper.dump(entry));
 
    }
}
