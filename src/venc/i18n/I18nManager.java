/* This software is under GNU/GPL v3 license, see
http://www.gnu.org/copyleft/gpl.html */

package venc.i18n;
import java.util.*;

public class I18nManager {
    public String systemDefaultLocale = Locale.getDefault().getLanguage();
    public ResourceBundle message;
    
    public I18nManager() {
        switch (systemDefaultLocale) {
            case "fr":
                this.message = ResourceBundle.getBundle("venc/i18n/MessagesBundle", new Locale("fr","FR"));
                break;
            default:
                this.message = ResourceBundle.getBundle("venc/i18n/MessagesBundle", new Locale("en","EN"));
        }
        
    }
    
    public String getString(String string) {
        return this.message.getString(string);
    }
}
