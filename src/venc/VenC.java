/* This software is under GNU/GPL v3 license, see
http://www.gnu.org/copyleft/gpl.html */

package venc;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import venc.NewBlog;
import venc.i18n.I18nManager;
import java.util.Arrays;
import java.util.Date;
/**
 *
 * @author denissalem
 */
public class VenC {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        if (args.length != 0) {
            Core core = new Core();
            VenC.argv_handler(core, args);
        }
        else {
            new I18nManager();
            System.out.println(new I18nManager().getString("nothingToDo"));
        }
    }
    
    private static void argv_handler(Core core, String[] argv) {
        try {
            if (argv.length != 0) {
                switch(argv[0]) {
                    case "-nb":
                        NewBlog newBlog = new NewBlog(core, argv[1]);
                        VenC.argv_handler(core, Arrays.copyOfRange(argv, 2, argv.length));
                        break;
                    case "-ne":
                        core.fastEntriesOverview();
                        NewEntry newEntry = new NewEntry(core, argv[1]);
                        VenC.argv_handler(core, Arrays.copyOfRange(argv, 2, argv.length));
                        break;
                    default:
                        System.out.println(argv[0]+": "+core.lang.getString("unknowCommand"));
                        VenC.argv_handler(core, Arrays.copyOfRange(argv, 1, argv.length));
                        break;
                }
            }
            else {
                    core.printer(core.lang.getString("nothingToDo"));       
                }
        }
        catch (java.lang.ArrayIndexOutOfBoundsException e) {
            core.printer(argv[0]+": "+core.lang.getString("missingArguments"));
        }
            
    }

}
