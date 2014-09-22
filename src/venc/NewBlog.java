/* This software is under GNU/GPL v3 license, see
http://www.gnu.org/copyleft/gpl.html */

package venc;

import java.io.File;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import org.yaml.snakeyaml.DumperOptions;
import venc.i18n.I18nManager;
import org.yaml.snakeyaml.Yaml;

public class NewBlog {
    public NewBlog(Core core, String blogName) {
        I18nManager lang = core.lang;
        
        core.printer(lang.getString("creatingNewBlog"));
        Map<String, Object> defaultConfiguration = new HashMap<String, Object>();
        defaultConfiguration.put("blog_name", "Blog name");
        defaultConfiguration.put("author_name", "Your name");
        defaultConfiguration.put("blog_description", "Blog description");
        defaultConfiguration.put("blog_keywdateFormat.format(new Date())ords", "Some keywords that are related to your blog");
        defaultConfiguration.put("author_description", "Tell the world something about you");
        defaultConfiguration.put("license", "The license applied to your content");
        defaultConfiguration.put("url", "Blog url");
        defaultConfiguration.put("blog_language", "The language of your blog");
        defaultConfiguration.put("email", "Your email");
        defaultConfiguration.put("sone", "Your sone");
        defaultConfiguration.put("wot", "Your public Web of Trust key");
        defaultConfiguration.put("freemail", "Your Freemail");
        defaultConfiguration.put("fms_public_key", "Your FMS public key");
        defaultConfiguration.put("bitcoin", "Your bitcoin address");
            Map<String, String> paths = new HashMap<String, String>();
            paths.put("root","./");
            paths.put("index_file_name","index{page_number}.html");
            paths.put("categories_directory_name","{category}");
            paths.put("tags_directory_name","{tag}");
            paths.put("authors_directory_name","{authors}");
            paths.put("dates_directory_name","%Y-%m");
            paths.put("entry_file_name","entry{entry_id}.html");
            paths.put("archives_overview_directory_name","overview");
            paths.put("rss_file_name","feed.xml");
        defaultConfiguration.put("paths", paths);
        defaultConfiguration.put("entries_per_pages","10");
        defaultConfiguration.put("columns","1");
        defaultConfiguration.put("rss_thread_lenght","10");
        defaultConfiguration.put("thread_order", "oldest first");
        
        core.mkdir(blogName);
        core.mkdir(blogName+"/blog");
        core.mkdir(blogName+"/theme");
        core.mkdir(blogName+"/entries");
        core.mkdir(blogName+"/templates");
        
        
        DumperOptions options = new DumperOptions();
        options.setDefaultFlowStyle(DumperOptions.FlowStyle.BLOCK);
        Yaml yamlDumper = new Yaml(options);
        core.writeFile("./"+blogName+"/blog_configuration.yaml", yamlDumper.dump(defaultConfiguration));
        
    }
}
