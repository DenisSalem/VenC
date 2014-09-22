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
            VenC.argv_handler(args);
        }
        else {
            new I18nManager();
            System.out.println(new I18nManager().getString("nothingToDo"));
        }
    }
    
    private static void argv_handler(String[] argv) {
        Core core = new Core();
        if (argv.length != 0) {
            switch(argv[0]) {
                case "-nb":
                    NewBlog newBlog = new NewBlog(core, argv[1]);
                    VenC.argv_handler(Arrays.copyOfRange(argv, 2, argv.length));
                    break;
                    
                default:
                    System.out.println(core.lang.getString("unknowCommand"));
                    VenC.argv_handler(Arrays.copyOfRange(argv, 1, argv.length));
                    break;
            }
        }
        else {
                System.out.println(core.lang.getString("nothingToDo"));       
        }
            
    }

}
