/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package venc;

import java.io.File;
import java.io.FileOutputStream;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import venc.i18n.I18nManager;

/**
 *
 * @author anonyme
 */
public class Core {
    public I18nManager lang;
    
    public Core() {
        this.lang = new I18nManager();
    }
    
    public void printer(String string) {
        DateFormat dateFormat = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
        System.out.println(dateFormat.format(new Date())+" "+string);
    }
    public static boolean isInteger(String str) {
        int length = str.length();
	if (str == null) {
		return false;
	}

	if (length == 0) {
		return false;
	}
        
	for (int j = 0; j < length; j++) {
            char c = str.charAt(j);
            if (c <= '/' || c >= ':') {
                return false;
            }
	}
	return true;
    }

    public Boolean isFileAnEntry(String fileName) {
        String[] partedFileName = fileName.split("__");
        
        if (partedFileName.length < 3) {
            return false;
        }
        
        if (!this.isInteger(partedFileName[0])) {
            return false;
        }
        if (!this.isDateValid(partedFileName[1])) {
            return false;
        }
        return true;
    }

    public boolean isDateValid(String date) 
    {
        try {
            DateFormat df = new SimpleDateFormat("dd-MM-yyyy");
            df.setLenient(false);
            df.parse(date);
            return true;
        }
        catch (ParseException e) {
            return false;
        }
    }


    public int getLatestEntryId() {

    
        File dir = new File("entries");
    
        return 0;
    }
    public boolean mkdir(String folder) {
        File theDir = new File(folder);
        boolean mkdirTrace = false;

        if (!theDir.exists()) {
            try{
                theDir.mkdir();
                mkdirTrace = true;
            } catch(SecurityException se){
                this.printer(se.toString());
            }        
            if(mkdirTrace) {    
                this.printer(this.lang.getString("newFile")+" ./"+folder+"/");  
            }
        }
        else {
           this.printer("./"+folder+"/ "+this.lang.getString("alreadyExists"));
        }
            return mkdirTrace;
    }
    
    public void writeFile(String filename, String stream) {
        try {
            FileOutputStream out = new FileOutputStream(filename);
            out.write(stream.getBytes("utf-8"));
            out.close();
            this.printer(this.lang.getString("newFile")+" "+filename);
        }
        catch (Exception e) {
            this.printer(e.toString());
        }
    }
}
